#!/usr/bin/env python3
"""Import pinned Lawnicons SVG artwork as compact Nothing-dark icon-pack assets."""
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg

ANDROID = "{http://schemas.android.com/apk/res/android}"

def safe_name(value):
    value = re.sub(r"[^a-z0-9_]", "_", value.lower())
    return value if value and value[0].isalpha() else "icon_" + value

def white_svg(source):
    source = re.sub(r"""(["'])(?:#000(?:000)?|#111(?:111)?|black)(["'])""",
                    r"\1#ffffff\2", source, flags=re.IGNORECASE)
    source = re.sub(r"""(fill|stroke)=(['"])currentColor\2""",
                    r'\1="#ffffff"', source, flags=re.IGNORECASE)
    return source.replace("currentColor", "#ffffff").encode("utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--module", type=Path, default=Path("pack-nothink2"))
    parser.add_argument("--minimum", type=int, default=100)
    args = parser.parse_args()
    root = args.upstream
    svgs = root / "svgs"
    source_filter = root / "app/assets/appfilter.xml"
    if not svgs.is_dir() or not source_filter.is_file():
        raise SystemExit("Pinned Lawnicons source archive is incomplete")

    res = args.module / "src/main/res"
    glyphs, wrappers, xml = (res / "drawable-nodpi", res / "drawable", res / "xml")
    for folder in (glyphs, wrappers, xml):
        folder.mkdir(parents=True, exist_ok=True)

    ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
    source = ET.parse(source_filter).getroot()
    appfilter, drawable_list, themed = ET.Element("resources"), ET.Element("resources"), ET.Element("icons")
    done, packages = set(), set()
    count = 0
    for item in source.findall("item"):
        component, drawable = item.get("component"), item.get("drawable")
        if not component or not drawable:
            continue
        name = safe_name(drawable)
        svg = svgs / (drawable + ".svg")
        if not svg.is_file():
            continue
        cairosvg.svg2png(bytestring=white_svg(svg.read_text(encoding="utf-8")),
                         write_to=str(glyphs / (name + "_glyph.png")),
                         output_width=256, output_height=256)
        if name not in done:
            layer = ET.Element("layer-list")
            bg_item = ET.SubElement(layer, "item")
            bg_shape = ET.SubElement(bg_item, "shape", {ANDROID + "shape": "rectangle"})
            ET.SubElement(bg_shape, "solid", {ANDROID + "color": "#101010"})
            fg_item = ET.SubElement(layer, "item", {
                ANDROID + "width": "176dp", ANDROID + "height": "176dp",
                ANDROID + "gravity": "center"})
            ET.SubElement(fg_item, "bitmap", {
                ANDROID + "src": "@drawable/" + name + "_glyph",
                ANDROID + "gravity": "center", ANDROID + "filter": "true"})
            ET.ElementTree(layer).write(wrappers / (name + ".xml"),
                                        encoding="utf-8", xml_declaration=True)
            ET.SubElement(drawable_list, "item", {"drawable": name})
            done.add(name)
        ET.SubElement(appfilter, "item", {"component": component, "drawable": name})
        match = re.search(r"ComponentInfo\{([^/]+)/", component)
        if match and match.group(1) not in packages:
            package = match.group(1)
            ET.SubElement(themed, "icon", {
                "package": package, "drawable": "@drawable/" + name + "_glyph"})
            packages.add(package)
        count += 1

    if count < args.minimum:
        raise SystemExit(f"Only {count} app mappings had matching SVGs; expected {args.minimum}")
    ET.SubElement(appfilter, "iconback", {"img": "icon_background"})
    ET.SubElement(appfilter, "scale", {"factor": "0.72"})
    for element, filename in ((appfilter, "appfilter.xml"),
                              (drawable_list, "drawable.xml"),
                              (themed, "grayscale_icon_map.xml")):
        ET.ElementTree(element).write(xml / filename, encoding="utf-8", xml_declaration=True)
    print(f"Imported {count} mapped components, {len(done)} unique SVGs, {len(packages)} themed packages")

if __name__ == "__main__":
    main()
