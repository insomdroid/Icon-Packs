#!/usr/bin/env python3
"""Import original Android 4.4.4 AOSP launcher icon PNGs into the KitKat pack.

The source projects are pinned to the immutable android-4.4.4_r2 tag. Only
launcher icon PNG files referenced by each app manifest are copied; no APKs,
Google proprietary apps, or community-redrawn artwork are included.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "pack-kitkat" / "src" / "main" / "res"
TAG = "android-4.4.4_r2"
ANDROID = "{http://schemas.android.com/apk/res/android}"

# Pack drawable name -> AOSP repository path under platform/packages/apps.
SOURCES = {
    "contacts": "Contacts",
    "messages": "Mms",
    "calendar": "Calendar",
    "clock": "DeskClock",
    "calculator": "Calculator",
    "camera": "Camera",
    "gallery": "Gallery",
    "settings": "Settings",
    "files": "DocumentsUI",
    "browser": "Browser",
    "mail": "Email",
}

DENSITY_ORDER = ("xxxhdpi", "xxhdpi", "xhdpi", "hdpi", "mdpi", "nodpi")


def clone_source(repo_name: str, destination: Path) -> Path:
    url = f"https://android.googlesource.com/platform/packages/apps/{repo_name}"
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", "--branch", TAG, url, str(destination)],
        check=True,
    )
    return destination


def manifest_icon(project: Path) -> str:
    manifest = project / "AndroidManifest.xml"
    if not manifest.is_file():
        raise FileNotFoundError(f"Missing AndroidManifest.xml: {manifest}")
    root = ET.parse(manifest).getroot()
    application = root.find("application")
    if application is None:
        raise RuntimeError(f"No application element in {manifest}")

    # Prefer the application icon. If absent, use the first MAIN/LAUNCHER
    # activity or alias icon, matching Android's launcher resolution.
    icon = application.get(ANDROID + "icon")
    if icon:
        return icon
    for activity in list(application):
        if activity.tag not in ("activity", "activity-alias"):
            continue
        intent_filters = activity.findall("intent-filter")
        is_launcher = any(
            any(
                item.get(ANDROID + "name") == "android.intent.action.MAIN"
                for item in intent_filter.findall("action")
            )
            and any(
                item.get(ANDROID + "name") == "android.intent.category.LAUNCHER"
                for item in intent_filter.findall("category")
            )
            for intent_filter in intent_filters
        )
        if is_launcher and activity.get(ANDROID + "icon"):
            return activity.get(ANDROID + "icon", "")
    raise RuntimeError(f"No launcher icon reference found in {manifest}")


def resolve_png(project: Path, reference: str) -> Path:
    if not reference.startswith("@") or "/" not in reference:
        raise RuntimeError(f"Unsupported launcher icon reference: {reference}")
    resource_type, resource_name = reference[1:].split("/", 1)
    if resource_type not in ("mipmap", "drawable"):
        raise RuntimeError(f"Unsupported launcher icon resource type: {reference}")

    candidates: list[Path] = []
    for density in DENSITY_ORDER:
        folder = project / "res" / f"{resource_type}-{density}"
        candidates.extend((folder / f"{resource_name}.png", folder / f"{resource_name}.webp"))
    candidates.extend(
        (
            project / "res" / resource_type / f"{resource_name}.png",
            project / "res" / resource_type / f"{resource_name}.webp",
        )
    )
    for candidate in candidates:
        if candidate.is_file() and candidate.suffix.lower() == ".png":
            return candidate

    # Some KitKat projects store a mipmap resource in a drawable density
    # folder (or use a different resource folder convention). Search by the
    # exact resource basename as a safe fallback, still accepting PNG only.
    matches = sorted(
        (path for path in (project / "res").rglob(f"{resource_name}.png") if path.is_file()),
        key=lambda path: (("xxxhdpi", "xxhdpi", "xhdpi", "hdpi", "mdpi", "nodpi").index(
            next((density for density in ("xxxhdpi", "xxhdpi", "xhdpi", "hdpi", "mdpi", "nodpi") if density in path.parent.name), "nodpi")
        )),
    )
    if matches:
        return matches[0]
    raise FileNotFoundError(
        f"No PNG source found for {reference} in {project}/res"
    )


def main() -> None:
    output = RES / "drawable-nodpi"
    output.mkdir(parents=True, exist_ok=True)
    imported: list[str] = []

    with tempfile.TemporaryDirectory(prefix="aosp-kitkat-") as temporary:
        temp_root = Path(temporary)
        for drawable_name, repo_name in SOURCES.items():
            project = clone_source(repo_name, temp_root / repo_name)
            reference = manifest_icon(project)
            source_png = resolve_png(project, reference)

            # Remove the old illustrative vector so Android sees only the
            # authentic source bitmap under this resource name.
            old_vector = RES / "drawable" / f"{drawable_name}.xml"
            if old_vector.exists():
                old_vector.unlink()

            destination = output / f"{drawable_name}.png"
            shutil.copy2(source_png, destination)
            imported.append(
                f"{drawable_name}: {repo_name}/{reference} -> "
                f"{source_png.relative_to(project)}"
            )

    if len(imported) != len(SOURCES):
        raise RuntimeError("AOSP icon import was incomplete")
    print("Imported original AOSP Android 4.4.4 launcher icon assets:")
    for item in imported:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
