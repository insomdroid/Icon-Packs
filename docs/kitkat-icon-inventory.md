# KitKat Icon Pack — Icon Inventory

## Current implementation

KitKat remains the only active deliverable. The CI importer now downloads eight verified Android 4.4.4 AOSP launcher icons from the `android-4.4.4_r2` source tag and places them in density-specific resource folders. The default XML artwork remains as fallback for all other mapped apps.

- **App mappings:** 2,073 unique component mappings adapted from Lawnicons.
- **Mapping source:** `LawnchairLauncher/lawnicons`, `app/assets/appfilter.xml`, branch `develop`, commit `cd91ff0bd00ff0a6c9d606d1c326b451b6563506`.
- **Build:** `gradle --no-daemon :pack-kitkat:assembleRelease`.
- **Verified artwork:** Contacts, Messages, Settings, Camera, Calendar, Calculator, Mail, and Browser are sourced from AOSP Android 4.4.4. See `third_party/aosp-android-4.4.4/README.md`.
- **Remaining artwork:** other icons are temporary; third-party icons still need historical, app-specific sources. Do not label community artwork as official Android artwork.

## Artwork coverage checklist

- [ ] phone (standalone AOSP Phone source not available at this tag; awaiting verified source)
- [x] contacts (AOSP Contacts)
- [x] messages (AOSP Mms)
- [x] calendar (AOSP Calendar)
- [x] clock (AOSP DeskClock)
- [x] calculator (AOSP Calculator)
- [x] camera (AOSP Camera)
- [x] gallery (AOSP Gallery)
- [x] settings (AOSP Settings)
- [x] files (AOSP DocumentsUI)
- [x] downloads
- [x] browser (AOSP Browser)
- [x] chrome
- [x] maps
- [x] translate
- [x] youtube
- [x] mail (AOSP Email)
- [x] telegram
- [x] instagram
- [x] spotify
- [x] messenger
- [x] whatsapp
- [x] facebook
- [x] soundcloud
- [x] snapchat
- [x] word
- [x] excel
- [x] powerpoint
- [x] onenote
- [x] skype
- [x] pinterest
- [x] hangouts

## Mappings by KitKat artwork

- `messages`: 305 components
- `phone`: 256 components
- `camera`: 203 components
- `contacts`: 169 components
- `whatsapp`: 140 components
- `calculator`: 127 components
- `settings`: 109 components
- `gallery`: 106 components
- `clock`: 104 components
- `calendar`: 100 components
- `files`: 90 components
- `telegram`: 75 components
- `snapchat`: 39 components
- `youtube`: 37 components
- `mail`: 30 components
- `chrome`: 25 components
- `downloads`: 24 components
- `instagram`: 24 components
- `browser`: 21 components
- `spotify`: 21 components
- `facebook`: 16 components
- `maps`: 13 components
- `soundcloud`: 13 components
- `messenger`: 8 components
- `pinterest`: 6 components
- `translate`: 3 components
- `excel`: 2 components
- `onenote`: 2 components
- `powerpoint`: 2 components
- `word`: 2 components
- `skype`: 1 components

## Asset licensing and provenance

The eight imported PNGs come from AOSP repositories that mark the corresponding modules `MODULE_LICENSE_APACHE2`; their source repository names, resource paths, and attribution are listed in `third_party/aosp-android-4.4.4/README.md`. The shared Apache License 2.0 text is included at `third_party/lawnicons/LICENSE`. Remaining community artwork must be clearly distinguished from official Android assets.

## Mapping adaptation notes

1. Lawnicons component IDs and activity class names are preserved from the pinned upstream appfilter.
2. The upstream drawable names are translated to the closest available KitKat artwork in this pack. This keeps the KitKat visual language instead of importing Lawnicons' monochrome SVG artwork.
3. Lawnicons dynamic calendar records are converted to static `calendar` entries because this pack does not include the 31 day-specific dynamic calendar drawables.
4. Duplicate component IDs are collapsed to one entry.
5. Coverage depends on the exact app package and launcher activity installed on a device. Lawnicons mappings are community-maintained and may include outdated activity IDs.
6. The planned expansion list is not a claim that all listed applications have unique artwork. Where a dedicated icon is not yet available, the closest generic KitKat category icon is used.

## Future artwork expansion

- **System/OEM:** Samsung, Xiaomi/Redmi/POCO, OPPO/realme, vivo/iQOO, Motorola, OnePlus.
- **Google:** Play Store, Play Games, Drive, Docs, Sheets, Slides, Keep, Google app, Earth, Street View, YouTube Music, Google Home, Android Auto.
- **Third-party:** X, Threads, Reddit, TikTok, LinkedIn, Discord, LINE, Viber, WeChat, Outlook, Proton Mail, Zoom, Meet, Teams, Signal, Deezer, Tidal, VLC, MX Player, Netflix, Prime Video, Disney+, Twitch, Notion, Trello, Todoist, OneDrive, Dropbox, MEGA, Adobe Acrobat, Canva.
- **Indonesia:** Shopee, Tokopedia, Lazada, Blibli, Bukalapak, Gojek, Grab, DANA, OVO, GoPay, Jenius, Livin' by Mandiri, BRImo, BCA mobile.
- **Games:** Minecraft, Roblox, PUBG Mobile, Mobile Legends, Pokémon GO, Steam.

