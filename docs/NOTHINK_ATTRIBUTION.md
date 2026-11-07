# Nothink Icon Pack — Artwork and Mapping Attribution

Nothink is an independent, unofficial icon pack inspired by the monochrome visual language of Nothing OS. It is not affiliated with, endorsed by, or sponsored by Nothing Technology Limited. Nothing names and marks remain the property of their respective owner.

## Mapping and source artwork

- Project: [Lawnicons](https://github.com/LawnchairLauncher/lawnicons)
- Mapping source: `app/assets/appfilter.xml`
- SVG source directory: `svgs/`
- Pinned source revision: `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`
- License: Apache License 2.0
- License text: [`third_party/lawnicons/LICENSE`](../third_party/lawnicons/LICENSE)

The build downloads the pinned Lawnicons source, retains its app component mapping coverage, and transforms the source SVG glyphs into monochrome Nothink artwork. The standard icon layer uses a near-black circular field with a white glyph. A separate glyph-only layer is generated for compatible wallpaper-tinted themed-icon implementations.

The build fails rather than silently omitting a mapped icon if its source SVG is missing. It also verifies that at least 3,000 app component mappings are generated before packaging.

Modified artwork is generated during the GitHub Actions build and is not downloaded by the installed APK. No Nothing proprietary artwork or Nothing Launcher APK resources are redistributed.

## License notice

Lawnicons is licensed under the Apache License, Version 2.0. The complete license text is included in this repository. Modified generated artwork is identified as a derivative transformation of Lawnicons SVG assets. See the upstream project for its copyright and contributor notices.
