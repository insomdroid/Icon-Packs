# Insomdroid Icon Pack

One installable Android icon pack APK combining authentic Android 4.4 KitKat artwork and the supplied Jelly Bean-era artwork archives. These are artwork sources inside one pack, not separate themes or APKs.

## Combined icon collection

- Original Android 4.4.4 AOSP application icons imported from the pinned `android-4.4.4_r2` source tag.
- Archived KitKat-era bitmap icons from `references/kitkat-archives/drawable-xxxhdpi`.
- 265 unique Jelly Bean archive images from the two HKtorito archives. Original images are retained without redrawing or recoloring.
- Launcher component mappings use the available artwork matches; where no reliable Jelly Bean match exists, the existing KitKat artwork remains assigned.
- Mapping source: [Lawnicons](https://github.com/LawnchairLauncher/lawnicons), pinned to `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`. Lawnicons artwork is not included.

## Build

The single **Build Combined Icon Pack Release APK** workflow runs on relevant pushes to `main` or manually from [GitHub Actions](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml).

It imports both artwork sources, merges their drawable catalog and launcher mappings, builds the optimized Gradle `release` variant, and uploads one artifact:

`insomdroid-combined-icon-pack-release`

The artifact is retained for one day. PNG artwork is preserved as supplied; R8 code shrinking and Android resource shrinking are enabled, with all icon drawables explicitly retained because launcher metadata references drawable names dynamically.

## Compatibility

- Minimum SDK: Android 10 (API 29).
- Compile SDK / Target SDK: 36.
- Java: 17.

## Attribution

See [Jelly Bean artwork attribution](docs/HOLOKAT_ATTRIBUTION.md), [Lawnicons attribution](docs/LAWNICONS_ATTRIBUTION.md), and the included [Apache License 2.0](third_party/lawnicons/LICENSE). Acknowledgement does not imply that a third-party redistribution license has been verified.

## Build history cleanup

Use the manual **Cleanup Workflow History** workflow to retain the three newest completed workflow runs across the repository and delete older completed runs. In-progress runs are not deleted.
