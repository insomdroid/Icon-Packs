# Insomdroid Icon Packs

This repository maintains two independently installable Android icon packs.

## HoloKat

HoloKat combines original Android 4.4 KitKat artwork with the supplied Jelly Bean archive artwork.

- Module: `pack-kitkat`
- Application ID: `com.insomdroid.holokat`
- Build: [HoloKat release workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml)
- Artwork mapping audit: [HoloKat audit workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/audit-holokat.yml)
- Source attribution: [HoloKat attribution](docs/HOLOKAT_ATTRIBUTION.md)

## Nothink2

Nothink2 is a Lawnicons-based icon pack with a Nothing OS-inspired dark presentation.

- Module: `pack-nothink2`
- Application ID: `com.insomdroid.iconpacks.nothink2`
- Base artwork and mappings: pinned Lawnicons SVGs and component mappings (Apache-2.0)
- Classic icons: near-black tile, centered white glyph
- Themed icons: transparent monochrome masks for compatible launchers
- Build: [Nothink2 release workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-nothink2.yml)
- Source attribution: [Nothink2 attribution](docs/NOTHINK2_ATTRIBUTION.md)

Nothink2 is unofficial and is not affiliated with Lawnchair, Lawnicons, or Nothing Technology Limited.

## Development

The two packs share the Gradle root configuration and the small `core` module. Artwork importers and archive source files are retained only where required to regenerate the corresponding pack.
