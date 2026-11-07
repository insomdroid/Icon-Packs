# Nothink Design Guide

> This document is the source of truth for Nothink artwork decisions. When implementation choices are unclear, return here before changing artwork, generator logic, mappings, or validation.

**Status:** Approved visual direction; implementation is in progress.  
**Applies to:** `pack-nothing`, its artwork generator, generated normal icons, themed icons, previews, and validation.

## 1. Design direction

Nothink combines the graphic character of Nothing OS 2.0/3.0 with the refinement and restraint of Nothing OS 5.0. The result must feel modern while retaining a clear, distinctive monochrome graphic identity.

Reference material:
- [Nothing OS](https://nothing.tech/nothing-os)
- [Nothing OS evolution — Nothing Community](https://nothing.community/d/61774-nothing-os-evolution)

These references inform the visual direction; Nothink remains an independent, unofficial project and must not copy proprietary Nothing artwork.

## 2. Approved visual decisions

| Property | Approved direction |
|---|---|
| Era / inspiration | A considered blend of Nothing OS 2.0/3.0 and Nothing OS 5.0 |
| Overall character | Modern |
| Symbol construction | Hybrid: solid shapes combined with outline strokes |
| Stroke and shape weight | Medium |
| Geometry | Balanced: use straight edges and controlled curves according to the object |
| Collection consistency | One coherent visual family |
| Per-icon variation | Controlled; silhouettes may differ when the app identity requires it |
| Abstraction | Recognizable simplification; preserve the app's recognizable meaning |
| Normal icon background | Pure black, full-bleed tile; launcher applies its icon shape mask |
| Normal icon glyph | Pure white, ensuring contrast in light and dark launcher surfaces |
| Color palette | No baked-in glyph color for themed assets; no red accents, gradients, shadows, or colored decoration |
| Dot-matrix | Not used |
| Canvas composition | Medium / balanced; preserve comfortable transparent space |
| Silhouette | Complete and recognizable; no accidental or decorative clipping |
| Artwork method | Custom artwork, designed specifically for each app identity |
| Relationship to original app logo | Hybrid: retain a distinctive original mark when it works; simplify or reinterpret it when needed to fit Nothink |

## 3. Construction rules

1. Use a shared 24 × 24 conceptual grid as the starting construction system. Optical corrections are allowed when needed.
2. Keep stroke weight medium and consistent. Solid areas and outline strokes must feel like parts of the same design system.
3. Use balanced geometry. Do not force every app into the same corner radius, silhouette, or primitive.
4. Keep the symbol optically centered and medium in scale. Do not force identical mathematical bounding boxes on circular, tall, or wide symbols.
5. Preserve enough negative space for the symbol to remain legible at small launcher sizes.
6. Design each app symbol individually. Reusing one generic category pictogram for unrelated apps is not acceptable.
7. Never add arbitrary dots, red indicators, decorative marks, or dot-matrix texture.
8. Never crop a symbol merely to make it look more dynamic. Any crop must be an intentional, app-specific part of an approved design.
9. Prefer a simplified recognizable app mark where it is distinctive and suitable. Otherwise create an original Nothink interpretation that still communicates the app's identity.
10. Do not infer that separate resource filenames make artwork unique. The actual visual silhouette and construction must be reviewed.

## 4. Normal and themed artwork

### Normal artwork

- Use a pure-black full-bleed tile background with a pure-white glyph. This gives classic icon-pack launchers such as Nova reliable contrast in both light and dark modes.
- The launcher may clip the square tile to its configured icon shape.
- Keep the foreground symbol itself monochrome, with no gray, red, gradients, shadows, or colored decoration.
- Solid and outline components follow the same medium-weight construction system.
- The generated Android layer-list wrapper combines the black background and white-tinted transparent glyph mask; the glyph mask is stored once and reused by themed icons.

### Themed artwork

- Transparent background.
- Single monochrome alpha silhouette suitable for launcher tinting.
- No baked-in color, fixed background, red accent, or decorative dot-matrix.
- Themed artwork must preserve the identity and silhouette of its corresponding normal icon.

The app's own adaptive launcher icon is separate from the app icons in the pack. Its foreground, background, and monochrome layers must be reviewed independently. The appfilter's normal icon wrapper is also separate from the transparent monochrome mask used for Android themed icons.

## 5. Custom artwork workflow

Every icon must pass through these stages:

1. **Identify:** confirm the exact app name, package, and mapped drawable.
2. **Inspect identity:** review the app's original mark where available and decide whether to retain, simplify, or reinterpret it.
3. **Design:** create an app-specific symbol using the approved Nothink construction rules.
4. **Review:** inspect the actual rendered artwork on both light and dark launcher surfaces and at small sizes.
5. **Validate:** check transparency, neutral alpha-mask glyphs suitable for Android theme tinting, complete silhouette, optical balance, and consistency with approved benchmark icons.

The generator is a production tool, not a substitute for icon design. It must not silently assign the same generic category glyph to unrelated apps or invent decorations from hashes or random values.

## 6. Benchmark set

The first design benchmark should cover six mapped app identities from the pinned Lawnicons mapping source. These are selected as design subjects only; Lawnicons is used for component mapping, not as a source of artwork.

| Benchmark | App identity | Package |
|---|---|---|
| Camera | Google Camera | `com.google.android.GoogleCamera` |
| Phone | Google Phone | `com.google.android.dialer` |
| Browser | Google Chrome | `com.android.chrome` |
| Calendar | Google Calendar | `com.google.android.calendar` |
| Music | Spotify | `com.spotify.music` |
| Settings | Android Settings | `com.android.settings` |

The corresponding source mappings include `generic_camera`, `google_phone`, `google_chrome`, `google_calendar`, `spotify`, and `generic_settings`. These resource names are mapping identifiers, not instructions to reuse Lawnicons artwork.

Benchmark artwork must be custom-designed and reviewed before its construction rules are propagated to the remaining collection. If a source mapping changes, verify the package and drawable again rather than guessing.

## 7. Validation and acceptance criteria

An artwork set is not accepted merely because the APK compiles. Review must confirm:

- Normal appfilter icons render as a pure-black tile with a pure-white glyph, retaining contrast in dark mode.
- Themed icons use transparent neutral alpha-mask pixels and a single monochrome glyph suitable for system/launcher tinting.
- No red pixels, gray fills, gradients, shadows, or dot-matrix details are present.
- No accidental clipping or unexplained decorative marks appear.
- The symbol is recognizable at launcher size.
- The six benchmark icons form one coherent family without becoming duplicate generic pictograms.
- Each additional app has an individually considered symbol or an explicitly reviewed logo adaptation.
- Mapping coverage and generated-resource coverage are reported separately from visual-design approval.

A passing automated check cannot replace visual review.

## 8. Implementation status

The generator stores one transparent neutral alpha-mask WebP per pictogram. Standard appfilter entries use generated layer-list wrappers that place the mask as a white glyph on a pure-black tile, so icons remain visible in dark mode even in launchers that do not tint classic icon-pack artwork. Android themed-icon mappings point directly to the transparent mask and remain system-tintable. The six benchmark drawable identifiers have individually authored artwork: `generic_camera`, `google_phone`, `google_chrome`, `google_calendar`, `spotify`, and `generic_settings`.

**The collection is not yet fully custom-designed.** The remaining mapped apps still use the legacy semantic-family artwork, including a hash-varied abstract fallback. Those assets are not approved as final custom artwork under this guide. A successful APK build or automated color/transparency check does not mean the full collection has passed visual design review. Do not describe the full pack as complete until every mapped identity has been individually reviewed and its artwork replaced or explicitly approved.

When uncertain, follow this guide and preserve the user's approved decisions. Do not reintroduce removed elements without explicit approval.
