#!/usr/bin/env python3
"""Import the supplied HKtorito Jelly Bean archives and generate Holokat mappings."""
from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
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


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def resource_name(filename: str) -> str:
    stem = Path(filename).stem.lower()
    stem = re.sub(r"[^a-z0-9_]+", "_", stem)
    stem = re.sub(r"_+", "_", stem).strip("_")
    if not stem or not stem[0].isalpha():
        stem = "icon_" + (stem or "unnamed")
    return stem[:90]


# Explicit label-to-artwork aliases. Exact filename matches always take priority.
ALIASES = {
    "googlechrome": "chrome",
    "chromebrowser": "chrome",
    "googlechromebeta": "chromebeta",
    "googlechromedev": "chromedev",
    "googlechromecanary": "chromecanary",
    "chromiumbrowser": "chromium",
    "googlecalendar": "calendar",
    "androidcalendar": "calendar",
    "googlecamera": "cameragoogle",
    "gcam": "cameragoogle",
    "googlemessages": "messaging",
    "androidmessages": "messaging",
    "googlephone": "phone",
    "googledialer": "phone",
    "googlemail": "gmail",
    "googlemaps": "maps",
    "googlemapsgo": "mapsgo",
    "googlephotos": "photos",
    "googleplaystore": "playstore",
    "googleplaymusic": "playmusic",
    "googleplaygames": "playgames",
    "googleplaybooks": "playbooks",
    "googleplaymovies": "playmoviestv",
    "googlekeep": "keep",
    "googledrive": "drive",
    "googledocs": "docs",
    "googlesheets": "sheets",
    "googleslides": "slides",
    "googletranslate": "translate",
    "googleyoutube": "youtube",
    "microsoftoutlook": "outlook",
    "outlookmail": "outlook",
    "androidsettings": "settings",
    "aospbrowser": "browser",
    "aospcalculator": "calculator",
    "aospclock": "clock",
    "aospcamera": "camera",
    "aospdownloads": "downloads",
    "aospmusic": "music",
    "filesbygoogle": "filesgo",
    "googlefiles": "filesgo",
    "googlegmail": "gmail",
    "googledocsviewer": "docs",
    "googlecontacts": "contacts",
    "googlevoice": "voice",
    "googleassistant": "assistant",
    "googlemapsnavigation": "navigation",
    "googleearth": "earth",
    "googlefit": "fit",
    "googletranslatecamera": "translatecamera",
    "googlenews": "newsweather",
    "googlekeepnotes": "keep",
    "googlewallet": "wallet",
    "googletv": "googletv",
    "playstore": "playstore",
    "playmusic": "playmusic",
    "playgames": "playgames",
    "playbooks": "playbooks",
    "playmovies": "playmoviestv",
    "androidbeam": "androidbeam",
    "androidtv": "androidtvhome",
    "androidwear": "wear",
    "wearos": "wearos",
    "youtube": "youtube",
    "youtubeandroidtv": "youtubetv",
    "youtubeforandroidtv": "youtubetv",
    "youtubecreatorstudio": "youtubecreatorstudio",
    "youtubemusic": "youtubemusic",
    "youtubekids": "youtubekids",
    "facebookmessenger": "facebookmessenger",
    "messenger": "facebookmessenger",
    "instagramlite": "instagram",
    "whatsappbusiness": "whatsapp",
    "googleplus": "google",
    "google+": "google",
    "gplus": "google",
    "hangoutsdialer": "hangoutsdialer",
    "hangoutsdialer": "hangoutsdialer",
    "gmailgo": "gmailgo",
    "googlego": "googlego",
    "googlenow": "googlenow",
    "googleio": "googleio",
    "google settings": "googlesettings",
    "googlewallet": "wallet",
    "adwords": "adwords",
    "adwordsexpress": "adwordsexpress",
    "androidautolauncher": "androidauto",
    "chromecastbuiltin": "chromecastbuiltin",
    "chromecast": "chromecast",
    "cloudprint": "cloudprint",
    "cloudsearch": "cloudsearch",
    "fmradio": "fmradio",
    "filemanager": "filemanager",
    "findmydevice": "findmydevice",
    "quickoffice": "quickoffice",
    "voiceaccess": "voiceaccess",
    "voicesearch": "voicesearch",
    "voicedialer": "voicedialer",
    "soundrecorder": "soundrecorder",
    "videoplayer": "videos",
    "movieditor": "moviestudio",
    "moviestudio": "moviestudio",
    "email": "email",
    "mail": "mail",
    "browser": "browser",
    "calculator": "calculator",
    "calendar": "calendar",
    "camera": "camera",
    "clock": "clock",
    "contacts": "contacts",
    "downloads": "downloads",
    "messages": "messaging",
    "music": "music",
    "phone": "phone",
    "gallery": "gallery",
    "settings": "settings",
    "files": "files",
    "maps": "maps",
    "translate": "translate",
    "youtube": "youtube",
    "photos": "photos",
    "gmail": "gmail",
    "drive": "drive",
    "chrome": "chrome",
    "keep": "keep",
    "docs": "docs",
    "sheets": "sheets",
    "slides": "slides",
    "skype": "skype",
    "spotify": "spotify",
    "whatsapp": "whatsapp",
    "facebook": "facebook",
    "instagram": "instagram",
    "snapchat": "snapchat",
    "twitter": "twitter",
    "telegram": "telegram",
    "dropbox": "dropbox",
    "outlook": "outlook",
    "pinterest": "pinterest",
    "soundcloud": "soundcloud",
    "viber": "viber",
    "discord": "discord",
    "tiktok": "tiktok",
}


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

    for name, (data, original_path) in images.items():
        extension = Path(original_path).suffix.lower()
        (DRAWABLE_DIR / f"{name}{extension}").write_bytes(data)

    resources = ET.Element("resources")
    ET.SubElement(resources, "item", {"drawable": "ic_pack", "name": "holokat_pack"})
    for name in sorted(images):
        ET.SubElement(resources, "item", {"drawable": name, "name": name})
    ET.indent(resources, space="    ")
    DRAWABLE_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(resources, encoding="unicode") + "\n",
        encoding="utf-8",
    )

    artwork_by_label: dict[str, str] = {}
    artwork_by_label_and_path: dict[str, str] = {}
    for resource, (_, original_path) in images.items():
        label = normalize(Path(original_path).stem)
        artwork_by_label.setdefault(label, resource)
        artwork_by_label_and_path[label] = resource

    old_filter = ROOT / "pack-kitkat/src/main/res/xml/appfilter.xml"
    appfilter = ET.Element("resources")
    matched_components: set[str] = set()
    matched_artwork: Counter[str] = Counter()
    matched_labels: dict[str, set[str]] = defaultdict(set)
    unmatched_labels: set[str] = set()

    if old_filter.is_file():
        old_root = ET.parse(old_filter).getroot()
        for item in old_root.findall("item"):
            component = item.attrib.get("component")
            label = item.attrib.get("name", "")
            if not component or component in matched_components:
                continue

            normalized = normalize(label)
            resource = artwork_by_label.get(normalized)
            if resource is None:
                alias = ALIASES.get(normalized)
                if alias:
                    resource = artwork_by_label.get(normalize(alias))

            if resource is None:
                unmatched_labels.add(label)
                continue

            ET.SubElement(appfilter, "item", {
                "component": component,
                "drawable": resource,
                "name": label,
            })
            matched_components.add(component)
            matched_artwork[resource] += 1
            matched_labels[resource].add(label)

    ET.indent(appfilter, space="    ")
    APPFILTER_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(appfilter, encoding="unicode") + "\n",
        encoding="utf-8",
    )

    print(f"Holokat imported {len(images)} unique image assets from {len(ARCHIVES)} archives.")
    print(f"Generated {len(appfilter.findall('item'))} unique launcher component mappings.")
    print(f"Artwork used by mappings: {len(matched_artwork)} / {len(images)}.")
    print(f"Unmatched app labels: {len(unmatched_labels)}.")
    for resource, count in sorted(matched_artwork.items(), key=lambda entry: (-entry[1], entry[0])):
        labels = ", ".join(sorted(matched_labels[resource]))
        print(f"  {resource}: {count} components [{labels}]")
    if unmatched_labels:
        print("Unmatched labels: " + " | ".join(sorted(unmatched_labels)))
    print("Archive artwork is retained without redrawing or recoloring.")


if __name__ == "__main__":
    main()
