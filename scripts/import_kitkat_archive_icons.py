#!/usr/bin/env python3
"""Import verified KitKat-era bitmap references into the KitKat icon pack.

The source images remain in references/kitkat-archives. Density-specific PNGs
are added alongside the existing vector fallbacks, so Android can select the
bitmap on xxxhdpi devices and retain the vector on other densities.
"""

from __future__ import annotations

import struct
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "kitkat-archives" / "drawable-xxxhdpi"
DESTINATION = ROOT / "pack-kitkat" / "src" / "main" / "res" / "drawable-xxxhdpi"

# Resource name -> exact archived source filename.
ICON_IMPORTS = {
    "browser": "browser.png",
    "calculator": "calculator.png",
    "calendar": "calendar.png",
    "camera": "camera.png",
    "clock": "clock.png",
    "contacts": "contacts.png",
    "downloads": "downloads.png",
    "mail": "email.png",
    "messages": "messaging.png",
    "music": "music.png",
    "phone": "phone.png",
    "settings": "settings.png",
}

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        header = image.read(24)
    if len(header) != 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError(f"Not a valid PNG image: {path}")
    return struct.unpack(">II", header[16:24])


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Missing reference directory: {SOURCE}")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    imported = []

    for resource_name, source_name in ICON_IMPORTS.items():
        source = SOURCE / source_name
        if not source.is_file():
            raise SystemExit(f"Missing required archived icon: {source}")
        width, height = png_dimensions(source)
        if width < 96 or height < 96:
            raise SystemExit(
                f"Icon is unexpectedly small ({width}x{height}): {source}"
            )

        destination = DESTINATION / f"{resource_name}.png"
        shutil.copy2(source, destination)
        imported.append((resource_name, source_name, width, height))

    print(f"Imported {len(imported)} original bitmap references:")
    for resource_name, source_name, width, height in imported:
        print(f"  {resource_name}.png <- {source_name} ({width}x{height})")


if __name__ == "__main__":
    main()
