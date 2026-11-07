#!/usr/bin/env python3
"""Import real launcher icons from old, open-source Android APKs in F-Droid Archive.

Only archived APK builds targeting Android 4.4/API 19 or lower are eligible.
Icons are extracted unchanged from APK resources. SHA-256 deduplication ensures
that the 500-icon threshold counts unique image bytes, not app mappings.
"""

from __future__ import annotations

import concurrent.futures
import csv
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "pack-kitkat/src/main/res/drawable-nodpi"
APPFILTER = ROOT / "pack-kitkat/src/main/res/xml/appfilter.xml"
DRAWABLES = ROOT / "pack-kitkat/src/main/res/xml/drawable.xml"
ASSET_DIR = ROOT / "pack-kitkat/src/main/assets"
INVENTORY = ASSET_DIR / "kitkat-era-fdroid-icons.csv"
INDEX_URL = "https://f-droid.org/archive/index-v1.json"
ARCHIVE_BASE = "https://f-droid.org/archive/"
MIN_UNIQUE_ICONS = int(os.environ.get("KITKAT_MIN_ARCHIVE_ICONS", "500"))
MAX_CANDIDATES = int(os.environ.get("KITKAT_MAX_ARCHIVE_CANDIDATES", "1800"))
WORKERS = int(os.environ.get("KITKAT_DOWNLOAD_WORKERS", "12"))
MAX_APK_BYTES = 60 * 1024 * 1024
BEGIN = "<!-- BEGIN GENERATED F-DROID ARCHIVE ICONS -->"
END = "<!-- END GENERATED F-DROID ARCHIVE ICONS -->"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
USER_AGENT = "Insomdroid-KitKat-Icon-Importer/1.0 (+https://github.com/insomdroid/Icon-Packs)"


def fetch(url: str, destination: Path | None = None, attempts: int = 3) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read(MAX_APK_BYTES + 1 if destination else 0)
                if destination:
                    if len(data) > MAX_APK_BYTES:
                        raise ValueError("APK exceeds size limit")
                    destination.write_bytes(data)
                    return data
                return data
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(attempt + 1)
    print(f"WARNING: download failed: {url}: {last_error}", file=sys.stderr)
    return None


def integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def app_metadata(index: dict) -> dict[str, dict]:
    result = {}
    for app in index.get("apps", []):
        package = app.get("packageName")
        if package:
            result[package] = app
    return result


def existing_packages() -> set[str]:
    text = APPFILTER.read_text(encoding="utf-8")
    return set(re.findall(r'ComponentInfo\{([^/}]+)/', text))


def candidates(index: dict, metadata: dict, excluded: set[str]) -> list[dict]:
    result = []
    packages = index.get("packages", {})
    for package, versions in packages.items():
        if package in excluded or not versions:
            continue
        app = metadata.get(package, {})
        license_name = str(app.get("license", "")).strip()
        if not license_name or license_name.lower() in {"unknown", "proprietary", "all rights reserved"}:
            continue

        ordered = sorted(versions, key=lambda item: integer(item.get("versionCode")) or 0)
        selected = None
        for version in ordered:
            target = integer(version.get("targetSdkVersion"))
            if target is not None and target > 19:
                continue
            if not version.get("apkName") or not version.get("hash"):
                continue
            selected = version
            break
        if selected is None:
            continue
        size = integer(selected.get("size")) or 0
        if size > MAX_APK_BYTES:
            continue
        result.append({
            "package": package,
            "app_name": str(app.get("name") or package),
            "license": license_name,
            "version_name": str(selected.get("versionName") or ""),
            "version_code": str(selected.get("versionCode") or ""),
            "apk_name": selected["apkName"],
            "apk_hash": str(selected["hash"]).lower(),
            "target_sdk_index": integer(selected.get("targetSdkVersion")),
        })
    result.sort(key=lambda item: (item["package"].count("."), item["package"]))
    return result[:MAX_CANDIDATES]


