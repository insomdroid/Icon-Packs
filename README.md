# Insomdroid Icon Packs

Independently installable Android icon pack APKs. Development is currently focused on the KitKat theme.

## Active theme

- **KitKat** — original Android 4.4-inspired vector artwork.
- 32 original KitKat-style drawable assets.
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

The workflow builds the Gradle **release** variant and uploads the `kitkat-release-unsigned-apk` artifact for 7 days. Artifact compression is disabled to avoid wasting time recompressing an APK.

> **Signing:** the current project has no release keystore configured. The generated release APK is therefore unsigned and cannot be installed directly. Configure a persistent release signing keystore through GitHub Actions secrets before distributing an installable release APK. Do not use a temporary runner-generated debug key for release updates.

## Mapping source and attribution

Application package/activity mappings are adapted from [LawnchairLauncher/lawnicons](https://github.com/LawnchairLauncher/lawnicons), pinned to source commit `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`.

The mapping records are translated to this project's original KitKat artwork; Lawnicons' SVG artwork is not included. See [Lawnicons attribution](docs/LAWNICONS_ATTRIBUTION.md) and the included [Apache License 2.0](third_party/lawnicons/LICENSE).

Mapping coverage depends on the app package and launcher activity installed on the device. Some upstream component IDs may become outdated as applications change.

## Project structure

The repository retains the planned separate theme modules and catalog foundation. They are not part of the active build while KitKat is being completed.
