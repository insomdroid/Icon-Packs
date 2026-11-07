# Insomdroid Icon Packs

Two separately installable Android icon pack APKs are maintained in this repository.

## Holokat

The original Android 4.4 KitKat and supplied Jelly Bean artwork combined in one APK. See the existing [combined icon pack workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml) and [Jelly Bean artwork attribution](docs/HOLOKAT_ATTRIBUTION.md).

## Nothink

A separate monochrome geometric icon pack inspired by Nothing OS. Lawnicons supplies only the Android component mapping; every Nothink illustration is drawn by the original generator in this repository. No Lawnicons SVG artwork is used.

- Name: Nothink
- Application ID: `com.insomdroid.iconpacks.nothink`
- Target: at least 3,000 app component mappings from Lawnicons
- Artwork: original Nothink geometric illustrations are generated for mapped drawables during the build; no upstream SVG artwork is downloaded or used
- Build: [Build Nothink Icon Pack Release APK](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-nothink.yml)
- Artifact: `nothink-icon-pack-release` (one-day retention)

The workflow verifies the 3,000-mapping minimum and generates original artwork for each unique mapped drawable.

See [Nothink artwork and mapping attribution](docs/NOTHINK_ATTRIBUTION.md). Nothink is an unofficial independent project and is not affiliated with Nothing Technology Limited.
