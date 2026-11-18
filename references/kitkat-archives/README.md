# KitKat-era icon source archives

Upload the original APK or ZIP archives you want inspected into this folder.

## What to upload

- HoloRay Android KitKat Theme APK
- Other icon-pack APKs from the Internet Archive collection
- ZIP archives containing original Android 4.4-era applications or icon resources

Do not install old APKs on your phone. Upload the files here as archive material only; they will be inspected offline.

## Important

- Keep the original filenames.
- Do not extract or modify the archives before uploading.
- If an archive is too large for GitHub's web uploader, upload it as an asset to a GitHub Release and send the release asset link instead.
- Files in this folder are source material only. They are not automatically included in any APK.

The icon import process will check package metadata, extract launcher icon image resources without redrawing them, record source provenance, and calculate SHA-256 hashes to count unique images. Redistribution and licensing will be reviewed before including extracted artwork in a release.


## Current committed source inventory

The folder currently contains two uploaded ZIP archives (`Icons jb 1.zip` and `icons jb2.zip`) and the Figma community icon-pack source. Both ZIPs are read directly by the Holokat importer; extracted reference directories are not treated as the complete source inventory. The importer keeps original artwork and reports which assets were mapped or left unmapped.
