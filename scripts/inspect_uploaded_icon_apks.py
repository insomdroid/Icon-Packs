#!/usr/bin/env python3
"""Inspect uploaded legacy icon-pack APKs without installing them."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path("references/kitkat-archives")
OUT = Path("build/reference-inspection")
OUT.mkdir(parents=True, exist_ok=True)
rows = []
unique = {}
image_ext = {".png", ".webp", ".jpg", ".jpeg"}
for apk in sorted(ROOT.glob("*.apk")):
    try:
        with zipfile.ZipFile(apk) as z:
            names = z.namelist()
            image_files = [n for n in names if Path(n).suffix.lower() in image_ext]
            badging = subprocess.run(["aapt", "dump", "badging", str(apk)], text=True,
                                     capture_output=True, check=False).stdout
            def match(pattern):
                m = re.search(pattern, badging, re.M)
                return m.group(1) if m else ""
            package = match(r"^package: name='([^']+)'")
            version = match(r"^package: .* versionName='([^']*)'")
            sdk = match(r"^sdkVersion:'([^']+)'")
            target = match(r"^targetSdkVersion:'([^']+)'")
            app_icon = match(r"^application:.* icon='([^']+)'")
            apk_hash = hashlib.sha256(apk.read_bytes()).hexdigest()
            extracted = 0
            for name in image_files:
                data = z.read(name)
                digest = hashlib.sha256(data).hexdigest()
                unique.setdefault(digest, {"apk": apk.name, "entry": name, "bytes": len(data)})
                if name == app_icon or name.endswith("/" + app_icon):
                    target_dir = OUT / "launcher-icons" / apk.stem
                    target_dir.mkdir(parents=True, exist_ok=True)
                    (target_dir / (digest + Path(name).suffix.lower())).write_bytes(data)
                    extracted += 1
            rows.append({
                "file": apk.name, "size_bytes": apk.stat().st_size, "package": package,
                "version_name": version, "min_sdk": sdk, "target_sdk": target,
                "application_icon_resource": app_icon, "image_resource_files": len(image_files),
                "unique_image_hashes_including_this_apk": len({hashlib.sha256(z.read(n)).hexdigest() for n in image_files}),
                "launcher_icon_extracted": bool(extracted), "apk_sha256": apk_hash,
                "aapt_error": subprocess.run(["aapt", "dump", "badging", str(apk)],
                    text=True, capture_output=True).stderr[:1000]
            })
    except Exception as exc:
        rows.append({"file": apk.name, "error": str(exc)})
report = {"apk_count": len(list(ROOT.glob("*.apk"))), "unique_image_hashes_across_apks": len(unique),
          "apks": rows, "unique_images": list(unique.values())}
(OUT / "inspection-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
with (OUT / "inspection-report.md").open("w", encoding="utf-8") as f:
    f.write("# Uploaded APK inspection\n\n")
    f.write(f"- APK files: {report['apk_count']}\n- Unique image resource hashes across APKs: {len(unique)}\n\n")
    f.write("| File | Package | Version | minSdk | targetSdk | Image resources | App icon resource |\n|---|---|---:|---:|---:|---:|---|\n")
    for r in rows:
        f.write("| {file} | {package} | {version_name} | {min_sdk} | {target_sdk} | {image_resource_files} | {application_icon_resource} |\n".format(
            **{k: str(r.get(k, "")).replace("|", "/") for k in ["file","package","version_name","min_sdk","target_sdk","image_resource_files","application_icon_resource"]}))
print(json.dumps({"apk_count": report["apk_count"], "unique_image_hashes": len(unique), "rows": rows}, indent=2))
