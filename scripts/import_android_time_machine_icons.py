#!/usr/bin/env python3
"""Restore only the Android 4.4.4 application icons from Android Time Machine.

This runs after the legacy archive importers so density-specific or Jelly Bean
artwork cannot override the selected KitKat application icons.
"""
from __future__ import annotations

import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "pack-kitkat" / "src" / "main" / "res"
DRAWABLES_XML = RES / "xml" / "drawable.xml"
APPFILTER_XML = RES / "xml" / "appfilter.xml"

SOURCE_COMMIT = "13f36d7aff0503f99e2997b461c6e5d91e6ef4ab"
SOURCE_BASE = (
    "https://raw.githubusercontent.com/szabolevi98/android-time-machine/"
    f"{SOURCE_COMMIT}/versions/4.4.4/assets"
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"

# Android Time Machine 4.4.4 application artwork only.
# Resource name -> exact original asset filename.
ICONS = {
    "apps": "apps.png",
    "browser": "earth.png",
    "calculator": "calculator.png",
    "calendar": "calendar.png",
    "camera": "camera.png",
    "chrome": "chrome.png",
    "clock": "clock.png",
    "downloads": "downloads.png",
    "drive": "drive.png",
    "mail": "email.png",
    "gallery": "gallery.png",
    "gmail": "gmail.png",
    "google_plus": "google-plus.png",
    "google_search": "google-search.png",
    "google_settings": "google-settings.png",
    "hangouts": "hangouts.png",
    "keep": "keep.png",
    "maps": "maps.png",
    "news_weather": "news-weather.png",
    "newsstand": "newsstand.png",
    "contacts": "people.png",
    "phone": "phone.png",
    "photos": "photos.png",
    "play_books": "play-books.png",
    "play_games": "play-games.png",
    "play_movies": "play-movies.png",
    "play_music": "play-music.png",
    "quickoffice": "quickoffice.png",
    "settings": "settings.png",
    "voice_search": "voice-search.png",
    "wallet": "wallet.png",
    "youtube": "youtube.png",
}

WALLPAPER_FILENAME = "aosp-wallpaper.jpg"
WALLPAPER_RESOURCE = "kitkat_wallpaper"

# Labels in appfilter.xml -> original KitKat artwork resource.
LABEL_RULES = (
    (("googleplus", "google+"), "google_plus"),
    (("google news", "googlenews", "news"), "news_weather"),
    (("newsstand", "playnewsstand", "magazines"), "newsstand"),
    (("googlesearch", "search"), "google_search"),
    (("googlesettings", "google settings"), "google_settings"),
    (("hangouts", "talk"), "hangouts"),
    (("keep", "notes"), "keep"),
    (("newsweather", "weather"), "news_weather"),
    (("photos",), "photos"),
    (("playbooks", "books"), "play_books"),
    (("playgames", "games"), "play_games"),
    (("playmovies", "movies", "google tv", "googletv"), "play_movies"),
    (("playmusic", "youtube music", "youtubemusic"), "play_music"),
    (("quickoffice", "google docs", "googledocs", "google sheets", "googlesheets", "google slides", "googleslides"), "quickoffice"),
    (("voicesearch", "voice search", "google assistant"), "voice_search"),
    (("wallet", "google wallet"), "wallet"),
    (("chrome",), "chrome"),
    (("youtube",), "youtube"),
    (("calculator", "calcu"), "calculator"),
    (("calendar",), "calendar"),
    (("camera",), "camera"),
    (("clock", "alarmclock", "deskclock"), "clock"),
    (("download", "files", "file manager", "filemanager", "documentsui"), "downloads"),
    (("browser", "webbrowser"), "browser"),
    (("gmail",), "gmail"),
    (("email", "mail", "outlook"), "mail"),
    (("drive",), "drive"),
    (("google photos", "googlephotos"), "photos"),
    (("gallery", "aosp gallery"), "gallery"),
    (("maps", "map", "navigation"), "maps"),
    (("google drive", "googledrive"), "drive"),
    (("google keep", "googlekeep"), "keep"),
    (("contacts", "contact", "people"), "contacts"),
    (("phone", "dialer", "calling", "call"), "phone"),
    (("settings", "setting", "configuration"), "settings"),
)


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9+]+", "", value.casefold())