def parse_badging(apk_path: Path, aapt: str) -> dict | None:
    try:
        output = subprocess.run(
            [aapt, "dump", "badging", str(apk_path)],
            check=True, capture_output=True, text=True, timeout=40
        ).stdout
    except (subprocess.SubprocessError, OSError) as error:
        print(f"WARNING: aapt could not inspect {apk_path.name}: {error}", file=sys.stderr)
        return None

    package_match = re.search(r"^package: name='([^']+)'", output, re.MULTILINE)
    target_match = re.search(r"^targetSdkVersion:'(\d+)'", output, re.MULTILINE)
    activity_match = re.search(r"^launchable-activity: name='([^']+)'", output, re.MULTILINE)
    if not package_match or not activity_match:
        return None
    target_sdk = integer(target_match.group(1)) if target_match else None
    if target_sdk is None or target_sdk > 19:
        return None

    icons = []
    for density, path in re.findall(r"^application-icon-(\d+):'([^']+)'", output, re.MULTILINE):
        icons.append((integer(density) or 0, path))
    if not icons:
        match = re.search(r"^application:.*?\bicon='([^']+)'", output, re.MULTILINE)
        if match:
            icons.append((0, match.group(1)))
    if not icons:
        return None

    return {
        "package": package_match.group(1),
        "activity": activity_match.group(1),
        "target_sdk": target_sdk,
        "icon_paths": [path for _, path in sorted(icons, reverse=True)],
    }


def extract_png(apk_path: Path, paths: list[str]) -> bytes | None:
    try:
        with zipfile.ZipFile(apk_path) as archive:
            for path in paths:
                if path.endswith(".png"):
                    try:
                        data = archive.read(path)
                    except KeyError:
                        continue
                    if data.startswith(PNG_SIGNATURE):
                        return data
    except (OSError, zipfile.BadZipFile):
        return None
    return None


def normalize_activity(package: str, activity: str) -> str:
    if activity.startswith("."):
        return package + activity
    if "." not in activity:
        return package + "." + activity
    return activity


def strip_generated(text: str) -> str:
    pattern = re.escape(BEGIN) + r".*?" + re.escape(END)
    return re.sub(pattern, "", text, flags=re.DOTALL).rstrip()


