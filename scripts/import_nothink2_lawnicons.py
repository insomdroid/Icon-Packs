#!/usr/bin/env python3
"""Import selected Lawnicons SVG artwork as compact Nothing-dark assets."""
import argparse
import io
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image

ANDROID = "{http://schemas.android.com/apk/res/android}"


def safe_name(value):
    value = re.sub(r"[^a-z0-9_]", "_", value.lower())
    return value if value and value[0].isalpha() else "icon_" + value


def white_svg(source):
    source = re.sub(
        r"""(["'])(?:#000(?:000)?|#111(?:111)?|black)(["'])""",
        r"\1#ffffff\2",
        source,
        flags=re.IGNORECASE,
    )
    source = re.sub(
        r"""(fill|stroke)=(['"])currentColor\2""",
        r'\1="#ffffff"',
        source,
        flags=re.IGNORECASE,
    )
    return source.replace("currentColor", "#ffffff").encode("utf-8")


def write_xml(element, destination):
    ET.ElementTree(element).write(
        destination,
        encoding="utf-8",
        xml_declaration=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--module", type=Path, default=Path("pack-nothink2"))
    parser.add_argument(
        "--popular-list",
        type=Path,
        help="Optional newline-separated package allowlist; omit to import all supported apps.",
    )
    args = parser.parse_args()

    root = args.upstream
    svgs = root / "svgs"
    source_filter = root / "app/assets/appfilter.xml"
    if not svgs.is_dir() or not source_filter.is_file():
        raise SystemExit("Pinned Lawnicons source archive is incomplete")

    selected = None
    if args.popular_list:
        selected = {
            line.strip()
            for line in args.popular_list.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        if not selected:
            raise SystemExit("The supplied package allowlist is empty")

    res = args.module / "src/main/res"
    glyphs = res / "drawable-nodpi"
    wrappers = res / "drawable"
    adaptive = res / "drawable-anydpi-v26"
    xml = res / "xml"
    for folder in (glyphs, wrappers, adaptive, xml):
        folder.mkdir(parents=True, exist_ok=True)

    for pattern in ("*_glyph.png", "*_glyph.webp"):
        for stale in glyphs.glob(pattern):
            stale.unlink()
    # This directory is generated entirely from the pinned upstream mapping.
    for stale in adaptive.glob("*.xml"):
        stale.unlink()

    ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
    source = ET.parse(source_filter).getroot()
    appfilter = ET.Element("resources")
    drawable_list = ET.Element("resources")
    themed = ET.Element("icons")
    done, packages = set(), set()
    component_count = 0

    for item in source.findall("item"):
        component, drawable = item.get("component"), item.get("drawable")
        if not component or not drawable:
            continue
        match = re.search(r"ComponentInfo\{([^/]+)/", component)
        if not match or (selected is not None and match.group(1) not in selected):
            continue

        name = safe_name(drawable)
        if name not in done:
            svg = svgs / (drawable + ".svg")
            if not svg.is_file():
                continue

            # 120 px glyph in a 192 px transparent canvas keeps the original
            # compact appearance and leaves room for adaptive-icon masking.
            rendered = cairosvg.svg2png(
                bytestring=white_svg(svg.read_text(encoding="utf-8")),
                output_width=120,
                output_height=120,
            )
            glyph = Image.open(io.BytesIO(rendered)).convert("RGBA")
            canvas = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
            canvas.alpha_composite(
                glyph,
                ((192 - glyph.width) // 2, (192 - glyph.height) // 2),
            )
            canvas.save(
                glyphs / (name + "_glyph.webp"),
                format="WEBP",
                lossless=True,
                method=6,
            )

            # Conventional icon-pack fallback: dark circular background + glyph.
            layer = ET.Element("layer-list")
            bg_item = ET.SubElement(layer, "item")
            bg_shape = ET.SubElement(
                bg_item, "shape", {ANDROID + "shape": "oval"}
            )
            ET.SubElement(bg_shape, "solid", {ANDROID + "color": "#171717"})
            ET.SubElement(
                layer,
                "item",
                {ANDROID + "drawable": "@drawable/" + name + "_glyph"},
            )
            write_xml(layer, wrappers / (name + ".xml"))

            # Android 8+ adaptive drawable. The launcher supplies the mask;
            # the original dark background and white artwork remain unchanged.
            adaptive_icon = ET.Element("adaptive-icon")
            ET.SubElement(
                adaptive_icon,
                "background",
                {ANDROID + "drawable": "@color/icon_adaptive_background"},
            )
            ET.SubElement(
                adaptive_icon,
                "foreground",
                {ANDROID + "drawable": "@drawable/" + name + "_glyph"},
            )
            ET.SubElement(
                adaptive_icon,
                "monochrome",
                {ANDROID + "drawable": "@drawable/" + name + "_glyph"},
            )
            write_xml(adaptive_icon, adaptive / (name + ".xml"))

            ET.SubElement(drawable_list, "item", {"drawable": name})
            done.add(name)

        ET.SubElement(appfilter, "item", {"component": component, "drawable": name})
        package = match.group(1)
        if package not in packages:
            ET.SubElement(
                themed,
                "icon",
                {
                    "package": package,
                    "drawable": "@drawable/" + name + "_glyph",
                },
            )
            packages.add(package)
        component_count += 1

    missing = selected - packages if selected is not None else set()
    if missing:
        sample = ", ".join(sorted(missing)[:10])
        raise SystemExit(
            f"Only {len(packages)}/{len(selected)} selected apps were imported. "
            f"Missing examples: {sample}"
        )

    ET.SubElement(appfilter, "iconback", {"img": "icon_background"})
    ET.SubElement(appfilter, "scale", {"factor": "0.72"})
    for element, filename in (
        (appfilter, "appfilter.xml"),
        (drawable_list, "drawable.xml"),
        (themed, "grayscale_icon_map.xml"),
    ):
        write_xml(element, xml / filename)

    adaptive_count = len(list(adaptive.glob("*.xml")))
    if adaptive_count != len(done):
        raise SystemExit(
            f"Adaptive resource mismatch: {adaptive_count} files for {len(done)} icons"
        )

    print(
        f"Imported {component_count} mapped components for {len(packages)} supported apps, "
        f"{len(done)} unique WebP glyphs and {adaptive_count} adaptive drawables."
    )


if __name__ == "__main__":
    main()