def resource_for_label(label: str) -> str | None:
    normalized = normalize(label)
    for tokens, resource in LABEL_RULES:
        if any(normalize(token) in normalized for token in tokens):
            return resource
    return None


def download_icon(filename: str) -> bytes:
    url = f"{SOURCE_BASE}/{filename}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "Insomdroid-KitKat-Icon-Importer/1.0"}
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"Source is not a PNG image: {url}")
    return data


def main() -> None:
    destination_dir = RES / "drawable-nodpi"
    destination_dir.mkdir(parents=True, exist_ok=True)

    imported: list[tuple[str, str, int, str]] = []
    for resource, filename in ICONS.items():
        data = download_icon(filename)

        # Remove competing density-specific images and vector XML resources.
        # Keeping one nodpi source guarantees the same KitKat artwork at every
        # screen density instead of allowing older archive artwork to win.
        for directory in RES.glob("drawable*"):
            if not directory.is_dir() or directory == destination_dir:
                continue
            for extension in (".png", ".webp", ".jpg", ".jpeg", ".xml"):
                candidate = directory / f"{resource}{extension}"
                if candidate.is_file():
                    candidate.unlink()

        destination = destination_dir / f"{resource}.png"
        destination.write_bytes(data)
        imported.append((resource, filename, len(data), hashlib.sha256(data).hexdigest()))

    # Include the official Android 4.4.4 wallpaper in the pack app preview.
    wallpaper_url = f"{SOURCE_BASE}/{WALLPAPER_FILENAME}"
    wallpaper_request = urllib.request.Request(
        wallpaper_url, headers={"User-Agent": "Insomdroid-KitKat-Icon-Importer/1.0"}
    )
    with urllib.request.urlopen(wallpaper_request, timeout=45) as response:
        wallpaper_data = response.read()
    if not wallpaper_data.startswith(JPEG_SIGNATURE):
        raise ValueError(f"Source is not a JPEG wallpaper: {wallpaper_url}")
    (destination_dir / f"{WALLPAPER_RESOURCE}.jpg").write_bytes(wallpaper_data)
    print(f"WALLPAPER {WALLPAPER_RESOURCE} <- {WALLPAPER_FILENAME} ({len(wallpaper_data)} bytes)")

    # Register newly imported source icons for launchers that enumerate the
    # drawable catalogue. Existing mappings and unrelated artwork are retained.
    drawable_root = (
        ET.parse(DRAWABLES_XML).getroot()
        if DRAWABLES_XML.is_file()
        else ET.Element("resources")
    )
    existing = {item.attrib.get("name") for item in drawable_root.findall("item")}
    for resource in ICONS:
        if resource not in existing:
            ET.SubElement(drawable_root, "item", {"drawable": resource, "name": resource})
    ET.indent(drawable_root, space="  ")
    DRAWABLES_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(drawable_root, encoding="unicode")
        + "\n",
        encoding="utf-8",
    )

    # Keep the existing component catalogue but point matching stock-app
    # labels to the exact KitKat assets imported above.
    appfilter_root = ET.parse(APPFILTER_XML).getroot()
    remapped = 0
    for item in appfilter_root.findall("item"):
        resource = resource_for_label(item.attrib.get("name", ""))
        if resource is not None:
            item.set("drawable", resource)
            remapped += 1
    ET.indent(appfilter_root, space="  ")
    APPFILTER_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(appfilter_root, encoding="unicode")
        + "\n",
        encoding="utf-8",
    )

    print(f"Imported {len(imported)} original Android 4.4.4 app icons.")
    for resource, filename, size, digest in imported:
        print(f"ICON {resource} <- {filename} ({size} bytes, sha256={digest})")
    print(f"Remapped {remapped} existing appfilter entries to KitKat artwork.")


if __name__ == "__main__":
    main()
