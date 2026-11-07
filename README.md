# Insomdroid Icon Packs

Two separately installable Android icon pack APKs are maintained in this repository.

## Holokat

The original Android 4.4 KitKat and supplied Jelly Bean artwork combined in one APK. See the existing [combined icon pack workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml) and [Jelly Bean artwork attribution](docs/HOLOKAT_ATTRIBUTION.md).

## Nothink

Nothink is an independent icon pack inspired by the visual discipline of Nothing OS 2.0/3.0 and Nothing OS 5.0. Its approved design direction is modern, monochrome, and built from custom recognizable symbols using a consistent hybrid of solid shapes and outline strokes.

**The approved design specification is recorded in [Nothink Design Guide](docs/NOTHINK_DESIGN_GUIDE.md).** Treat that document as the source of truth before changing the artwork, generator, mappings, or validation. The current generator has not yet been migrated to the approved design; existing generated artwork must not be considered compliant until that migration and visual review are complete.

- Name: Nothink
- Application ID: `com.insomdroid.iconpacks.nothink`
- Mapping: Lawnicons Android component mappings, pinned to a fixed source revision; mapping data only, not upstream artwork
- Approved artwork: custom per-app symbols; transparent backgrounds; pure-white normal glyphs; transparent monochrome themed glyphs
- Build: [Build Nothink Icon Pack Release APK](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-nothink.yml)
- Artifact: `nothink-icon-pack-release` (one-day retention)

See [Nothink artwork and mapping attribution](docs/NOTHINK_ATTRIBUTION.md). Nothink is an unofficial independent project and is not affiliated with Nothing Technology Limited.
