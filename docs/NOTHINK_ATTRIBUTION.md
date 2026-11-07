# Nothink Icon Pack — Artwork and Mapping Attribution

Nothink is an independent, unofficial icon pack inspired by the monochrome geometric visual language of Nothing OS. It is not affiliated with, endorsed by, or sponsored by Nothing Technology Limited. Nothing names and marks remain the property of their respective owner.

## App mapping source

- Project: [Lawnicons](https://github.com/LawnchairLauncher/lawnicons)
- Mapping file only: `app/assets/appfilter.xml`
- Pinned source revision: `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`
- License: Apache License 2.0
- License text: [`third_party/lawnicons/LICENSE`](../third_party/lawnicons/LICENSE)

The build downloads only the pinned `appfilter.xml` mapping file from Lawnicons. It does not download, read, copy, transform, or package Lawnicons SVG files or other upstream icon artwork. Lawnicons is used strictly to obtain Android component-to-icon mappings.

## Original Nothink artwork

Every Nothink illustration is drawn by the generator in this repository. The artwork direction is **Geometric Solid**: bold, simple, recognizable pictograms; consistent stroke weight, optical size, proportions, spacing, and rounded geometry; a near-black field; white pictogram shapes; restrained signal-red accents; and a small dot-matrix detail used only as an accent.

The generator classifies app names and package identifiers into semantic pictogram families (for example phone, messages, camera, calendar, music, maps, weather, files, security, and calculator). Apps without a reliable semantic match receive an original abstract geometric mark. It does not use generated letter initials as the icon artwork. A transparent monochrome glyph layer is also generated for compatible themed-icon implementations.

The artwork is original Nothink illustration work. It is not extracted from app icons, Lawnicons SVGs, Nothing proprietary artwork, or any other icon pack. The workflow verifies that the generated image files exist for all mapped drawable entries before packaging.

## License notice

Lawnicons is licensed under the Apache License, Version 2.0. Its mapping file is used as an attribution-required mapping reference; no Lawnicons icon illustrations are redistributed in Nothink. The complete upstream license text is included in this repository. Nothink artwork is maintained separately in this project.
