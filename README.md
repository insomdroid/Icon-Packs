# Insomdroid Icon Packs

Two separately installable Android icon pack APKs are maintained in this repository.

## Holokat

The original Android 4.4 KitKat and supplied Jelly Bean artwork combined in one APK. See the existing [combined icon pack workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml) and [Jelly Bean artwork attribution](docs/HOLOKAT_ATTRIBUTION.md).

## Nothink

A separate monochrome icon pack inspired by Nothing OS. It uses the pinned Lawnicons component mapping and SVG source artwork, transformed during the first GitHub Actions build into a dark circular monochrome icon set plus a separate glyph-only layer for compatible wallpaper-tinted themed-icon launchers.

- Name: Nothink
- Application ID: `com.insomdroid.iconpacks.nothink`
- Target: at least 3,000 app component mappings from Lawnicons
- Artwork: every mapped SVG is generated into the APK during the build; missing source artwork fails the build instead of silently leaving mappings without images
- Build: [Build Nothink Icon Pack Release APK](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-nothink.yml)
- Artifact: `nothink-icon-pack-release` (one-day retention)

The number of supported app components and the number of unique source illustrations are different counts. The workflow prints both values and verifies the 3,000-mapping minimum.

See [Nothink artwork and mapping attribution](docs/NOTHINK_ATTRIBUTION.md). Nothink is an unofficial independent project and is not affiliated with Nothing Technology Limited.
