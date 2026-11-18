# Audit 137 Unmapped Jelly Bean Artwork

Audit basis:
- Source: `holokat-archive-mapping-report`, GitHub Actions run `44293995477`.
- Current component catalogue: `pack-kitkat/src/main/res/xml/appfilter.xml` (2,074 component entries, 286 distinct display labels).
- Current importer: `scripts/import_holokat_icons.py`.
- Result: 137 unmapped archive entries, representing 132 artwork labels after accounting for five repeated/alternate entries in the second archive.

## Decision rules

1. Do not invent package names or launcher Activity classes.
2. Do not map a service, settings panel, keyboard, widget, or feature sub-screen as though it were a normal launchable app.
3. Keep valid artwork in the pack even when it has no safe component mapping. An unmapped drawable is preferable to a false-positive icon.
4. Add a component only after its package and launcher Activity are verified from an authoritative source or a real APK manifest.
5. Existing apps in `appfilter.xml` keep their current mapping unless an exact package/activity match justifies a change.

## A. Candidate application artwork — retain, but do not auto-map yet

These are recognizable apps or app families, but the current appfilter does not provide a verified matching launcher component for the archive artwork. They need a package/activity check before mapping.

| Artwork | Audit decision | Reason |
|---|---|---|
| Amazon | Candidate | Real app, but no verified Amazon launcher component in the current catalogue |
| Analytics | Candidate | Ambiguous Google Analytics branding/product generation |
| Arts & Culture | Candidate | Real Google app; verify current package/activity |
| Datally | Candidate | Real historical Google app; verify whether still distributed/launchable |
| Find My Device | Candidate | Real Google app; verify package/activity and avoid confusing with system settings |
| Galaxy Store | Candidate | Real Samsung app; OEM package/activity varies |
| Health Connect | Candidate | Real app/system integration; verify actual launcher entry |
| Netflix (archive filename: Netfilx) | Candidate | Real app, but spelling in archive is incorrect and package/activity is not in this catalogue |
| Read Along | Candidate | Real Google app; verify current package/activity |
| Socratic | Candidate | Real Google app; verify current package/activity |
| Twitter | Candidate | Real app branding is now X; do not assume the historical package/activity |
| Uptodown | Candidate | Real third-party store; verify exact launcher component |
| YouTube Creator Studio | Candidate | Historical branding; current product is YouTube Studio, so verify current app identity |
| Google | Candidate | Ambiguous generic Google artwork; must distinguish Google app from Google Settings and Google Play services |
| Google IO | Candidate | Event app artwork; verify whether a current launcher component exists |
| My Business | Candidate | Product branding changed to Google Business Profile; do not reuse old package assumptions |
| Read Along | Candidate | Retained once; archive contains one artwork entry |
| Remote Desktop | Candidate | Ambiguous product name; could refer to Chrome Remote Desktop or another client |
| Screenwise Meter | Candidate | Historical research/measurement app; not a general launcher target |
| Web Store | Candidate | Likely Chrome Web Store branding, generally not a standalone Android app |
| Watch | Candidate | Ambiguous: Android Wear/Watch app versus a generic watch utility |
| Buds | Candidate | Ambiguous product label; likely companion app/device UI rather than a unique app identity |
| One | Candidate | Too generic to identify a package safely |
| Offers | Candidate | Ambiguous/legacy Google Offers branding |
| Travel | Candidate | Ambiguous legacy Google travel product; verify exact app identity |
| Trends | Candidate | Google Trends is primarily a web product, not necessarily a launcher app |
| Trips | Candidate | Google Trips was discontinued; do not map to a current app without evidence |
| Bookmark | Candidate | Generic feature name, not a unique app |
| Local | Candidate | Ambiguous historical Google Local/Places branding |
| Places | Candidate | Historical Google Places feature/product; not enough to identify a current launcher app |
| My Maps | Candidate | Real Google product; verify whether the Android app has a launcher activity in the target catalogue |
| Street View | Candidate | Real Google app/product; verify current package/activity |
| Cast | Candidate | May be a Cast settings/receiver feature rather than a standalone app |
| Chromecast | Candidate | Device/service branding; distinguish companion app from system receiver |
| Chromecast Built-In | Candidate | System receiver/service, not normally a launcher app |
| Android TV | Candidate | Platform/system branding; not a unique phone launcher app |
| Android TV Home | Candidate | TV system home app; irrelevant to ordinary phone app drawer unless explicitly supported |
| Android TV Launcher | Candidate | TV launcher component; do not map as a phone app |
| Live Channels | Candidate | Android TV app; verify target device relevance |
| Backdrop Daydream | Candidate | Chromecast/Android TV ambient display feature, not a normal app |
| ARCore | Candidate | Runtime/service may not expose a normal launcher activity |
| ARCore Elements | Candidate | Sample/demo content; not a general app |
| AIY Projects | Candidate | Hardware/demo ecosystem branding; verify exact app identity |
| Creative Preview | Candidate | Ambiguous developer/advertising tool; verify before mapping |
| Cloud Search | Candidate | Enterprise Google app; verify exact package and launcher activity |
| Project Fi | Candidate | Historical Google Fi branding; verify current package/activity before using old artwork |
| Google Settings | Candidate | Often a system settings entry or Google Play services component, not a standalone app |
| Assistant Go | Candidate | Historical lightweight Assistant app; verify whether it remains separately launchable |
| Goggles | Candidate | Discontinued Google Goggles app |
| Hangouts | Candidate | Retired product; do not map to Google Chat or Meet automatically |
| Hangouts Dialer | Candidate | Retired companion app; do not map to Google Phone |
| G+ Messenger | Candidate | Retired Google+ feature/app |
| G+ Photos | Candidate | Retired Google+ Photos branding; do not confuse with Google Photos |
| Currents | Candidate | Retired Google+ successor; not Google News |
| Picasa | Candidate | Discontinued product; not Google Photos |
| Latitude | Candidate | Discontinued Google location-sharing product |
| Inbox | Candidate | Discontinued Gmail alternative; do not map to Gmail by assumption |
| Market | Candidate | Legacy Android Market branding; modern Play Store is not the same artwork |
| Play Magazines | Candidate | Legacy product, later Google Play Newsstand; discontinued |
| Play Android Apps | Candidate | Store category/branding, not a unique installed app |
| Play Android Games | Candidate | Store category/branding, not a unique installed app |
| Play Developer Console | Candidate | Developer Console branding; verify current Play Console app identity |
| Play Protect | Candidate | Google Play services/security surface, not normally a standalone app |
| Quickoffice | Candidate | Discontinued office suite; do not map to Docs/Sheets automatically |
| Sites | Candidate | Google Sites is primarily a web product; no verified Android launcher target |
| AdWords Express | Candidate | Historical advertising product branding; not a current general consumer app |
| Flash Player | Candidate | Obsolete Android plugin; do not map |
| Admin | Candidate | Ambiguous administrative/system app label; package unknown |
| Support | Candidate | Generic support app label; package unknown |
| Support Services | Candidate | System/OEM service label; not a unique app identity |
| Google Settings | Candidate | Counted once; same ambiguity applies |

