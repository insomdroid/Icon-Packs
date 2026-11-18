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

WALLPAPERS = {
    "kitkat_wallpaper": "kk-default_wallpaper.jpg",
    "aosp_wallpaper": "aosp-wallpaper.jpg",
}

WIDGET_ASSETS = {
    "kitkat_music_background": "music-appwidget_bg.png",
    "kitkat_music_unknown": "music-albumart_mp_unknown.png",
    "kitkat_music_previous": "music-ic_media_previous.png",
    "kitkat_music_play": "music-ic_media_play.png",
    "kitkat_music_pause": "music-ic_media_pause.png",
    "kitkat_music_next": "music-ic_media_next.png",
    "kitkat_gallery_preview": "gallery-widget_preview.png",
    "kitkat_gallery_border": "gallery-appwidget_photo_border.png",
    "kitkat_power_background": "widget-power-bg.png",
    "kitkat_power_wifi_on": "power-wifi-on.png",
    "kitkat_power_bluetooth_on": "power-bluetooth-on.png",
    "kitkat_power_gps_on": "power-gps-on.png",
    "kitkat_power_sync_on": "power-sync-on.png",
    "kitkat_power_brightness_full": "power-brightness-full.png",
    "kitkat_search_icon": "google-search.png",
    "kitkat_voice_search": "kd-ic_voice_search.png",
    "kitkat_digital_clock_preview": "jbclock-appwidget_digital_clock_preview.png",
}

CLOCK_ASSETS = {
    "kitkat_clock_dial": "appwidget_clock_dial.png",
    "kitkat_clock_hour": "appwidget_clock_hour.png",
    "kitkat_clock_minute": "appwidget_clock_minute.png",
    "kitkat_clock_font": "AndroidClock.ttf",
    "kitkat_clock_mono_bold": "AndroidClockMono-Bold.ttf",
    "kitkat_clock_mono_light": "AndroidClockMono-Light.ttf",
    "kitkat_clock_mono_thin": "AndroidClockMono-Thin.ttf",
}

# Labels in appfilter.xml -> original KitKat artwork resource.
LABEL_RULES = (
    (("googleplus", "google+"), "google_plus"),
    (("newsstand", "playnewsstand", "magazines"), "newsstand"),
    (("google news", "googlenews", "news"), "news_weather"),
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

    # Preserve both original Android 4.4.4 wallpapers as separate choices.
    for resource, filename in WALLPAPERS.items():
        wallpaper_url = f"{SOURCE_BASE}/{filename}"
        wallpaper_request = urllib.request.Request(
            wallpaper_url, headers={"User-Agent": "Insomdroid-KitKat-Icon-Importer/1.0"}
        )
        with urllib.request.urlopen(wallpaper_request, timeout=45) as response:
            wallpaper_data = response.read()
        if not wallpaper_data.startswith(JPEG_SIGNATURE):
            raise ValueError(f"Source is not a JPEG wallpaper: {wallpaper_url}")
        (destination_dir / f"{resource}.jpg").write_bytes(wallpaper_data)
        print(f"WALLPAPER {resource} <- {filename} ({len(wallpaper_data)} bytes)")

    # Import original KitKat clock artwork and clock typefaces for the live widget.
    clock_drawables = RES / "drawable-nodpi"
    clock_font_dir = RES / "font"
    clock_font_dir.mkdir(parents=True, exist_ok=True)
    for resource, filename in CLOCK_ASSETS.items():
        request = urllib.request.Request(
            f"{SOURCE_BASE}/{filename}",
            headers={"User-Agent": "Insomdroid-KitKat-Icon-Importer/1.0"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            asset_data = response.read()
        if filename.endswith(".png") and not asset_data.startswith(PNG_SIGNATURE):
            raise ValueError(f"Clock artwork is not a PNG: {filename}")
        if filename.endswith(".ttf") and not asset_data.startswith(b"\x00\x01\x00\x00"):
            raise ValueError(f"Clock typeface is not a TrueType font: {filename}")
        target = clock_font_dir / f"{resource}.ttf" if filename.endswith(".ttf") else clock_drawables / f"{resource}.png"
        target.write_bytes(asset_data)
        print(f"CLOCK_ASSET {resource} <- {filename} ({len(asset_data)} bytes)")

    # Import original artwork used by Android 4.4.4 home-screen widgets.
    for resource, filename in WIDGET_ASSETS.items():
        request = urllib.request.Request(
            f"{SOURCE_BASE}/{filename}",
            headers={"User-Agent": "Insomdroid-KitKat-Icon-Importer/1.0"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            asset_data = response.read()
        if not asset_data.startswith(PNG_SIGNATURE):
            raise ValueError(f"Widget artwork is not a PNG: {filename}")
        (destination_dir / f"{resource}.png").write_bytes(asset_data)
        print(f"WIDGET_ASSET {resource} <- {filename} ({len(asset_data)} bytes)")

    # Register widget artwork as standalone drawable resources.
    drawable_root = ET.parse(DRAWABLES_XML).getroot() if DRAWABLES_XML.is_file() else ET.Element("resources")
    existing_widget_names = {item.attrib.get("name") for item in drawable_root.findall("item")}
    for resource in WIDGET_ASSETS:
        if resource not in existing_widget_names:
            ET.SubElement(drawable_root, "item", {"drawable": resource, "name": resource})
    ET.indent(drawable_root, space="  ")
    DRAWABLES_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(drawable_root, encoding="unicode") + "\n",
        encoding="utf-8",
    )

    # Register all widget artwork and wallpapers in the drawable catalogue.
    drawable_root = ET.parse(DRAWABLES_XML).getroot() if DRAWABLES_XML.is_file() else ET.Element("resources")
    existing_names = {item.attrib.get("name") for item in drawable_root.findall("item")}
    for resource in list(WIDGET_ASSETS) + list(WALLPAPERS) + ["kitkat_clock_dial", "kitkat_clock_hour", "kitkat_clock_minute"]:
        if resource not in existing_names:
            ET.SubElement(drawable_root, "item", {"drawable": resource, "name": resource})
    ET.indent(drawable_root, space="  ")
    DRAWABLES_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(drawable_root, encoding="unicode") + "\n",
        encoding="utf-8",
    )

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
