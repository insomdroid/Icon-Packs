#!/usr/bin/env python3
"""Apply user-supplied, app-specific SVG artwork to the generated Nothink icon set."""
from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import statistics
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import cairosvg
import requests
from PIL import Image

MAX_DOWNLOAD = 100 * 1024 * 1024
MAX_ENTRIES = 300
MAX_SVG_SIZE = 5 * 1024 * 1024
CANVAS = 192
ALLOWED_HOSTS = {"github.com", "githubusercontent.com", "user-images.githubusercontent.com"}


def normalize_name(value: str) -> str:
    value = Path(value).stem.lower()
    value = re.sub(r"[^a-z0-9]+", "", value)
    return value


def download_archive(url: str, destination: Path) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise SystemExit("SVG ZIP URL must be HTTPS and hosted on github.com or githubusercontent.com.")
    total = 0
    with requests.get(url, stream=True, timeout=(20, 90), allow_redirects=True,
                      headers={"User-Agent": "Nothink-SVG-Importer/1.0"}) as response:
        response.raise_for_status()
        final = urlparse(response.url)
        if final.scheme != "https" or final.hostname not in ALLOWED_HOSTS:
            raise SystemExit("SVG ZIP redirected to an untrusted host.")
        with destination.open("wb") as output:
            for chunk in response.iter_content(1024 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                if total > MAX_DOWNLOAD:
                    raise SystemExit("SVG ZIP exceeds the 100 MB limit.")
                output.write(chunk)
    if not zipfile.is_zipfile(destination):
        raise SystemExit("The supplied URL did not return a valid ZIP archive.")


def make_alpha_mask(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = list(rgba.getdata())
    alpha_values = [p[3] for p in pixels]
    opaque = [p for p in pixels if p[3] > 245]
    if not opaque:
        raise ValueError("SVG has no visible artwork.")

    # Transparent exports keep their authored alpha. For flattened exports,
    # infer a silhouette from contrast against the canvas corner color.
    transparent_ratio = sum(1 for a in alpha_values if a < 245) / len(alpha_values)
    if transparent_ratio > 0.01:
        mask_values = alpha_values
    else:
        w, h = rgba.size
        corners = [
            rgba.getpixel((0, 0)), rgba.getpixel((w - 1, 0)),
            rgba.getpixel((0, h - 1)), rgba.getpixel((w - 1, h - 1)),
        ]
        bg = tuple(int(statistics.median(c[i] for c in corners)) for i in range(3))
        bg_luma = bg[0] * 0.2126 + bg[1] * 0.7152 + bg[2] * 0.0722
        mask_values = []
        for r, g, b, a in pixels:
            luma = r * 0.2126 + g * 0.7152 + b * 0.0722
            if bg_luma >= 128:
                value = max(0, int((bg_luma - luma) * 2.0))
            else:
                value = max(0, int((luma - bg_luma) * 2.0))
            mask_values.append(min(255, value) * a // 255)

    mask = Image.new("RGBA", rgba.size, (255, 255, 255, 0))
    mask.putdata([(255, 255, 255, a) for a in mask_values])
    bbox = mask.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Could not detect a foreground silhouette.")
    cropped = mask.crop(bbox)
    cropped.thumbnail((int(CANVAS * 0.72), int(CANVAS * 0.72)), Image.Resampling.LANCZOS)
    result = Image.new("RGBA", (CANVAS, CANVAS), (255, 255, 255, 0))
    result.alpha_composite(cropped, ((CANVAS - cropped.width) // 2, (CANVAS - cropped.height) // 2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="HTTPS URL of a ZIP containing SVG files")
    parser.add_argument("--report", default="build/jusicons-report/report.json")
    parser.add_argument("--output-report", default="build/jusicons-report/svg-import-report.json")
    parser.add_argument("--minimum-matches", type=int, default=1)
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.is_file():
        raise SystemExit(f"Missing APK extraction report: {report_path}")
    base_report = json.loads(report_path.read_text(encoding="utf-8"))
    apps = base_report.get("apps", [])
    if not apps:
        raise SystemExit("APK extraction report contains no application mappings.")

    lookup = {}
    for app in apps:
        if app.get("status") != "generated":
            continue
        candidates = {
            app.get("label", ""),
            app.get("package", ""),
            app.get("drawable", ""),
        }
        for candidate in candidates:
            key = normalize_name(candidate)
            if key:
                lookup.setdefault(key, []).append(app)

    archive_path = Path("build/uploaded-nothink-artwork.zip")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    download_archive(args.url, archive_path)

    import importlib.util
    generator_path = Path("scripts/generate_jusicons_batch.py")
    spec = importlib.util.spec_from_file_location("nothink_generator", generator_path)
    if spec is None or spec.loader is None:
        raise SystemExit("Unable to load the existing Nothink vectorizer.")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)

    seen = set()
    results = []
    with zipfile.ZipFile(archive_path) as archive:
        files = [entry for entry in archive.infolist()
                 if not entry.is_dir() and entry.filename.lower().endswith(".svg")]
        if len(files) > MAX_ENTRIES:
            raise SystemExit(f"ZIP contains {len(files)} SVG files; maximum is {MAX_ENTRIES}.")
        for entry in files:
            filename = Path(entry.filename)
            if filename.is_absolute() or ".." in filename.parts:
                results.append({"file": entry.filename, "status": "rejected", "reason": "unsafe path"})
                continue
            if entry.file_size > MAX_SVG_SIZE:
                results.append({"file": entry.filename, "status": "rejected", "reason": "SVG exceeds 5 MB"})
                continue
            key = normalize_name(filename.name)
            candidates = lookup.get(key, [])
            if len(candidates) != 1:
                results.append({
                    "file": entry.filename,
                    "status": "unmatched" if not candidates else "ambiguous",
                    "matches": [item.get("label") for item in candidates],
                })
                continue
            app = candidates[0]
            drawable = app["drawable"]
            if drawable in seen:
                results.append({"file": entry.filename, "status": "duplicate", "app": app["label"]})
                continue
            try:
                source = archive.read(entry)
                if b"<script" in source.lower() or b"<foreignobject" in source.lower():
                    raise ValueError("SVG contains unsupported active content.")
                png = cairosvg.svg2png(bytestring=source, output_width=CANVAS, output_height=CANVAS)
                image = Image.open(io.BytesIO(png)).convert("RGBA")
                mask = make_alpha_mask(image)
                path_data = generator.vectorize(mask)
                if not path_data:
                    raise ValueError("Vectorized foreground is empty.")
                xml = (
                    '<?xml version="1.0" encoding="utf-8"?>\n'
                    '<vector xmlns:android="http://schemas.android.com/apk/res/android" '
                    'android:width="48dp" android:height="48dp" '
                    'android:viewportWidth="48" android:viewportHeight="48">\n'
                    '    <path android:fillColor="#FF000000" android:pathData="M0,0h48v48h-48Z" />\n'
                    f'    <path android:fillColor="#FFFFFFFF" android:pathData="{html.escape(path_data, quote=True)}" />\n'
                    '</vector>\n'
                )
                output = Path("pack-nothing/src/main/res/drawable") / f"{drawable}.xml"
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(xml, encoding="utf-8")
                seen.add(drawable)
                results.append({
                    "file": entry.filename,
                    "status": "applied",
                    "app": app["label"],
                    "package": app["package"],
                    "drawable": drawable,
                    "svg_sha256": hashlib.sha256(source).hexdigest(),
                    "vector_path_characters": len(path_data),
                })
            except Exception as exc:
                results.append({"file": entry.filename, "status": "failed", "app": app["label"], "reason": str(exc)})

    applied = sum(item["status"] == "applied" for item in results)
    output = {
        "source": "user-uploaded SVG ZIP",
        "svg_files_found": len(files),
        "applied_icons": applied,
        "unmatched_or_failed": len(results) - applied,
        "results": results,
    }
    output_path = Path(args.output_report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"SVG_FILES={len(files)} APPLIED={applied} OTHER={len(results) - applied}")
    if applied < args.minimum_matches:
        print(f"ERROR: only {applied} SVG files matched; minimum is {args.minimum_matches}.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
