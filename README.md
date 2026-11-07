# Insomdroid Icon Packs

Two separately installable Android icon pack APKs are maintained in this repository.

## Holokat

The original Android 4.4 KitKat and supplied Jelly Bean artwork combined in one APK. See the existing [combined icon pack workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml) and [Jelly Bean artwork attribution](docs/HOLOKAT_ATTRIBUTION.md).

## Nothink

A separate monochrome geometric icon pack inspired by Nothing OS. Its visual direction is **Geometric Solid**: bold, simple pictograms with consistent geometry, white artwork on a near-black field, restrained red accents, and subtle dot-matrix details. Lawnicons supplies only Android component mappings; Nothink illustrations are drawn by the generator in this repository. No upstream icon artwork or SVG is used.

- Name: Nothink
- Application ID: `com.insomdroid.iconpacks.nothink`
- Mapping: Lawnicons component mappings, pinned to a fixed source revision
- Artwork: original Nothink-inspired geometric pictograms, generated for every unique mapped drawable; separate transparent monochrome assets support wallpaper-tinted themed icons
- Build: [Build Nothink Icon Pack Release APK](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-nothink.yml)
- Artifact: `nothink-icon-pack-release` (one-day retention)

See [Nothink artwork and mapping attribution](docs/NOTHINK_ATTRIBUTION.md). Nothink is an unofficial independent project and is not affiliated with Nothing Technology Limited.
