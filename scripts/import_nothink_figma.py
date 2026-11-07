#!/usr/bin/env python3
"""Import app-specific artwork rendered directly from the committed Figma file."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ANDROID = "{http://schemas.android.com/apk/res/android}"


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def app_package(component: str) -> str:
    match = re.fullmatch(r"ComponentInfo\{([^/]+)/[^}]+\}", component.strip())
    return match.group(1) if match else ""


def make_mask(source: Image.Image) -> Image.Image:
    image = source.convert("RGBA")
    rgb = image.convert("RGB")
    alpha = image.getchannel("A")
    corners = [rgb.getpixel((x, y)) for x, y in (
        (0, 0), (rgb.width - 1, 0), (0, rgb.height - 1), (rgb.width - 1, rgb.height - 1)
    )]
    background = tuple(round(sum(pixel[i] for pixel in corners) / 4) for i in range(3))
    bg = Image.new("RGB", rgb.size, background)
    diff = ImageChops.difference(rgb, bg).convert("L")
    # Transparent Figma exports already carry their silhouette in alpha.
    if alpha.getextrema()[0] < 255:
        diff = ImageChops.multiply(diff, alpha)
    else:
        diff = diff.point(lambda value: 0 if value < 18 else min(255, round((value - 18) * 1.25)))
    bbox = diff.getbbox()
    if bbox is None:
        raise ValueError("rendered node has no visible foreground against its canvas")
    glyph = Image.new("RGBA", diff.size, (255, 255, 255, 0))
    glyph.putalpha(diff)
    glyph = glyph.crop(bbox)
    glyph.thumbnail((138, 138), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (192, 192), (255, 255, 255, 0))
    canvas.alpha_composite(glyph, ((192 - glyph.width) // 2, (192 - glyph.height) // 2))
    return canvas


def xml_write(root: ET.Element, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exports", type=Path, default=Path("build/nothink-figma-export"))
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--res", type=Path, default=Path("pack-nothing/src/main/res"))
    parser.add_argument("--minimum", type=int, default=1)
    args = parser.parse_args()

    manifest_path = args.exports / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_items = ET.parse(args.mapping).getroot().findall("item")
    by_name: dict[str, list[ET.Element]] = {}
    for item in source_items:
        component = item.get("component", "")
        drawable = item.get("drawable", "").removeprefix("@drawable/")
        label = item.get("name", drawable)
        for alias in (label, drawable, app_package(component)):
            key = norm(alias)
            if key:
                by_name.setdefault(key, []).append(item)

    image_dir = args.exports
    selected: dict[str, tuple[Image.Image, str, list[ET.Element]]] = {}
    unmatched = []
    for node in manifest.get("icons", []):
        key = norm(node.get("name", ""))
        matches = by_name.get(key, [])
        # Multiple launcher activities for one app are expected; distinct packages are not.
        packages = {app_package(item.get("component", "")) for item in matches}
        if not matches or len(packages) != 1:
            unmatched.append({"node": node.get("name"), "reason": "no exact unique app identity match"})
            continue
        package = next(iter(packages))
        if package in selected:
            continue
        file_path = image_dir / node["file"]
        try:
            mask = make_mask(Image.open(file_path))
        except Exception as error:
            unmatched.append({"node": node.get("name"), "reason": str(error)})
            continue
        selected[package] = (mask, node.get("name", ""), matches)

    drawable_dir = args.res / "drawable-nodpi"
    wrapper_dir = args.res / "drawable"
    xml_dir = args.res / "xml"
    drawable_dir.mkdir(parents=True, exist_ok=True)
    wrapper_dir.mkdir(parents=True, exist_ok=True)
    xml_dir.mkdir(parents=True, exist_ok=True)

    component_map = {}
    package_map = {}
    unique_art = {}
    imported = []
    for package, (mask, label, items) in sorted(selected.items()):
        digest = hashlib.sha256(mask.tobytes()).hexdigest()
        art_name = unique_art.get(digest)
        if art_name is None:
            art_name = "figma_" + digest[:16]
            mask.save(drawable_dir / f"{art_name}.webp", "WEBP", lossless=True, quality=100, method=6)
            unique_art[digest] = art_name
        package_drawable = "fig_" + hashlib.sha1(package.encode()).hexdigest()[:12]
        package_map[package] = package_drawable
        ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
        alias = ET.Element("bitmap", {ANDROID + "src": f"@drawable/{art_name}", ANDROID + "gravity": "center"})
        xml_write(alias, wrapper_dir / f"{package_drawable}.xml")
        layer = ET.Element("layer-list")
        bg_item = ET.SubElement(layer, "item")
        shape = ET.SubElement(bg_item, "shape", {ANDROID + "shape": "rectangle"})
        ET.SubElement(shape, "solid", {ANDROID + "color": "#FF000000"})
        ET.SubElement(layer, "item", {ANDROID + "drawable": f"@drawable/{package_drawable}"})
        xml_write(layer, wrapper_dir / f"icon_{package_drawable}.xml")
        for item in items:
            component = item.get("component", "")
            if component:
                component_map[component] = (f"icon_{package_drawable}", label)
        imported.append({"figma_name": label, "package": package, "drawable": package_drawable, "components": len(items), "artwork_sha256": digest})

    appfilter = ET.Element("resources")
    for component, (drawable, _) in sorted(component_map.items()):
        ET.SubElement(appfilter, "item", {"component": component, "drawable": drawable})
    xml_write(appfilter, xml_dir / "appfilter.xml")

    drawable_index = ET.Element("resources")
    for package, drawable in sorted(package_map.items()):
        ET.SubElement(drawable_index, "item", {"drawable": f"icon_{drawable}"})
    xml_write(drawable_index, xml_dir / "drawable.xml")

    themed = ET.Element("icons")
    for package, drawable in sorted(package_map.items()):
        ET.SubElement(themed, "icon", {"package": package, "drawable": f"@drawable/{drawable}"})
    xml_write(themed, xml_dir / "grayscale_icon_map.xml")

    report = {
        "source": manifest.get("source"),
        "figma_nodes_rendered": manifest.get("renderedNodes", 0),
        "mapped_applications": len(imported),
        "unique_artworks": len(unique_art),
        "launcher_component_mappings": len(component_map),
        "unmatched_nodes": unmatched,
        "imported": imported,
    }
    report_dir = Path("build/nothink-figma-report")
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"NOTHINK_FIGMA_MAPPED_APPS={len(imported)}")
    print(f"NOTHINK_FIGMA_UNIQUE_ARTWORKS={len(unique_art)}")
    print(f"NOTHINK_FIGMA_COMPONENT_MAPPINGS={len(component_map)}")
    if len(imported) < args.minimum:
        raise SystemExit(f"Only {len(imported)} Figma artworks matched app identities; minimum is {args.minimum}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
