#!/usr/bin/env python3
"""Create original Nothink artwork from Lawnicons app-component mappings only."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack-nothing" / "src" / "main" / "res"
ICON_SIZE = 192
SCALE = 3
CANVAS = ICON_SIZE * SCALE
MIN_MAPPINGS = 3000
BACKGROUND = (15, 15, 15, 255)
WHITE = (245, 245, 242, 255)
RED = (238, 45, 52, 255)
TRANSPARENT = (0, 0, 0, 0)


def resource_name(value: str) -> str:
    value = re.sub(r"[^a-z0-9_]+", "_", value.strip().lower())
    value = re.sub(r"_+", "_", value).strip("_")
    if not value or value[0].isdigit():
        value = "_" + (value or "icon")
    return value[:120]


def component_package(component: str) -> str | None:
    match = re.fullmatch(r"ComponentInfo\{([^/]+)/[^}]+\}", component.strip())
    return match.group(1) if match else None


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def initials(label: str, package: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9 ]+", " ", label).strip()
    words = [word for word in clean.split() if word]
    if len(words) >= 2:
        result = (words[0][0] + words[1][0]).upper()
    elif words:
        result = words[0][:2].upper()
    else:
        parts = [part for part in re.split(r"[._-]+", package) if part]
        result = (parts[-1][:2] if parts else "N").upper()
    return result[:2]


def draw_icon(label: str, package: str, drawable: str) -> tuple[Image.Image, Image.Image]:
    identity = f"{package}|{drawable}|{label}"
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    variant = digest[0] % 6
    accent_side = digest[1] % 4
    glyph = initials(label, package)

    layer = Image.new("RGBA", (CANVAS, CANVAS), TRANSPARENT)
    draw = ImageDraw.Draw(layer)

    # Original Nothing-inspired visual language: restrained geometry,
    # precise white strokes, and one signal-red indicator.
    margin = 28 * SCALE
    stroke = 4 * SCALE
    center = CANVAS // 2
    draw.rounded_rectangle(
        (margin, margin, CANVAS - margin, CANVAS - margin),
        radius=25 * SCALE,
        outline=WHITE,
        width=stroke,
    )

    # Each mapped app gets its own deterministic technical frame motif.
    inset = (42 + (digest[2] % 9)) * SCALE
    if variant in (0, 3):
        draw.arc((inset, inset, CANVAS - inset, CANVAS - inset),
                 start=205 + digest[3] % 25, end=330 + digest[4] % 20,
                 fill=WHITE, width=stroke)
    elif variant in (1, 4):
        y = (48 + digest[3] % 20) * SCALE
        draw.line((inset, y, CANVAS - inset, y), fill=WHITE, width=stroke)
        draw.line((inset, CANVAS - y, CANVAS - inset, CANVAS - y),
                  fill=WHITE, width=stroke)
    else:
        x = (48 + digest[3] % 20) * SCALE
        draw.line((x, inset, x, CANVAS - inset), fill=WHITE, width=stroke)
        draw.line((CANVAS - x, inset, CANVAS - x, CANVAS - inset),
                  fill=WHITE, width=stroke)

    font_size = (57 if len(glyph) == 1 else 48) * SCALE
    font = load_font(font_size, bold=True)
    bounds = draw.textbbox((0, 0), glyph, font=font, stroke_width=0)
    text_w, text_h = bounds[2] - bounds[0], bounds[3] - bounds[1]
    draw.text((center - text_w / 2 - bounds[0],
               center - text_h / 2 - bounds[1] + (digest[5] % 7 - 3) * SCALE),
              glyph, font=font, fill=WHITE)

    # A signature red status point changes position per mapped illustration.
    dot = 8 * SCALE
    positions = [
        (CANVAS - 47 * SCALE, 47 * SCALE),
        (47 * SCALE, 47 * SCALE),
        (CANVAS - 47 * SCALE, CANVAS - 47 * SCALE),
        (47 * SCALE, CANVAS - 47 * SCALE),
    ]
    px, py = positions[accent_side]
    draw.ellipse((px - dot, py - dot, px + dot, py + dot), fill=RED)

    # Small data ticks make the collection coherent without using upstream art.
    tick_count = 2 + digest[6] % 4
    for index in range(tick_count):
        x = (62 + index * 13) * SCALE
        y = (CANVAS - 61) * SCALE
        length = (7 + digest[7 + index] % 8) * SCALE
        draw.line((x, y, x, y - length), fill=WHITE, width=2 * SCALE)

    layer = layer.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
    themed = layer
    static = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), BACKGROUND)
    static.alpha_composite(themed)
    return static, themed


def save_png(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="PNG", optimize=True, compress_level=9)


def write_xml(root: ET.Element, destination: Path) -> None:
    ET.indent(root, space="  ")
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(destination, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping-xml", required=True, type=Path)
    args = parser.parse_args()

    mapping_file = args.mapping_xml.resolve()
    if not mapping_file.is_file():
        raise SystemExit(f"Lawnicons mapping XML not found: {mapping_file}")

    source_root = ET.parse(mapping_file).getroot()
    source_items = [
        item for item in source_root.iter("item")
        if item.get("component") and item.get("drawable")
    ]
    if len(source_items) < MIN_MAPPINGS:
        raise SystemExit(
            f"Lawnicons mapping has only {len(source_items)} app entries; "
            f"at least {MIN_MAPPINGS} are required."
        )

    drawable_to_data: dict[str, tuple[str, str, str]] = {}
    component_to_drawable: dict[str, tuple[str, str]] = {}
    package_to_drawable: dict[str, str] = {}

    for item in source_items:
        original_drawable = item.attrib["drawable"].removeprefix("@drawable/")
        drawable = resource_name(original_drawable)
        component = item.attrib["component"].strip()
        label = item.attrib.get("name", original_drawable).strip()
        package = component_package(component)

        previous = drawable_to_data.get(drawable)
        if previous and previous[0] != original_drawable:
            suffix = hashlib.sha1(original_drawable.encode("utf-8")).hexdigest()[:8]
            drawable = f"{drawable[:110]}_{suffix}"

        drawable_to_data[drawable] = (original_drawable, label, package or "")
        component_to_drawable[component] = (drawable, label)
        if package:
            package_to_drawable.setdefault(package, drawable)

    if len(component_to_drawable) < MIN_MAPPINGS:
        raise SystemExit(
            f"Only {len(component_to_drawable)} component mappings were parsed."
        )

    drawable_dir = PACK / "drawable-nodpi"
    drawable_dir.mkdir(parents=True, exist_ok=True)

    for drawable, (_, label, package) in sorted(drawable_to_data.items()):
        static_icon, themed_icon = draw_icon(label, package, drawable)
        save_png(static_icon, drawable_dir / f"{drawable}.png")
        save_png(themed_icon, drawable_dir / f"themed_{drawable}.png")

    appfilter = ET.Element("resources")
    for component, (drawable, label) in sorted(component_to_drawable.items()):
        ET.SubElement(appfilter, "item", {
            "component": component, "drawable": drawable, "name": label
        })
    write_xml(appfilter, PACK / "xml" / "appfilter.xml")
    write_xml(appfilter, ROOT / "pack-nothing" / "src" / "main" / "assets" / "appfilter.xml")

    drawable_index = ET.Element("resources")
    for drawable, (_, label, _) in sorted(drawable_to_data.items()):
        ET.SubElement(drawable_index, "item", {"drawable": drawable, "name": label})
    write_xml(drawable_index, PACK / "xml" / "drawable.xml")

    themed_map = ET.Element("icons")
    for package, drawable in sorted(package_to_drawable.items()):
        ET.SubElement(themed_map, "icon", {
            "package": package, "drawable": f"@drawable/themed_{drawable}"
        })
    write_xml(themed_map, PACK / "xml" / "grayscale_icon_map.xml")

    print(f"NOTHINK_APP_MAPPINGS={len(component_to_drawable)}")
    print(f"NOTHINK_UNIQUE_ORIGINAL_ARTWORK={len(drawable_to_data)}")
    print(f"NOTHINK_THEMED_PACKAGES={len(package_to_drawable)}")
    print("NOTHINK_UPSTREAM_SVG_USED=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"NOTHINK_GENERATION_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
