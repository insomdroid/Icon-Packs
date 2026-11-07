# KitKat Icon Pack — Icon Inventory

Status: first implementation batch. KitKat is the only active deliverable; other theme modules are intentionally untouched.

## Original artwork included
- [x] Phone
- [x] Contacts
- [x] Messages
- [x] Calendar
- [x] Clock
- [x] Calculator
- [x] Camera
- [x] Gallery
- [x] Settings
- [x] Files
- [x] Downloads
- [x] Browser
- [x] Chrome
- [x] Maps
- [x] Translate
- [x] Youtube
- [x] Mail
- [x] Telegram
- [x] Instagram
- [x] Spotify
- [x] Messenger
- [x] Whatsapp

## Launcher mappings included
| Group | Applications | Mapping status |
|---|---|---|
| Android / AOSP | Calendar, Calculator, Camera, Clock, Contacts, Phone/Dialer, Files, Downloads, Email, Gallery, Messaging, Settings | Component/activity pairs based on published icon-pack mappings; legacy variants may not exist on current OEM ROMs. |
| Google | Chrome, Maps, Translate, Files by Google, YouTube, Photos, Play Books, Gmail | Component/activity pairs based on published launcher mappings. |
| Third party | Spotify, Instagram, Telegram, Facebook, Messenger, WhatsApp, SoundCloud, Snapchat, Microsoft Word/Excel/PowerPoint/OneNote, Skype, Pinterest, Open Camera | Component/activity pairs based on published launcher mappings. |

## Expansion queue
### Android / Google
Phone variants, Contacts, Messages, Email, Voice Dialer, Calendar, Clock, Calculator, Camera, Gallery, Music, Video, FM Radio, Recorder, Settings, Downloads, Files, Package Installer, Print Spooler, Wallpapers, Documents, Search, Voice Search, Play Store, Play Games, Drive, Docs, Sheets, Slides, Keep, Google app, Google TV, Earth, Street View, YouTube Music, Play Movies, Google Home, Android Auto.

### OEM
- Samsung: Phone, Contacts, Messages, Camera, Gallery, My Files, Calendar, Calculator, Clock, Samsung Internet, Galaxy Store, SmartThings, Voice Recorder, Samsung Notes.
- Xiaomi / Redmi / POCO: Phone, Contacts, Messages, Camera, Gallery, File Manager, Security, Themes, Music, Mi Video, GetApps, Notes.
- OPPO / realme: Phone, Contacts, Messages, Camera, Photos, File Manager, Music, Theme Store, Phone Manager.
- vivo / iQOO: Phone, Contacts, Messages, Camera, Album, iManager, File Manager, Browser, Themes.
- Motorola: Phone, Contacts, Messages, Camera, Gallery, FM Radio, Moto, Device Help.
- OnePlus: Phone, Contacts, Messages, Camera, Gallery, File Manager, Notes, Community.

### Third party
- Social: X, Threads, Reddit, TikTok, Facebook Lite, Messenger Lite, LinkedIn, Discord, LINE, Viber, WeChat, Tumblr.
- Communication: Outlook, Proton Mail, Zoom, Google Meet, Microsoft Teams, Signal, Element.
- Media: YouTube Music, Apple Music, Deezer, Tidal, VLC, MX Player, Netflix, Prime Video, Disney+, Twitch.
- Productivity: Notion, Trello, Todoist, OneDrive, Dropbox, MEGA, Adobe Acrobat, Canva.
- Shopping / Indonesia: Shopee, Tokopedia, Lazada, Blibli, Bukalapak, Amazon, AliExpress.
- Transport / finance / games: Gojek, Grab, DANA, OVO, GoPay, Jenius, Livin' by Mandiri, BRImo, BCA mobile, Minecraft, Roblox, PUBG Mobile, Mobile Legends, Pokémon GO, Steam.

## Verification rules
1. A drawable is supported only when an appfilter component maps to it.
2. Package names alone are insufficient: activity class names differ across app releases and device vendors.
3. OEM mappings will be separate from AOSP mappings.
4. The expansion queue is planned coverage, not a claim that every queued app is already supported.

## Mapping references
- GoogleIcons appfilter: https://github.com/amirzaidi/GoogleIcons/blob/master/app/src/main/res/xml/appfilter.xml
- Community icon-pack appfilter examples: https://github.com/Cordazar/iconpack_template/blob/master/assets/appfilter.xml
- Historical mappings: https://github.com/the-dagger/CrapCons-IconPack/blob/master/app/src/main/res/xml/appfilter.xml