def main() -> int:
    print(f"Downloading official F-Droid Archive index: {INDEX_URL}")
    raw_index = fetch(INDEX_URL)
    if not raw_index:
        raise RuntimeError("Could not download the F-Droid Archive index")
    index = json.loads(raw_index)
    metadata = app_metadata(index)
    excluded = existing_packages()
    queue = candidates(index, metadata, excluded)
    print(f"Archive index candidates targeting API 19 or lower: {len(queue)}")
    if len(queue) < MIN_UNIQUE_ICONS:
        raise RuntimeError(
            f"Only {len(queue)} eligible archived APK candidates are available; "
            f"at least {MIN_UNIQUE_ICONS} unique icons are required."
        )

    aapt = os.environ.get("AAPT")
    if not aapt:
        sdk = Path(os.environ.get("ANDROID_HOME", os.environ.get("ANDROID_SDK_ROOT", "")))
        candidates_aapt = sorted((sdk / "build-tools").glob("*/aapt"), reverse=True)
        if not candidates_aapt:
            raise RuntimeError("Android build-tools aapt was not found")
        aapt = str(candidates_aapt[0])

    RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for old in RESOURCE_DIR.glob("fdroid_*.png"):
        old.unlink()

    unique: dict[str, str] = {}
    appfilter_items = []
    drawable_items = []
    inventory_rows = []
    attempted = 0
    accepted = 0

    with tempfile.TemporaryDirectory(prefix="kitkat-fdroid-") as temp:
        temp_dir = Path(temp)
        for batch_start in range(0, len(queue), WORKERS):
            if len(unique) >= MIN_UNIQUE_ICONS:
                break
            batch = queue[batch_start:batch_start + WORKERS]
            futures = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for candidate in batch:
                    attempted += 1
                    apk_path = temp_dir / f"{attempted}.apk"
                    url = ARCHIVE_BASE + candidate["apk_name"]
                    futures[pool.submit(fetch, url, apk_path)] = (candidate, apk_path)

                for future in concurrent.futures.as_completed(futures):
                    candidate, apk_path = futures[future]
                    try:
                        data = future.result()
                    except Exception as error:
                        print(f"WARNING: download task failed for {candidate['package']}: {error}", file=sys.stderr)
                        continue
                    if data is None:
                        continue

                    actual_apk_hash = hashlib.sha256(data).hexdigest()
                    if actual_apk_hash != candidate["apk_hash"]:
                        print(f"WARNING: hash mismatch for {candidate['package']}; skipped", file=sys.stderr)
                        continue

                    details = parse_badging(apk_path, aapt)
                    if not details or details["package"] != candidate["package"]:
                        continue
                    image_data = extract_png(apk_path, details["icon_paths"])
                    if not image_data:
                        continue

                    digest = hashlib.sha256(image_data).hexdigest()
                    resource = unique.get(digest)
                    if resource is None:
                        resource = "fdroid_" + digest[:20]
                        unique[digest] = resource
                        (RESOURCE_DIR / f"{resource}.png").write_bytes(image_data)
                        drawable_items.append(f'  <item drawable="{resource}" name="{resource}" />')

                    package = details["package"]
                    activity = normalize_activity(package, details["activity"])
                    app_name = html.escape(candidate["app_name"], quote=True)
                    appfilter_items.append(
                        f'  <item component="ComponentInfo{{{package}/{activity}}}" '
                        f'drawable="{resource}" name="{app_name}" />'
                    )
                    inventory_rows.append([
                        package, candidate["app_name"], candidate["version_name"],
                        candidate["version_code"], candidate["license"],
                        details["target_sdk"], candidate["apk_name"],
                        actual_apk_hash, digest, f"drawable-nodpi/{resource}.png"
                    ])
                    accepted += 1
                    if accepted % 50 == 0:
                        print(f"Processed {accepted} apps; {len(unique)} unique icons")
                    if len(unique) >= MIN_UNIQUE_ICONS:
                        for pending in futures:
                            if not pending.done():
                                pending.cancel()
                        break

    if len(unique) < MIN_UNIQUE_ICONS:
        raise RuntimeError(
            f"Only {len(unique)} unique PNG icons extracted from {accepted} eligible apps "
            f"after checking {attempted} archived APKs. Required: {MIN_UNIQUE_ICONS}."
        )

    drawable_text = strip_generated(DRAWABLES.read_text(encoding="utf-8"))
    drawable_text = drawable_text.replace(
        "</resources>",
        "\n" + BEGIN + "\n" + "\n".join(drawable_items) + "\n" + END + "\n</resources>"
    )
    DRAWABLES.write_text(drawable_text + "\n", encoding="utf-8")

    appfilter_text = strip_generated(APPFILTER.read_text(encoding="utf-8"))
    appfilter_text = appfilter_text.replace(
        "</resources>",
        "\n" + BEGIN + "\n" + "\n".join(appfilter_items) + "\n" + END + "\n</resources>"
    )
    APPFILTER.write_text(appfilter_text + "\n", encoding="utf-8")

    with INVENTORY.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow([
            "package_name", "app_name", "version_name", "version_code",
            "license", "target_sdk", "apk_filename", "apk_sha256",
            "icon_sha256", "resource_path"
        ])
        writer.writerows(inventory_rows)

    print(f"SUCCESS: {len(unique)} unique archived APK launcher icons extracted.")
    print(f"Mapped {accepted} app launcher components.")
    print(f"Inventory: {INVENTORY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
