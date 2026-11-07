# Nothink 100-app trial: JusIcons generator adaptation

This trial adapts the build-time icon-generation approach and monochrome processing pipeline from [JusIcons](https://github.com/shubh72010/JusIcons).

## Reused processing
- Adaptive icon normalization uses the foreground layer and excludes the adaptive background.
- The MonoProcessor luminance histogram, fCombine, iPick, quadratic alpha remap, binary mask, centered-square crop and visual scale are ported from JusIcons.
- The generator runs at build time and writes one Android Vector Drawable per app.
- Launcher components are read from each APK manifest and written to appfilter.xml.

## Deliberate differences
- Each app's actual launcher icon is extracted from its APK.
- No generated letter, category glyph, hash-based shape, or synthetic fallback is used.
- APK files are temporary CI inputs and are not committed to this repository.
- The initial catalog targets 50 Google apps and 50 popular third-party apps.
- A failed or unavailable APK is reported as failed, never replaced with a fake icon.

## Sources and licensing
The generator adapts the GPL-3.0-licensed JusIcons project:
https://github.com/shubh72010/JusIcons

The GPL-3.0 license text is included at third_party/jusicons/LICENSE. Generated artwork is derived from the respective application icons. APKs are downloaded only for extraction during CI and are not redistributed by this workflow. Trademark and artwork rights remain with their respective owners; this trial does not claim that extracted artwork is public domain or freely relicensable.

APK source endpoint:
https://d.apkpure.com/b/APK/{package}?version=latest

The CI report records each package, outcome, APK SHA-256, source URL, drawable name and launcher component mapping.