## B. Platform, system, input-method, and utility artwork — keep unmapped

These names describe Android components, device services, settings surfaces, input methods, widgets, or hardware integration. They should not be assigned to unrelated app icons.

- Accessibility
- Accessibility Scanner 2
- Android Beam
- Android for Work
- Android Wear
- Android
- Application Package
- Apps Device Policy
- Device Policy
- Data Transfer & Restore
- SIM Manager
- NFC Services
- Camera Services
- Camera ALT
- Camera One
- Cantonese Input
- Cantonese Keyboard
- Hindi Input
- Hindi Keyboard
- Indic Keyboard
- Japanese Input
- Japanese Keyboard
- Korean Input
- Korean Keyboard
- Pinyin Input
- Pinyin Keyboard
- Zhuyin Input
- Zhuyin Keyboard
- Handwriting Keyboard
- Keyboard
- Drawer
- Launcher
- Widget
- Wallpapers
- Voice Dialer
- Quick Contacts Dialer
- Quick Contacts Mail
- Switch Access
- Talk
- TalkBack
- VR Services
- Jelly Bean
- Data Transfer & Restore
- Admin
- Application Package
- Cloud Print
- Cloud Print 2

## C. Feature-specific artwork — keep as artwork, not standalone app mappings

These are sub-features or alternate entry points. Mapping them to the parent app would make the pack less accurate unless the archive icon is confirmed to be the intended parent-app icon.

- Gmail Offline
- Gmail Widget
- Translate Camera
- Translate Community
- Translate Draw
- Translate Keyboard
- Translate Voice
- Cardboard Camera
- Movie Studio
- Google Settings
- Fast Pair Validator
- Backdrop Daydream
- Creative Preview
- Compose Design Catalog
- Cloud Search
- Data Transfer & Restore

## D. Duplicate/alternate archive entries

The following five are second-archive copies/alternate entries and should not be counted as five additional unique app identities:

- Accessibility (second archive copy)
- Cloud Print (second archive copy)
- Navigation Go (second archive copy)
- Navigation (second archive copy)
- Accessibility Scanner (second archive artwork)

The importer should retain the unique image bytes only when hashes differ; it should not create duplicate component mappings just because a second archive contains another copy.

## E. Mapping decisions for this pass

- **New package/activity mappings added: 0.** No package/activity was added from an artwork label alone.
- **False-positive mappings avoided:** retired services, Android system surfaces, keyboard/input methods, widgets, and TV-only components remain unmapped.
- **Artwork retained:** all 137 report entries remain available for visual review; the five alternate/duplicate entries are documented separately.
- **Next safe mapping pass:** verify candidate apps against their actual APK manifests or authoritative package/activity catalogues, then add only exact launcher activities. In particular, Google apps with changed branding (Google Trips, Inbox, Hangouts, G+, Project Fi, My Business, AdWords Express) must not be redirected to modern replacements without an explicit identity decision.

## Build verification

The archive-import/build workflow `44293995477` completed successfully. The combined release artifact is `insomdroid-combined-icon-pack-release` (artifact ID `14422901849`, 25,252,103 bytes). This confirms the importer and APK build complete; it does not mean all 137 artwork entries have valid launcher mappings.
