# ChatGPT Development Guide — Icon Packs

Repository: https://github.com/insomdroid/Icon-Packs

This guide is the working standard for icon-pack artwork, mappings, Android packaging, and GitHub Actions. Treat the repository and its asset/license records as the source of truth.

## Scope

This repository contains multiple independent icon-pack products and source collections, including Holokat, Nothink, and Nothink2. Keep their artwork, package IDs, mappings, build outputs, and design rules distinct. Do not assume a change for one pack applies to another.

## Non-negotiable working rules

- Work only in this repository. Do not mix code or assets from Dislauncher, Nomina, or Omamu.
- Inspect the current directory structure, package IDs, build scripts, mapping format, asset provenance, licenses, and workflows before editing.
- Prefer small, focused changes on `main` for routine work; do not create a PR unless requested or required.
- Never invent an icon asset, application package name, attribution, license, or mapping.
- Never replace approved artwork or mappings without a clear reason and user approval.
- Do not add generic or unrelated icons merely to increase the supported-app count.
- Keep each icon pack's application ID, launcher integration, versioning, and release artifact identity correct.
- Do not create multiple APKs when the agreed release is one combined APK.
- Verify APK size and contents; do not assume a larger APK means better coverage.

## Artwork quality rules

- An icon should visibly represent the real application, not merely share a generic category.
- Match the selected historical/design reference faithfully. Do not modernize classic artwork unless explicitly requested.
- For monochrome/Nothing-inspired designs, preserve the approved glyph weight, tile/background treatment, negative space, centering, and scale.
- Keep the foreground glyph optically centered and consistently sized. Avoid oversized glyphs, clipping, weak contrast, or invisible icons in dark themes.
- Test themed/adaptive behavior on supported launchers and distinguish maskable artwork from baked backgrounds.
- Adaptive shape and color behavior must follow the actual implementation and launcher capabilities; never promise universal support without testing.
- Avoid near-duplicate icons unless they are intentionally different variants for distinct applications.

## Mapping and coverage workflow

1. Identify the exact application and package name from reliable repository evidence or a verified installed-app/package list.
2. Search existing mappings before adding anything.
3. Inspect the candidate artwork at full resolution and compare it with the actual app identity.
4. Confirm that the asset is relevant, licensed/usable, and not a duplicate.
5. Add the mapping using the repository's existing format and naming conventions.
6. Run validation/build and inspect the generated APK.
7. Report confirmed mapped applications separately from candidates and unsupported applications.

Never infer package names from an app's display name alone. Never report an app as supported until the mapping is included in the built artifact.

## Source and licensing discipline

- Preserve the original source URL, author/creator, license, and required attribution for third-party artwork.
- Keep attribution documents in sync when assets are added, removed, or replaced.
- Do not claim third-party artwork as original work.
- If licensing is unclear, do not include the asset until the uncertainty is resolved.
- Keep original source archives separate from generated/modified assets where the repository structure supports it.

## Build and release workflow

- Inspect the exact workflow file before changing it.
- Confirm which icon-pack APK(s) the workflow is intended to build.
- Build from the repository's pinned/approved asset sources; avoid silently switching upstream versions.
- Check workflow logs, artifact names, package IDs, APK contents, and final file size.
- Install the APK over the previous version when testing updates; do not require uninstalling unless the application ID/signing identity genuinely changed and that change was explicitly intended.
- Test with more than one launcher where launcher compatibility is part of the requirement.
- Do not call a build successful until GitHub Actions reports success. Do not call icon coverage complete until the generated APK has been inspected.

## Copy-ready prompts

### Audit artwork and mappings
> Audit the requested icon-pack collection in this repository. Inspect existing artwork, mappings, package IDs, duplicates, source attribution, and build configuration. Do not edit yet. Return a table of confirmed matches, uncertain candidates, duplicates, and missing mappings with evidence and exact file paths.

### Add approved icons
> Add only the icons and mappings we approved. Preserve the original design character and existing assets. Verify each package name and source/license record. Do not add speculative mappings or unrelated icons. Build the intended APK and report exactly which mappings are included in the artifact.

### Fix visual scale/contrast
> Compare these icon screenshots in light and dark themes. Measure the visible glyph/background balance, centering, margins, and contrast. Identify whether the issue comes from source artwork, adaptive icon XML, scaling configuration, or launcher rendering. Do not enlarge or replace all icons as a blanket fix.

### Diagnose build or APK size
> Inspect the failing workflow and APK contents. Find the first meaningful error or the actual source of unexpected APK growth. Make the smallest targeted fix. Do not delete artwork or change compression blindly. Report before/after APK size and the verified contents.

## Checkpoint template

- Icon pack:
- Package/application ID:
- Last known-good commit:
- Last successful workflow:
- Release APK:
- Confirmed mapped app count:
- Assets added/changed:
- Attribution/license updated:
- Known visual issues:
- Current task:
- Next single task:

## Definition of done

The correct pack builds into the intended APK; every newly claimed mapping is present and points to the correct application; artwork is visually checked at actual launcher size in light and dark conditions; third-party attribution is preserved; and the release artifact and workflow result are verified. If launcher/device testing is incomplete, state that explicitly.
