# Insomdroid Icon Packs

Separately installable Android icon pack APKs are maintained in this repository.

## Holokat

The original Android 4.4 KitKat and supplied Jelly Bean artwork combined in one APK. See the [combined icon pack workflow](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml) and [Jelly Bean artwork attribution](docs/HOLOKAT_ATTRIBUTION.md).

## Nothink

Nothink is an independent icon pack inspired by Nothing OS 2.0/3.0 and Nothing OS 5.0. Its design guide and implementation status are documented in [Nothink Design Guide](docs/NOTHINK_DESIGN_GUIDE.md).

## Nothink2

Nothink2 is a separate Lawnicons-based icon pack with a Nothing OS 5.0 dark presentation.

- App name: **Nothink2**
- Application ID: `com.insomdroid.iconpacks.nothink2`
- Base artwork and mappings: pinned Lawnicons SVGs and component mappings (Apache-2.0)
- Classic icons: near-black tile, centered white Lawnicons glyph, intentionally reduced glyph scale
- Themed icons: transparent monochrome masks for wallpaper-derived colors on compatible launchers
- Icon shape: follows the shape selected in the launcher/device; it is not baked into the artwork
- Android target: API 33 (Android 13)
- Build: [Build Nothink2 APK](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-nothink2.yml)
- Artifact: `nothink2-release-apk`

Enable themed icons in Android and in a compatible launcher to use wallpaper-derived icon colors. Classic icon-pack and themed-icon support varies by launcher.

See [Nothink2 artwork attribution](docs/NOTHINK2_ATTRIBUTION.md). Nothink2 is unofficial and is not affiliated with Lawnchair, Lawnicons, or Nothing Technology Limited.
