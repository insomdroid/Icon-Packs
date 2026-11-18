# Audit 137 Unmapped Jelly Bean Artwork

## Scope and evidence

- Source report: GitHub Actions run `44293995477`, artifact `holokat-archive-mapping-report`.
- Archive scan: 265 unique image files; 128 artwork labels mapped; 137 report entries remain unmapped.
- Current target catalogue: `pack-kitkat/src/main/res/xml/appfilter.xml` contains 2,074 component entries and 286 distinct display labels.
- Code reviewed: `scripts/import_holokat_icons.py`.

Important distinction: “unmapped” means the importer did not establish a safe link between that artwork label and a launcher component. It does **not** prove that the artwork is useless, nor that no app with a similar name exists.

## Per-artwork decision

For every entry below, the safe decision in this pass is **retain the artwork, do not invent a component mapping**. The archive label alone does not prove the installed package name or launcher Activity. This is especially important for system services, input methods, widgets, retired Google products, and products whose branding changed.

| # | Artwork label from archive | Classification / mapping note |
|---:|---|---|
| 1 | Accessibility | Android accessibility feature/system surface; not a verified standalone app |
| 2 | Admin | Ambiguous administrative/system label; package identity unknown |
| 3 | AdWords Express | Legacy advertising product branding; no verified current launcher component |
| 4 | AIY Projects | Hardware/demo ecosystem branding; no verified launcher component |
| 5 | Amazon | Candidate app, but exact package and launcher Activity are not in this catalogue |
| 6 | Analytics | Ambiguous Analytics branding; exact product/package not established |
| 7 | Android Beam | Android platform feature; not a standalone launcher app |
| 8 | Android for Work | Enterprise/platform branding; no verified standalone launcher target |
| 9 | Android TV Home | TV system home app; not a phone launcher mapping |
| 10 | Android TV Launcher | TV launcher component; not a normal phone app |
| 11 | Android TV | Platform/product branding; identity too broad for a component mapping |
| 12 | Android Wear | Historical platform branding; not a standalone app identity |
| 13 | Android | Generic platform artwork; not a unique app |
| 14 | Application Package | Android package/system component; not a normal launcher app |
| 15 | Apps Device Policy | Device policy/system surface; exact launcher activity not established |
| 16 | ARCore Elements | Demo/sample content; not a general app mapping |
| 17 | ARCore | Runtime/service; verify launcher visibility before mapping |
| 18 | Arts & Culture | Candidate Google app; exact package/activity not verified in current catalogue |
| 19 | Assistant Go | Historical/lightweight Assistant branding; separate launcher target not verified |
| 20 | Backdrop Daydream | Ambient display/Chromecast feature, not a normal app |
| 21 | Bookmark | Generic feature label; no unique package identity |
| 22 | Buds | Ambiguous companion/device label; exact app identity unknown |
| 23 | Camera ALT | Alternate camera artwork; no unique app identity |
| 24 | Camera One | Ambiguous camera app label; package/activity not established |
| 25 | Camera Services | Platform service, not a normal launcher app |
| 26 | Cantonese Input | Input method; should not be mapped as a normal app |
| 27 | Cantonese Keyboard | Keyboard/input method; should not be mapped as a normal app |
| 28 | Cardboard Camera | Historical/specialized camera app; exact launcher component not verified |
| 29 | Cast | Cast feature/settings/receiver identity is ambiguous |
| 30 | Chromecast Built-In | Receiver/system service; not a normal launcher app |
| 31 | Chromecast | Device/service branding; distinguish companion app from receiver |
| 32 | Cloud Print | Discontinued Google service; do not map to an unrelated print app |
| 33 | Cloud Search | Enterprise Google app; package/activity not verified |
| 34 | Communities | Ambiguous Google+ Communities-era branding; likely retired feature |
| 35 | Compose Design Catalog | Developer sample/catalog app; not a consumer app mapping |
| 36 | Creative Preview | Ambiguous preview/developer/advertising tool; package not established |
| 37 | Currents | Retired Google product; do not redirect to Google News |
| 38 | Data Transfer & Restore | Setup/transfer utility or system surface; not a verified standalone app |
| 39 | Datally | Historical Google data-management app; current launcher component not verified |
| 40 | Device Policy | Enterprise/system policy app; exact package/activity not verified |
| 41 | Drawer | Launcher UI feature/artwork, not a separate installed app |
| 42 | Fast Pair Validator | Developer/test utility; not a general consumer app |
| 43 | Find My Device | Candidate Google app; exact package/activity needs verification |
| 44 | Flash Player | Obsolete Android plugin; do not map |
| 45 | G+ Messenger | Retired Google+ feature/app; do not map to Google Chat |
| 46 | G+ Photos | Retired Google+ feature; do not confuse with Google Photos |
| 47 | Galaxy Store | Candidate Samsung app; OEM package/activity not verified here |
| 48 | Gmail Offline | Gmail feature/legacy offline app identity; do not assume it is the Gmail launcher icon |
| 49 | Gmail Widget | Widget, not an app launcher component |
| 50 | Goggles | Discontinued Google Goggles app |
| 51 | Google IO | Event app branding; current package/activity not verified |
| 52 | Google Settings | Often a system/Play services settings surface; not a verified standalone app |
| 53 | Google | Generic Google app artwork; must distinguish Google app from Settings/Play services |
| 54 | Handwriting Keyboard | Input method; not a normal app mapping |
| 55 | Hangouts Dialer | Retired companion app; do not map to Google Phone |
| 56 | Hangouts | Retired product; do not map to Chat or Meet automatically |
| 57 | Health Connect | Candidate app/system integration; actual launcher visibility needs verification |
| 58 | Health Studies | Research app; package/activity not verified |
| 59 | Hindi Input | Input method; not a normal app mapping |
| 60 | Hindi Keyboard | Keyboard/input method; not a normal app mapping |
| 61 | Inbox | Discontinued Gmail alternative; do not map to Gmail by assumption |
| 62 | Indic Keyboard | Keyboard/input method; not a normal app mapping |
| 63 | Japanese Input | Input method; not a normal app mapping |
| 64 | Japanese Keyboard | Keyboard/input method; not a normal app mapping |
| 65 | Jelly Bean | Android version/mascot artwork, not an app |
| 66 | Keyboard | Generic input-method artwork; not a unique app |
| 67 | Korean Input | Input method; not a normal app mapping |
| 68 | Korean Keyboard | Keyboard/input method; not a normal app mapping |
| 69 | Latitude | Discontinued Google location-sharing product |
| 70 | Launcher | Launcher/system UI component; not a separate app mapping |
| 71 | Live Channels | Android TV app; target-device relevance and package need verification |
| 72 | Local | Ambiguous legacy Google Local/Places product label |
| 73 | Market | Legacy Android Market branding; not automatically equivalent to Play Store |
| 74 | Movie Studio | Legacy Android media utility; package/activity not verified |
| 75 | My Business | Historical Google My Business branding; now Google Business Profile, identity changed |
| 76 | My Maps | Candidate Google product; launcher component not verified in current catalogue |
| 77 | Navigation Go | Legacy/navigation product variant; exact package/activity not verified |
| 78 | Navigation | Ambiguous legacy Google Navigation artwork; do not assume Google Maps component |
| 79 | Netfilx | Netflix artwork with misspelled archive filename; exact package/activity not in catalogue |
| 80 | NFC Services | Platform service; not a normal launcher app |
| 81 | Now Launcher | Historical Google Now Launcher; retired, not the Google app |
| 82 | Offers | Ambiguous/legacy Google Offers branding; no verified launcher component |
| 83 | One | Generic/ambiguous product label; no package identity |
| 84 | Picasa | Discontinued Google photo product; do not map to Google Photos |
| 85 | Pinyin Input | Input method; not a normal app mapping |
| 86 | Pinyin Keyboard | Keyboard/input method; not a normal app mapping |
| 87 | Places | Historical Google Places product/feature; no verified current launcher target |
| 88 | Play Android Apps | Play Store category/branding, not a unique installed app |
| 89 | Play Android Games | Play Store category/branding, not a unique installed app |
| 90 | Play Developer Console | Developer Console branding; current Play Console app identity needs verification |
| 91 | Play Magazines | Discontinued Google Play Newsstand-era product |
| 92 | Play Protect | Google Play services/security surface; not a verified standalone launcher app |
| 93 | Project Fi | Historical Google Fi branding; verify current component before using old artwork |
| 94 | Quick Contacts Dialer | Contacts/dialer shortcut or feature; not a unique app identity |
| 95 | Quick Contacts Mail | Contacts/mail shortcut or feature; not a unique app identity |
| 96 | Quickoffice | Discontinued office suite; do not redirect to Docs/Sheets |
| 97 | Read Along | Candidate Google app; exact package/activity not verified |
| 98 | reCAPTCHA | Platform/web verification service, not a launcher app |
| 99 | Remote Desktop | Ambiguous product name; exact app/package not established |
| 100 | Screenwise Meter | Historical research/measurement utility; not a general launcher target |
| 101 | SIM Manager | Platform/OEM system utility; exact launcher component not verified |
| 102 | Sites | Google Sites is primarily a web product; no verified Android launcher target |
| 103 | Socratic | Candidate Google app; exact package/activity not verified |
| 104 | Street View | Candidate Google app/product; exact launcher component not verified |
| 105 | Support Services | Generic system/OEM support service; not a unique app identity |
| 106 | Support | Generic support label; package identity unknown |
| 107 | Switch Access | Android accessibility service/feature; not a normal app mapping |
| 108 | Talk | Historical Google Talk/feature branding; retired |
| 109 | TalkBack | Android accessibility service; not a normal app mapping |
| 110 | Translate Camera | Google Translate feature/entry point; not proven to be a distinct app |
| 111 | Translate Community | Google Translate feature/legacy community surface |
| 112 | Translate Draw | Google Translate feature/entry point |
| 113 | Translate Keyboard | Input/feature surface; not a separate app |
| 114 | Translate Voice | Google Translate feature/entry point |
| 115 | Travel | Ambiguous/legacy Google travel product; exact identity not established |
| 116 | Trends | Google Trends is primarily a web product; no verified Android launcher target |
| 117 | Trips | Discontinued Google Trips; do not map to Maps or Travel automatically |
| 118 | Twitter | Candidate historical Twitter app artwork; branding/package/activity may have changed |
| 119 | Uptodown | Candidate third-party app store; exact launcher component not verified |
| 120 | Voice Dialer | Android system utility; not a normal third-party app mapping |
| 121 | VR Services | Platform/runtime service; not a normal launcher app |
| 122 | Wallpapers | Generic wallpaper picker/service; exact launcher app identity not established |
| 123 | Watch | Ambiguous watch/Android Wear companion label; package unknown |
| 124 | Web Store | Likely Chrome Web Store branding; not a verified standalone Android app |
| 125 | WebView Beta | WebView provider/system component; not a normal launcher app |
| 126 | WebView Canary | WebView provider/system component; not a normal launcher app |
| 127 | WebView Dev | WebView provider/system component; not a normal launcher app |
| 128 | WebView | WebView provider/system component; not a normal launcher app |
| 129 | Widget | Widget artwork/category, not a launcher component |
| 130 | YouTube Creator Studio | Historical branding; current YouTube Studio identity/package needs verification |
| 131 | Zhuyin Input | Input method; not a normal app mapping |
| 132 | Zhuyin Keyboard | Keyboard/input method; not a normal app mapping |
| 133 | Accessibility Scanner (second archive) | Separate second-archive variant; accessibility utility, component not verified |
| 134 | Accessibility (second archive) | Second-archive alternate; do not create a duplicate component mapping |
| 135 | Cloud Print (second archive) | Second-archive alternate of discontinued service; do not map |
| 136 | Navigation Go (second archive) | Second-archive alternate; package/activity not verified |
| 137 | Navigation (second archive) | Second-archive alternate; package/activity not verified |

## Outcome

- **New appfilter components added in this audit: 0.** The archive labels do not contain enough evidence to safely create package/activity mappings.
- **Artwork disposition:** keep all extracted artwork available for visual review; unmapped resources do not break the icon pack.
- **False-positive prevention:** do not map system services, input methods, widgets, TV-only components, retired apps, or sub-features onto unrelated modern apps.
- **Next safe mapping step:** verify a candidate's package and exported launcher Activity from an actual APK manifest or an authoritative upstream component catalogue. Only then add the exact component to `appfilter.xml` and rerun the importer/build.

## Build verification

Workflow run `44293995477` completed successfully. The combined release artifact is `insomdroid-combined-icon-pack-release` (artifact ID `14422901849`, 25,252,103 bytes). This verifies the archive import and APK build, not that all 137 entries have launcher mappings.
