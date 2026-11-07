# Insomdroid Icon Packs

Independently installable Android icon pack APKs. Development is currently focused on the KitKat theme.

## Active theme

- **KitKat** — original Android 4.4-inspired vector artwork.
- 32 original KitKat-style drawable assets.
- 2,073 unique launcher component mappings adapted from Lawnicons' upstream `appfilter.xml`.
- Minimum SDK: Android 10 (API 29).
- Compile/Target SDK: 36.

## Build KitKat

1. Open **Actions**.
2. Select **Build KitKat Icon Pack**.
3. Run the workflow on `main`.
4. Download the `kitkat-icon-pack` artifact after the workflow succeeds.

## Mapping source and attribution

Application package/activity mappings are adapted from [LawnchairLauncher/lawnicons](https://github.com/LawnchairLauncher/lawnicons), pinned to source commit `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`.

The mapping records are translated to this project's original KitKat artwork; Lawnicons' SVG artwork is not included. See [Lawnicons attribution](docs/LAWNICONS_ATTRIBUTION.md) and the included [Apache License 2.0](third_party/lawnicons/LICENSE).

Mapping coverage depends on the app package and launcher activity installed on the device. Some upstream component IDs may become outdated as applications change.

## Project structure

The repository retains the planned separate theme modules and catalog foundation. They are not part of the active build while KitKat is being completed.
