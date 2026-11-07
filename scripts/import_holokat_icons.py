#!/usr/bin/env python3
"""Import the two supplied HKtorito Jelly Bean archives into the Holokat APK module."""
from __future__ import annotations

import hashlib
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = [
    ROOT / "references/kitkat-archives/Icons jb 1.zip",
    ROOT / "references/kitkat-archives/icons jb2.zip",
]
RES = ROOT / "pack-holokat/src/main/res"
DRAWABLE_DIR = RES / "drawable-nodpi"
DRAWABLE_XML = RES / "xml/drawable.xml"
APPFILTER_XML = RES / "xml/appfilter.xml"
IMAGE_EXTENSIONS = {".png", ".webp", ".jpg", ".jpeg"}
ANDROID_NS = "http://schemas.android.com/apk/res/android"


def resource_name(filename: str) -> str:
    stem = Path(filename).stem.lower()
    stem = re.sub(r"[^a-z0-9_]+", "_", stem)
    stem = re.sub(r"_+", "_", stem).strip("_")
    if not stem or not stem[0].isalpha():
        stem = "icon_" + (stem or "unnamed")
    return stem[:90]


def main() -> None:
    missing = [str(path) for path in ARCHIVES if not path.is_file()]
    if missing:
        raise SystemExit("Missing Holokat source archive(s): " + ", ".join(missing))

    DRAWABLE_DIR.mkdir(parents=True, exist_ok=True)
    for old in DRAWABLE_DIR.iterdir():
        if old.is_file():
            old.unlink()

    images: dict[str, tuple[bytes, str]] = {}
    hashes: set[str] = set()
    for archive in ARCHIVES:
        with zipfile.ZipFile(archive) as zf:
            for info in zf.infolist():
                if info.is_dir() or Path(info.filename).suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                data = zf.read(info)
                digest = hashlib.sha256(data).hexdigest()
                if digest in hashes:
                    continue
                hashes.add(digest)
                base = resource_name(Path(info.filename).name)
                name = base
                suffix = 2
                while name in images:
                    name = f"{base}_{suffix}"
                    suffix += 1
                images[name] = (data, info.filename)

    if not images:
        raise SystemExit("No supported image files found in Holokat archives.")

    for name, (data, _) in images.items():
        (DRAWABLE_DIR / f"{name}{Path(images[name][1]).suffix.lower()}").write_bytes(data)

    resources = ET.Element("resources")
    ET.SubElement(resources, "item", {"drawable": "ic_pack", "name": "holokat_pack"})
    for name in sorted(images):
        ET.SubElement(resources, "item", {"drawable": name, "name": name})
    ET.indent(resources, space="    ")
    DRAWABLE_XML.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(resources, encoding="unicode") + "\n", encoding="utf-8")

    # Reuse only known component-to-icon mappings from the existing KitKat pack
    # where the Jelly Bean archive contains the same app-name artwork.
    known = {
        "phone": "phone", "contacts": "contacts", "people": "contacts",
        "messaging": "messages", "messages": "messages", "calendar": "calendar",
        "google_calendar": "calendar", "clock": "clock", "calculator": "calculator",
        "camera": "camera", "camera_google": "camera", "downloads": "downloads",
        "browser": "browser", "chromium": "browser", "email": "mail",
        "gmail": "mail", "music": "music", "play_music": "music",
    }
    available = {name.lower(): name for name in images}
    chosen = {key: available[value] for key, value in known.items() if value in available}
    old_filter = ROOT / "pack-kitkat/src/main/res/xml/appfilter.xml"
    appfilter = ET.Element("resources")
    if old_filter.is_file() and chosen:
        old_root = ET.parse(old_filter).getroot()
        for item in old_root.findall("item"):
            component = item.attrib.get("component")
            drawable = item.attrib.get("drawable", "").lower()
            replacement = chosen.get(drawable)
            if component and replacement:
                ET.SubElement(appfilter, "item", {"component": component, "drawable": replacement})
    ET.indent(appfilter, space="    ")
    APPFILTER_XML.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(appfilter, encoding="unicode") + "\n", encoding="utf-8")

    print(f"Holokat imported {len(images)} unique image assets from {len(ARCHIVES)} archives.")
    print(f"Generated {len(appfilter.findall('item'))} verified inherited launcher component mappings.")
    print("Archive artwork is retained without redrawing or recoloring.")


if __name__ == "__main__":
    main()
