#!/usr/bin/env python3
"""Extract Jelly Bean archives and compare their icons with archived KitKat assets."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath

import imagehash
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "kitkat-archives"
OUT = ROOT / "build" / "jellybean-archive-inspection"
ARCHIVES = ["Icons jb 1.zip", "icons jb2.zip"]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
KITKAT_DIRS = [
    SOURCE / "drawable-xxxhdpi",
    SOURCE / "drawable-xxhdpi",
]


def safe_extract(zf: zipfile.ZipFile, destination: Path) -> None:
    destination_resolved = destination.resolve()
    for info in zf.infolist():
        if info.is_dir():
            continue
        member = PurePosixPath(info.filename)
        if member.is_absolute() or ".." in member.parts:
            raise ValueError(f"Unsafe ZIP path: {info.filename}")
        target = (destination / Path(*member.parts)).resolve()
        if destination_resolved not in target.parents and target != destination_resolved:
            raise ValueError(f"ZIP path escapes destination: {info.filename}")
        target.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(info) as src, target.open("wb") as dst:
            while chunk := src.read(1024 * 1024):
                dst.write(chunk)


def read_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perceptual_hash(path: Path):
    with Image.open(path) as image:
        image = image.convert("RGBA")
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        background.alpha_composite(image)
        return imagehash.phash(background.convert("RGB"))


def make_contact_sheets(rows: list[dict], out_dir: Path, prefix: str) -> None:
    if not rows:
        return
    thumb_w, thumb_h, label_h = 144, 144, 42
    cols, per_page = 6, 60
    font = ImageFont.load_default()
    for page_start in range(0, len(rows), per_page):
        page = rows[page_start:page_start + per_page]
        page_no = page_start // per_page + 1
        canvas = Image.new("RGB", (cols * thumb_w, ((len(page) + cols - 1) // cols) * (thumb_h + label_h)), "white")
        draw = ImageDraw.Draw(canvas)
        for index, row in enumerate(page):
            path = Path(row["extracted_path"])
            try:
                with Image.open(path) as im:
                    im = im.convert("RGBA")
                    im.thumbnail((thumb_w - 12, thumb_h - 12))
                tile = Image.new("RGBA", (thumb_w, thumb_h), (238, 238, 238, 255))
                tile.alpha_composite(im, ((thumb_w - im.width) // 2, (thumb_h - im.height) // 2))
                x, y = (index % cols) * thumb_w, (index // cols) * (thumb_h + label_h)
                canvas.paste(tile.convert("RGB"), (x, y))
                label = row["archive_path"].replace("\\", "/")
                label = label if len(label) <= 27 else "…" + label[-26:]
                draw.text((x + 3, y + thumb_h + 2), label, fill="black", font=font)
                draw.text((x + 3, y + thumb_h + 15), f'{row["width"]}x{row["height"]}  {row["sha256"][:10]}', fill="black", font=font)
            except Exception as exc:
                print(f"Cannot thumbnail {path}: {exc}")
        canvas.save(out_dir / f"{prefix}-contact-{page_no:02d}.jpg", quality=88)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict] = []
    by_hash: dict[str, list[dict]] = defaultdict(list)

    for archive_name in ARCHIVES:
        archive_path = SOURCE / archive_name
        if not archive_path.is_file():
            raise FileNotFoundError(f"Missing uploaded archive: {archive_path}")
        prefix = re.sub(r"[^a-z0-9]+", "-", archive_path.stem.lower()).strip("-")
        destination = OUT / prefix
        destination.mkdir(parents=True, exist_ok=True)
        print(f"Extracting {archive_name} ({archive_path.stat().st_size:,} bytes)")
        with zipfile.ZipFile(archive_path) as zf:
            safe_extract(zf, destination)

        rows: list[dict] = []
        for path in sorted(destination.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
                continue
            digest = read_hash(path)
            width = height = 0
            mode = "unreadable"
            try:
                with Image.open(path) as im:
                    width, height = im.size
                    mode = im.mode
                    im.verify()
            except Exception:
                pass
            row = {
                "archive": archive_name,
                "archive_path": path.relative_to(destination).as_posix(),
                "extracted_path": str(path),
                "extension": path.suffix.lower(),
                "width": width,
                "height": height,
                "mode": mode,
                "bytes": path.stat().st_size,
                "sha256": digest,
            }
            rows.append(row)
            all_rows.append(row)
            by_hash[digest].append(row)

        with (OUT / f"{prefix}-images.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
                "archive", "archive_path", "extracted_path", "extension", "width", "height", "mode", "bytes", "sha256"
            ])
            writer.writeheader()
            writer.writerows(rows)
        make_contact_sheets(rows, OUT, prefix)
        print(f"{archive_name}: {len(rows)} image files, {len({r['sha256'] for r in rows})} unique image hashes")

    with (OUT / "all-images.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()) if all_rows else [])
        if all_rows:
            writer.writeheader()
            writer.writerows(all_rows)

    # Only use known KitKat application bitmap assets as comparison references.
    kitkat_rows = []
    for directory in KITKAT_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.iterdir()):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                try:
                    kitkat_rows.append({
                        "kitkat_path": path.relative_to(ROOT).as_posix(),
                        "extracted_path": str(path),
                        "sha256": read_hash(path),
                        "phash": str(perceptual_hash(path)),
                    })
                except Exception as exc:
                    print(f"Skipping unreadable KitKat image {path}: {exc}")

    unique_jb = {}
    for row in all_rows:
        unique_jb.setdefault(row["sha256"], row)

    matches = []
    for ref in kitkat_rows:
        ref_hash = ref["phash"]
        ranked = []
        for jb in unique_jb.values():
            try:
                distance = perceptual_hash(Path(jb["extracted_path"])) - imagehash.hex_to_hash(ref_hash)
            except Exception:
                continue
            ranked.append((distance, jb))
        ranked.sort(key=lambda item: item[0])
        for distance, jb in ranked[:5]:
            matches.append({
                "kitkat_path": ref["kitkat_path"],
                "jellybean_archive": jb["archive"],
                "jellybean_icon": jb["archive_path"],
                "phash_distance": distance,
                "exact_sha256_match": ref["sha256"] == jb["sha256"],
                "jellybean_sha256": jb["sha256"],
            })

    matches.sort(key=lambda x: (x["kitkat_path"], x["phash_distance"]))
    with (OUT / "kitkat-jellybean-nearest-matches.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["kitkat_path", "jellybean_archive", "jellybean_icon", "phash_distance", "exact_sha256_match", "jellybean_sha256"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(matches)

    duplicate_groups = [
        {"sha256": digest, "count": len(items), "files": [f'{x["archive"]}:{x["archive_path"]}' for x in items]}
        for digest, items in sorted(by_hash.items()) if len(items) > 1
    ]
    summary = {
        "archives": ARCHIVES,
        "image_file_count_including_duplicates": len(all_rows),
        "unique_image_hash_count": len(by_hash),
        "duplicate_groups_count": len(duplicate_groups),
        "kitkat_reference_image_count": len(kitkat_rows),
        "kitkat_jellybean_nearest_match_rows": len(matches),
        "exact_cross_version_matches": sum(1 for x in matches if x["exact_sha256_match"]),
        "best_perceptual_matches_distance_0_to_8": sum(1 for x in matches if x["phash_distance"] <= 8),
        "counts_by_archive": {
            name: {
                "image_files": sum(1 for row in all_rows if row["archive"] == name),
                "unique_hashes": len({row["sha256"] for row in all_rows if row["archive"] == name}),
            } for name in ARCHIVES
        },
        "kitkat_reference_assets": [x["kitkat_path"] for x in kitkat_rows],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    report = [
        "# Jelly Bean / KitKat icon comparison",
        "",
        f'- Images extracted: **{len(all_rows)}**',
        f'- Unique image files by SHA-256: **{len(by_hash)}**',
        f'- KitKat bitmap references compared: **{len(kitkat_rows)}**',
        f'- Exact cross-version matches: **{summary["exact_cross_version_matches"]}**',
        f'- Perceptual candidates with pHash distance ≤ 8: **{summary["best_perceptual_matches_distance_0_to_8"]}** (review visually; not automatically accepted)',
        "",
        "The CSV lists the five closest Jelly Bean candidates for each KitKat bitmap. A low perceptual distance is only a candidate, not proof that the artwork is identical.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
