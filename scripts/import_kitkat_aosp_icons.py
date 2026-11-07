#!/usr/bin/env python3
"""Import original Android 4.4.4 AOSP launcher artwork into the KitKat pack.

The source tag is pinned to android-4.4.4_r2. Only PNG resources verified in the corresponding Android 4.4.4 AOSP source
repositories are included here. Manifest references are checked where the
source repository contains the app manifest. Existing default-density XML artwork remains as fallback for
icons that are not covered by this verified source list.
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_ROOT = ROOT / "pack-kitkat" / "src" / "main" / "res"
AOSP_TAG = "android-4.4.4_r2"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# drawable name -> (AOSP repository, exact source path, destination density)
# These paths were checked against the Android 4.4.4_r2 AOSP source trees.
ASSETS = {
    "contacts": (
        "platform_packages_apps_contacts",
        "res/mipmap-xxhdpi/ic_launcher_contacts.png",
        "drawable-xxhdpi",
    ),
    "messages": (
        "platform_packages_apps_mms",
        "res/mipmap-xxhdpi/ic_launcher_smsmms.png",
        "drawable-xxhdpi",
    ),
    "settings": (
        "platform_packages_apps_settings",
        "res/mipmap-xxxhdpi/ic_launcher_settings.png",
        "drawable-xxxhdpi",
    ),
    "camera": (
        "platform_packages_apps_camera",
        "res/mipmap-xxhdpi/ic_launcher_camera.png",
        "drawable-xxhdpi",
    ),
    "calendar": (
        "platform_packages_apps_calendar",
        "res/mipmap-xxhdpi/ic_launcher_calendar.png",
        "drawable-xxhdpi",
    ),
    "calculator": (
        "platform_packages_apps_calculator",
        "res/mipmap-xxxhdpi/ic_launcher_calculator.png",
        "drawable-xxxhdpi",
    ),
    "mail": (
        "platform_packages_apps_email",
        "res/mipmap-xxhdpi/ic_launcher_mail.png",
        "drawable-xxhdpi",
    ),
    "browser": (
        "platform_packages_apps_browser",
        "res/mipmap-xxhdpi/ic_launcher_browser.png",
        "drawable-xxhdpi",
    ),
    "downloads": (
        "platform_packages_providers_downloadprovider",
        "res/mipmap-xxxhdpi/ic_launcher_download.png",
        "drawable-xxxhdpi",
    ),
}


def download(url: str) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "Insomdroid-KitKat-Icon-Importer/1.0"},
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                data = response.read()
            if not data.startswith(PNG_SIGNATURE):
                raise ValueError(f"Downloaded file is not a PNG: {url}")
            return data
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Unable to download verified AOSP icon: {url}: {last_error}")


def main() -> int:
    imported = []
    for drawable, (repository, source_path, destination_density) in ASSETS.items():
        url = (
            f"https://raw.githubusercontent.com/aosp-mirror/{repository}/"
            f"{AOSP_TAG}/{source_path}"
        )
        data = download(url)
        destination_dir = RESOURCE_ROOT / destination_density
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / f"{drawable}.png"
        destination.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        imported.append((drawable, destination.relative_to(ROOT), len(data), digest))
        print(f"Imported {drawable}: {destination.relative_to(ROOT)} ({len(data)} bytes)")

    print(f"Imported {len(imported)} original AOSP Android 4.4.4 icons.")
    for drawable, path, size, digest in imported:
        print(f"ASSET {drawable} {path} {size} sha256={digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
