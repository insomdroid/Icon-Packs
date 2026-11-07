#!/usr/bin/env python3
"""Generate original, semantic Nothink pictograms from app names and package IDs.

Lawnicons is read only for Android component mappings. No upstream artwork is read.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack-nothing" / "src" / "main" / "res"
ICON_SIZE = 192
SCALE = 3
CANVAS = ICON_SIZE * SCALE
MIN_MAPPINGS = 3000
BACKGROUND = (10, 12, 13, 255)
WHITE = (246, 247, 244, 255)
RED = (238, 45, 52, 255)
TRANSPARENT = (0, 0, 0, 0)
STROKE = 12 * SCALE

# Semantic families deliberately use pictograms, never generated initials.
RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("phone", ("phone", "dialer", "call", "telephony")),
    ("messages", ("message", "messaging", "sms", "chat", "signal", "telegram", "whatsapp", "messenger")),
    ("mail", ("mail", "email", "gmail", "outlook", "inbox")),
    ("camera", ("camera", "photos", "gallery", "lens")),
    ("browser", ("browser", "chrome", "firefox", "webview", "internet", "brave", "opera")),
    ("calendar", ("calendar", "agenda", "schedule")),
    ("clock", ("clock", "alarm", "timer", "stopwatch")),
    ("music", ("music", "audio", "spotify", "sound", "player", "podcast")),
    ("video", ("video", "movie", "youtube", "stream", "tv", "netflix")),
    ("maps", ("maps", "map", "navigation", "location", "gps")),
    ("weather", ("weather", "forecast", "climate", "meteo")),
    ("settings", ("settings", "config", "preferences", "control")),
    ("files", ("file", "folder", "document", "drive", "storage", "explorer")),
    ("download", ("download", "downloader", "transfer")),
    ("shopping", ("shop", "store", "market", "cart", "commerce", "amazon")),
    ("wallet", ("wallet", "bank", "payment", "finance", "money", "pay")),
    ("security", ("security", "privacy", "lock", "password", "auth", "vpn", "antivirus")),
    ("health", ("health", "fitness", "heart", "medical", "workout", "wellness")),
    ("education", ("education", "school", "learn", "book", "reader", "dictionary", "study")),
    ("games", ("game", "gaming", "arcade", "play")),
    ("social", ("social", "community", "forum", "reddit", "mastodon", "profile")),
    ("home", ("home", "launcher", "house", "smart home")),
    ("travel", ("travel", "flight", "airline", "hotel", "booking", "train")),
    ("food", ("food", "recipe", "restaurant", "kitchen", "delivery")),
    ("search", ("search", "find", "assistant", "discover")),
    ("contacts", ("contact", "people", "person", "address book")),
    ("calculator", ("calculator", "calc", "math")),
)

def classify(label: str, package: str, drawable: str) -> str:
    haystack = f"{label} {package} {drawable}".lower().replace("_", " ").replace(".", " ")
    for family, words in RULES:
        if any(word in haystack for word in words):
            return family
    return "abstract"


def resource_name(value: str) -> str:
    value = re.sub(r"[^a-z0-9_]+", "_", value.strip().lower())
    value = re.sub(r"_+", "_", value).strip("_")
    if not value or value[0].isdigit():
        value = "_" + (value or "icon")
    return value[:120]


def component_package(component: str) -> str | None:
    match = re.fullmatch(r"ComponentInfo\{([^/]+)/[^}]+\}", component.strip())
    return match.group(1) if match else None


def q(value: float) -> int:
    return int(round(value * SCALE))


def draw_symbol(draw: ImageDraw.ImageDraw, family: str, digest: bytes, include_accents: bool = True) -> None:
    """Draw a bold, legible 192dp pictogram on a 3x working canvas."""
    w = STROKE
    white = WHITE
    # All geometry stays inside a common optical box and uses a shared stroke.
    if family == "phone":
        draw.arc((q(43), q(40), q(149), q(151)), 35, 325, fill=white, width=w)
        draw.rounded_rectangle((q(42), q(39), q(68), q(75)), radius=q(9), fill=white)
        draw.rounded_rectangle((q(124), q(119), q(151), q(153)), radius=q(9), fill=white)
    elif family == "messages":
        draw.rounded_rectangle((q(34), q(42), q(158), q(132)), radius=q(25), outline=white, width=w)
        draw.polygon([(q(56),q(127)),(q(48),q(153)),(q(84),q(132))], fill=white)
        for x in (68, 96, 124):
            draw.ellipse((q(x-5),q(82-5),q(x+5),q(82+5)), fill=white)
    elif family == "mail":
        draw.rounded_rectangle((q(30), q(48), q(162), q(145)), radius=q(13), outline=white, width=w)
        draw.line([(q(37),q(58)),(q(96),q(106)),(q(155),q(58))], fill=white, width=w)
        draw.line([(q(39),q(135)),(q(78),q(101))], fill=white, width=w)
        draw.line([(q(153),q(135)),(q(114),q(101))], fill=white, width=w)
    elif family == "camera":
        draw.rounded_rectangle((q(29), q(53), q(163), q(145)), radius=q(18), outline=white, width=w)
        draw.rounded_rectangle((q(54), q(39), q(91), q(60)), radius=q(7), fill=white)
        draw.ellipse((q(72),q(70),q(120),q(118)), outline=white, width=w)
        draw.ellipse((q(88),q(86),q(104),q(102)), fill=white)
    elif family == "browser":
        draw.ellipse((q(35),q(35),q(157),q(157)), outline=white, width=w)
        draw.ellipse((q(69),q(35),q(123),q(157)), outline=white, width=w)
        draw.arc((q(35),q(60),q(157),q(132)), 0, 180, fill=white, width=w)
        draw.line((q(39),q(96),q(153),q(96)), fill=white, width=w)
    elif family == "calendar":
        draw.rounded_rectangle((q(34),q(43),q(158),q(151)), radius=q(14), outline=white, width=w)
        draw.line((q(35),q(76),q(157),q(76)), fill=white, width=w)
        for x in (65, 127):
            draw.line((q(x),q(31),q(x),q(58)), fill=white, width=w)
        for x in (66, 96, 126):
            for y in (99, 128):
                draw.rounded_rectangle((q(x-5),q(y-5),q(x+5),q(y+5)), radius=q(2), fill=white)
    elif family == "clock":
        draw.ellipse((q(34),q(34),q(158),q(158)), outline=white, width=w)
        draw.line((q(96),q(54),q(96),q(98),q(128),q(116)), fill=white, width=w)
        draw.ellipse((q(88),q(88),q(104),q(104)), fill=white)
    elif family == "music":
        draw.line((q(112),q(43),q(112),q(123)), fill=white, width=w)
        draw.line((q(112),q(43),q(151),q(53),q(151),q(130)), fill=white, width=w)
        draw.ellipse((q(45),q(112),q(91),q(151)), fill=white)
        draw.ellipse((q(106),q(118),q(151),q(156)), fill=white)
    elif family == "video":
        draw.rounded_rectangle((q(29),q(47),q(163),q(145)), radius=q(18), outline=white, width=w)
        draw.polygon([(q(79),q(69)),(q(79),q(123)),(q(127),q(96))], fill=white)
    elif family == "maps":
        draw.ellipse((q(54),q(34),q(138),q(118)), outline=white, width=w)
        draw.polygon([(q(56),q(94)),(q(96),q(160)),(q(136),q(94))], fill=white)
        draw.ellipse((q(82),q(62),q(110),q(90)), fill=TRANSPARENT)
    elif family == "weather":
        draw.ellipse((q(69),q(40),q(125),q(96)), outline=white, width=w)
        for angle in range(0,360,45):
            import math
            a = math.radians(angle)
            x1,y1 = 97+37*math.cos(a),68+37*math.sin(a)
            x2,y2 = 97+51*math.cos(a),68+51*math.sin(a)
            draw.line((q(x1),q(y1),q(x2),q(y2)), fill=white, width=w)
        draw.rounded_rectangle((q(34),q(101),q(158),q(145)), radius=q(22), fill=white)
        draw.ellipse((q(61),q(82),q(112),q(130)), fill=white)
        draw.rectangle((q(62),q(116),q(137),q(143)), fill=white)
    elif family == "settings":
        draw.ellipse((q(50),q(50),q(142),q(142)), outline=white, width=w)
        for angle in range(0,360,45):
            import math
            a=math.radians(angle)
            x1,y1=96+48*math.cos(a),96+48*math.sin(a)
            x2,y2=96+62*math.cos(a),96+62*math.sin(a)
            draw.line((q(x1),q(y1),q(x2),q(y2)), fill=white, width=w+q(2))
        draw.ellipse((q(82),q(82),q(110),q(110)), fill=white)
    elif family == "files":
        draw.rounded_rectangle((q(30),q(57),q(162),q(145)), radius=q(13), outline=white, width=w)
        draw.polygon([(q(34),q(57)),(q(34),q(43)),(q(83),q(43)),(q(98),q(58))], fill=white)
        draw.line((q(37),q(83),q(155),q(83)), fill=white, width=w)
    elif family == "download":
        draw.line((q(96),q(34),q(96),q(112)), fill=white, width=w+q(3))
        draw.line((q(65),q(83),q(96),q(116),q(127),q(83)), fill=white, width=w+q(3))
        draw.rounded_rectangle((q(37),q(125),q(155),q(151)), radius=q(9), outline=white, width=w)
    elif family == "shopping":
        draw.rounded_rectangle((q(42),q(67),q(150),q(151)), radius=q(12), outline=white, width=w)
        draw.arc((q(67),q(34),q(125),q(102)), 180, 360, fill=white, width=w)
    elif family == "wallet":
        draw.rounded_rectangle((q(31),q(51),q(161),q(145)), radius=q(16), outline=white, width=w)
        draw.rounded_rectangle((q(94),q(79),q(164),q(119)), radius=q(10), fill=white)
        draw.ellipse((q(109),q(92),q(120),q(103)), fill=TRANSPARENT)
    elif family == "security":
        points=[(q(96),q(31)),(q(151),q(53)),(q(143),q(111)),(q(96),q(157)),(q(49),q(111)),(q(41),q(53)),(q(96),q(31))]
        draw.line(points, fill=white, width=w, joint="curve")
        draw.line((q(69),q(94),q(88),q(113),q(126),q(73)), fill=white, width=w+q(2))
    elif family == "health":
        draw.ellipse((q(39),q(47),q(102),q(112)), fill=white)
        draw.ellipse((q(90),q(47),q(153),q(112)), fill=white)
        draw.polygon([(q(42),q(85)),(q(96),q(153)),(q(150),q(85))], fill=white)
        draw.line((q(54),q(98),q(78),q(98),q(89),q(77),q(105),q(119),q(119),q(98),q(139),q(98)), fill=TRANSPARENT, width=q(7))
    elif family == "education":
        draw.polygon([(q(30),q(49)),(q(88),q(60)),(q(96),q(70)),(q(104),q(60)),(q(162),q(49)),(q(162),q(145)),(q(104),q(155)),(q(96),q(163)),(q(88),q(155)),(q(30),q(145))], outline=white)
        draw.line((q(96),q(70),q(96),q(158)), fill=white, width=w)
        draw.line((q(47),q(80),q(78),q(86)), fill=white, width=w)
        draw.line((q(114),q(86),q(145),q(80)), fill=white, width=w)
    elif family == "games":
        draw.rounded_rectangle((q(30),q(59),q(162),q(137)), radius=q(32), outline=white, width=w)
        draw.line((q(60),q(98),q(88),q(98)), fill=white, width=w+q(2))
        draw.line((q(74),q(84),q(74),q(112)), fill=white, width=w+q(2))
        for x,y in ((126,88),(140,108)):
            draw.ellipse((q(x-6),q(y-6),q(x+6),q(y+6)), fill=white)
    elif family == "social":
        draw.ellipse((q(76),q(38),q(116),q(78)), fill=white)
        draw.ellipse((q(34),q(62),q(66),q(94)), fill=white)
        draw.ellipse((q(126),q(62),q(158),q(94)), fill=white)
        draw.rounded_rectangle((q(54),q(91),q(138),q(151)), radius=q(28), fill=white)
        draw.arc((q(20),q(88),q(80),q(145)), 180, 350, fill=white, width=w)
        draw.arc((q(112),q(88),q(172),q(145)), 190, 360, fill=white, width=w)
    elif family == "home":
        draw.polygon([(q(25),q(91)),(q(96),q(34)),(q(167),q(91))], outline=white)
        draw.line((q(43),q(82),q(43),q(153),q(149),q(153),q(149),q(82)), fill=white, width=w)
        draw.rounded_rectangle((q(81),q(106),q(111),q(153)), radius=q(5), outline=white, width=w)
    elif family == "travel":
        draw.polygon([(q(96),q(28)),(q(108),q(83)),(q(158),q(111)),(q(158),q(126)),(q(108),q(111)),(q(105),q(151)),(q(124),q(164)),(q(124),q(174)),(q(96),q(164)),(q(68),q(174)),(q(68),q(164)),(q(87),q(151)),(q(84),q(111)),(q(34),q(126)),(q(34),q(111)),(q(84),q(83))], fill=white)
    elif family == "food":
        draw.line((q(56),q(35),q(56),q(92)), fill=white, width=w)
        for x in (42,56,70):
            draw.line((q(x),q(35),q(x),q(70)), fill=white, width=w)
        draw.line((q(56),q(92),q(56),q(157)), fill=white, width=w)
        draw.ellipse((q(112),q(34),q(145),q(80)), outline=white, width=w)
        draw.line((q(128),q(80),q(128),q(157)), fill=white, width=w)
    elif family == "search":
        draw.ellipse((q(34),q(31),q(123),q(120)), outline=white, width=w+q(2))
        draw.line((q(111),q(109),q(158),q(156)), fill=white, width=w+q(4))
    elif family == "contacts":
        draw.ellipse((q(75),q(35),q(117),q(77)), fill=white)
        draw.rounded_rectangle((q(45),q(88),q(147),q(157)), radius=q(34), fill=white)
    elif family == "calculator":
        draw.rounded_rectangle((q(48),q(29),q(144),q(163)), radius=q(13), outline=white, width=w)
        draw.rounded_rectangle((q(63),q(43),q(129),q(76)), radius=q(5), fill=white)
        for x in (70,96,122):
            for y in (99,128):
                draw.ellipse((q(x-6),q(y-6),q(x+6),q(y+6)), fill=white)
    else:
        # Original abstract mark for apps without a reliable semantic label.
        # The arrangement is hash-varied but remains a consistent geometric family.
        mode = digest[0] % 4
        if mode == 0:
            draw.rounded_rectangle((q(43),q(43),q(149),q(149)), radius=q(22), outline=white, width=w)
            draw.ellipse((q(72),q(72),q(120),q(120)), fill=white)
        elif mode == 1:
            draw.polygon([(q(96),q(31)),(q(154),q(96)),(q(96),q(161)),(q(38),q(96))], outline=white)
            draw.ellipse((q(81),q(81),q(111),q(111)), fill=white)
        elif mode == 2:
            for x,y,r in ((67,67,17),(125,67,17),(96,119,22)):
                draw.ellipse((q(x-r),q(y-r),q(x+r),q(y+r)), fill=white)
        else:
            draw.line((q(43),q(143),q(43),q(49),q(149),q(49),q(149),q(143)), fill=white, width=w)
            draw.line((q(64),q(120),q(96),q(76),q(128),q(120)), fill=white, width=w)

    if include_accents:
        # A restrained red signal mark is used only in the full-colour artwork.
        # The themed layer remains strictly monochrome so Android can tint it.
        corner = digest[1] % 4
        red_dot = q(9)
        positions = ((q(147),q(45)),(q(45),q(45)),(q(147),q(147)),(q(45),q(147)))
        cx, cy = positions[corner]
        draw.ellipse((cx-red_dot,cy-red_dot,cx+red_dot,cy+red_dot), fill=RED)

        # Dot-matrix detail is part of the glyph, and is monochrome in both modes.
    rows = 2 + digest[2] % 2
    cols = 3
    for row in range(rows):
        for col in range(cols):
            if (digest[3 + row] >> col) & 1:
                x = q(68 + col * 12)
                y = q(169 + row * 7)
                draw.ellipse((x-q(1.5),y-q(1.5),x+q(1.5),y+q(1.5)), fill=white)


def render_icon(label: str, package: str, drawable: str) -> tuple[Image.Image, Image.Image, str]:
    identity = f"{package}|{drawable}|{label}"
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    family = classify(label, package, drawable)

    # Full-colour artwork: transparent symbol over the Nothink dark field.
    static_layer = Image.new("RGBA", (CANVAS, CANVAS), TRANSPARENT)
    draw_symbol(ImageDraw.Draw(static_layer), family, digest, include_accents=True)
    static_layer = static_layer.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
    static = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), BACKGROUND)
    static.alpha_composite(static_layer)

    # Themed artwork: no fixed background and no red pixels. Compatible launchers
    # can tint this single-colour alpha mask using wallpaper/system colours.
    themed = Image.new("RGBA", (CANVAS, CANVAS), TRANSPARENT)
    draw_symbol(ImageDraw.Draw(themed), family, digest, include_accents=False)
    themed = themed.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
    return static, themed, family


def save_webp(image: Image.Image, destination: Path) -> None:
    """Write lossless WebP artwork with exact RGBA pixels and transparency.

    Android supports WebP resources on the project's minimum API level. Lossless
    WebP avoids aapt's PNG crunch expansion while preserving the quantized artwork
    pixel-for-pixel, including transparent themed-icon backgrounds.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    indexed = image.convert("RGBA").quantize(
        colors=32,
        method=Image.Quantize.FASTOCTREE,
        dither=Image.Dither.NONE,
    )
    indexed.convert("RGBA").save(
        destination,
        format="WEBP",
        lossless=True,
        quality=100,
        method=6,
        exact=True,
    )


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
        package = component_package(component) or ""

        previous = drawable_to_data.get(drawable)
        if previous and previous[0] != original_drawable:
            suffix = hashlib.sha1(original_drawable.encode("utf-8")).hexdigest()[:8]
            drawable = f"{drawable[:110]}_{suffix}"

        drawable_to_data[drawable] = (original_drawable, label, package)
        component_to_drawable[component] = (drawable, label)
        if package:
            package_to_drawable.setdefault(package, drawable)

    if len(component_to_drawable) < MIN_MAPPINGS:
        raise SystemExit(f"Only {len(component_to_drawable)} component mappings were parsed.")

    drawable_dir = PACK / "drawable-nodpi"
    drawable_dir.mkdir(parents=True, exist_ok=True)
    families: Counter[str] = Counter()

    for drawable, (_, label, package) in sorted(drawable_to_data.items()):
        static_icon, themed_icon, family = render_icon(label, package, drawable)
        families[family] += 1
        save_webp(static_icon, drawable_dir / f"{drawable}.webp")
        save_webp(themed_icon, drawable_dir / f"themed_{drawable}.webp")

    appfilter = ET.Element("resources")
    for component, (drawable, _) in sorted(component_to_drawable.items()):
        ET.SubElement(appfilter, "item", {"component": component, "drawable": drawable})
    write_xml(appfilter, PACK / "xml" / "appfilter.xml")
    write_xml(appfilter, ROOT / "pack-nothing" / "src" / "main" / "assets" / "appfilter.xml")

    drawable_index = ET.Element("resources")
    for drawable in sorted(drawable_to_data):
        ET.SubElement(drawable_index, "item", {"drawable": drawable})
    write_xml(drawable_index, PACK / "xml" / "drawable.xml")

    themed_map = ET.Element("icons")
    for package, drawable in sorted(package_to_drawable.items()):
        ET.SubElement(themed_map, "icon", {
            "package": package, "drawable": f"@drawable/themed_{drawable}"
        })
    write_xml(themed_map, PACK / "xml" / "grayscale_icon_map.xml")

    print(f"NOTHINK_APP_MAPPINGS={len(component_to_drawable)}")
    print(f"NOTHINK_UNIQUE_PICTOGRAMS={len(drawable_to_data)}")
    print("NOTHINK_ARTWORK_STYLE=GEOMETRIC_SOLID")
    print("NOTHINK_LETTER_INITIALS_USED=0")
    print("NOTHINK_UPSTREAM_ARTWORK_USED=0")
    for family, count in sorted(families.items()):
        print(f"NOTHINK_FAMILY_{family.upper()}={count}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"NOTHINK_GENERATION_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
