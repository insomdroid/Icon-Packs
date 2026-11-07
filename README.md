# Insomdroid Icon Packs

Independently installable Android icon pack APKs. Development is currently focused on the KitKat theme.

## Active theme

- **KitKat** — the active theme module. Eight built-in app icons are now imported from original AOSP Android 4.4.4 resources; other artwork remains temporary until period-correct sources are verified.
- 2,073 unique launcher component mappings adapted from Lawnicons' upstream `appfilter.xml`.
- Minimum SDK: Android 10 (API 29).
- Compile/Target SDK: 36.

## Automatic build

The **Build KitKat Release APK** workflow runs automatically when build-related files are pushed to `main`.

It skips commits that only change:
- `README.md` or Markdown documentation.
- Files under `docs/`.
- Reference images under `references/`, `reference/`, `reference-images/`, `screenshots/`, `Screenshot/`, or `assets/references/`.

You can also start a build manually from [GitHub Actions](https://github.com/insomdroid/Icon-Packs/actions/workflows/build-icon-packs.yml).

The workflow builds the Gradle **release** variant and uploads the signed `kitkat-release-apk` artifact for **1 day**. Artifact compression is disabled to avoid wasting time recompressing an APK.

> **Temporary signing:** each workflow run generates a fresh temporary release keystore. The APK is signed and can be installed, but a later build uses a different signing key, so it cannot update an installation signed by an earlier run. This is a temporary development setup, not suitable for publishing updates.

## KitKat artwork status

The release workflow imports eight original Android 4.4.4 AOSP app icons (Messaging, Settings, Camera, Calendar, Calculator, Email, Browser, and Downloads) from the pinned `android-4.4.4_r2` source tag before building. The remaining icons are still temporary artwork; this is a partial authentic set, not yet a complete KitKat-era collection. See `third_party/aosp-android-4.4.4/README.md` for source and license details.

## Mapping source and attribution

Application package/activity mappings are adapted from [LawnchairLauncher/lawnicons](https://github.com/LawnchairLauncher/lawnicons), pinned to source commit `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`.

The mapping records are translated to this project's original KitKat artwork; Lawnicons' SVG artwork is not included. See [Lawnicons attribution](docs/LAWNICONS_ATTRIBUTION.md) and the included [Apache License 2.0](third_party/lawnicons/LICENSE).

Mapping coverage depends on the app package and launcher activity installed on the device. Some upstream component IDs may become outdated as applications change.

## Project structure

The repository retains the planned separate theme modules and catalog foundation. They are not part of the active build while KitKat is being completed.
