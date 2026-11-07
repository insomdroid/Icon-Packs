#!/usr/bin/env python3
"""Build the Nothink monochrome icon artwork and Lawnicons app mappings.

Lawnicons SVGs are rasterized to transparent monochrome glyph layers. The
standard icon-pack layer adds a restrained near-black circular field; the
themed-icon layer contains only the glyph alpha so compatible launchers can
tint it from the current wallpaper. Every mapped drawable is generated before
Gradle starts, so no first-launch download or on-device generation is needed.
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack-nothing" / "src" / "main" / "res"
ICON_SIZE = 192
MIN_MAPPINGS = 3000
BACKGROUND = (16, 16, 16, 255)
FOREGROUND = (255, 255, 255, 255)


def resource_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value or value[0].isdigit():
        value = "_" + (value or "icon")
    return value[:120]


def component_package(component: str) -> str | None:
    match = re.fullmatch(r"ComponentInfo\\{([^/]+)/[^}]+\\}", component.strip())
    return match.group(1) if match else None


def render_glyph(svg_path: Path) -> tuple[Image.Image, Image.Image]:
    rendered = cairosvg.svg2png(
        bytestring=svg_path.read_bytes(),
        output_width=ICON_SIZE,
        output_height=ICON_SIZE,
    )
    from io import BytesIO

    source = Image.open(BytesIO(rendered)).convert("RGBA")
    alpha = source.getchannel("A")
    luminance = source.convert("L")
    # Lawnicons source artwork is black on transparent. This also removes a
    # possible white canvas while retaining antialiased dark strokes.
    darkness = Image.eval(luminance, lambda value: 255 - value)
    mask = Image.new("L", (ICON_SIZE, ICON_SIZE))
    source_alpha = alpha.load()
    darkness_pixels = darkness.load()
    mask_pixels = mask.load()
    for y in range(ICON_SIZE):
        for x in range(ICON_SIZE):
            mask_pixels[x, y] = source_alpha[x, y] * darkness_pixels[x, y] // 255

    bounds = mask.getbbox()
    if bounds is None:
        raise ValueError(f"SVG has no visible dark artwork: {svg_path.name}")
    glyph = mask.crop(bounds)
    glyph.thumbnail((132, 132), Image.Resampling.LANCZOS)

    glyph_layer = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    white_glyph = Image.new("RGBA", glyph.size, FOREGROUND)
    glyph_layer.alpha_composite(
        Image.composite(white_glyph, Image.new("RGBA", glyph.size), glyph)
    )
    left = (ICON_SIZE - glyph.width) // 2
    top = (ICON_SIZE - glyph.height) // 2
    placed_glyph = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    placed_glyph.alpha_composite(glyph_layer, (left, top))

    static_icon = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(static_icon)
    draw.ellipse((8, 8, ICON_SIZE - 8, ICON_SIZE - 8), fill=BACKGROUND)
    static_icon.alpha_composite(placed_glyph)
    return static_icon, placed_glyph


def save_png(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="PNG", optimize=True, compress_level=9)


def write_xml(root: ET.Element, destination: Path) -> None:
    ET.indent(root, space="  ")
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(destination, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lawnicons-root", required=True, type=Path)
    args = parser.parse_args()

    upstream = args.lawnicons_root.resolve()
    source_filter = upstream / "app" / "assets" / "appfilter.xml"
    source_svgs = upstream / "svgs"
    if not source_filter.is_file() or not source_svgs.is_dir():
        raise SystemExit("The pinned Lawnicons checkout is missing app/assets/appfilter.xml or svgs/.")

    source_root = ET.parse(source_filter).getroot()
    source_items = [item for item in source_root.iter("item") if item.get("component") and item.get("drawable")]
    if len(source_items) < MIN_MAPPINGS:
        raise SystemExit(
            f"Lawnicons mapping has only {len(source_items)} app entries; "
            f"at least {MIN_MAPPINGS} are required."
        )

    drawable_to_label: dict[str, str] = {}
    component_to_drawable: dict[str, tuple[str, str]] = {}
    package_to_drawable: dict[str, str] = {}
    missing: list[str] = []

    for item in source_items:
        original_drawable = item.attrib["drawable"].removeprefix("@drawable/")
        drawable = resource_name(original_drawable)
        component = item.attrib["component"].strip()
        label = item.attrib.get("name", original_drawable).strip()
        svg = source_svgs / f"{original_drawable}.svg"
        if not svg.is_file():
            missing.append(f"{component} -> {original_drawable}.svg")
            continue
        drawable_to_label.setdefault(drawable, label)
        component_to_drawable[component] = (drawable, label)
        package = component_package(component)
        if package:
            package_to_drawable.setdefault(package, drawable)

    if missing:
        preview = "\\n".join(missing[:25])
        raise SystemExit(
            f"{len(missing)} Lawnicons mappings reference SVGs that are absent. "
            f"Refusing to create an incomplete pack. First missing entries:\\n{preview}"
        )
    if len(component_to_drawable) < MIN_MAPPINGS:
        raise SystemExit(
            f"Only {len(component_to_drawable)} unique component mappings remain after validation."
        )

    drawable_dir = PACK / "drawable-nodpi"
    themed_dir = PACK / "drawable-nodpi"
    drawable_dir.mkdir(parents=True, exist_ok=True)

    for drawable in sorted(drawable_to_label):
        original_name = next(
            item.attrib["drawable"].removeprefix("@drawable/")
            for item in source_items
            if resource_name(item.attrib["drawable"].removeprefix("@drawable/")) == drawable
        )
        static_icon, themed_icon = render_glyph(source_svgs / f"{original_name}.svg")
        save_png(static_icon, drawable_dir / f"{drawable}.png")
        save_png(themed_icon, themed_dir / f"themed_{drawable}.png")

    appfilter = ET.Element("resources")
    for component, (drawable, label) in sorted(component_to_drawable.items()):
        ET.SubElement(
            appfilter,
            "item",
            {"component": component, "drawable": drawable, "name": label},
        )
    write_xml(appfilter, PACK / "xml" / "appfilter.xml")

    assets_filter = ROOT / "pack-nothing" / "src" / "main" / "assets" / "appfilter.xml"
    write_xml(appfilter, assets_filter)

    drawable_index = ET.Element("resources")
    for drawable, label in sorted(drawable_to_label.items()):
        ET.SubElement(drawable_index, "item", {"drawable": drawable, "name": label})
    write_xml(drawable_index, PACK / "xml" / "drawable.xml")

    themed_map = ET.Element("icons")
    for package, drawable in sorted(package_to_drawable.items()):
        ET.SubElement(
            themed_map,
            "icon",
            {"package": package, "drawable": f"@drawable/themed_{drawable}"},
        )
    write_xml(themed_map, PACK / "xml" / "grayscale_icon_map.xml")

    print(f"NOTHINK_APP_MAPPINGS={len(component_to_drawable)}")
    print(f"NOTHINK_UNIQUE_ARTWORK={len(drawable_to_label)}")
    print(f"NOTHINK_THEMED_PACKAGES={len(package_to_drawable)}")
    print("NOTHINK_MISSING_ARTWORK=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"NOTHINK_GENERATION_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
