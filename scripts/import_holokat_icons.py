#!/usr/bin/env python3
"""Merge the supplied Jelly Bean archive artwork into the single KitKat icon pack."""
from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = [
    ROOT / "references/kitkat-archives/Icons jb 1.zip",
    ROOT / "references/kitkat-archives/icons jb2.zip",
]
RES = ROOT / "pack-kitkat/src/main/res"
DRAWABLE_DIR = RES / "drawable-nodpi"
DRAWABLE_XML = RES / "xml/drawable.xml"
APPFILTER_XML = RES / "xml/appfilter.xml"
IMAGE_EXTENSIONS = {".png", ".webp", ".jpg", ".jpeg"}


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def resource_name(filename: str) -> str:
    stem = Path(filename).stem.lower()
    stem = re.sub(r"[^a-z0-9_]+", "_", stem)
    stem = re.sub(r"_+", "_", stem).strip("_")
    if not stem or not stem[0].isalpha():
        stem = "icon_" + (stem or "unnamed")
    return stem[:90]


# Explicit label-to-artwork aliases. Exact filename matches always take priority.
ALIASES = {
    "googlechrome": "chrome",
    "chromebrowser": "chrome",
    "googlechromebeta": "chromebeta",
    "googlechromedev": "chromedev",
    "googlechromecanary": "chromecanary",
    "chromiumbrowser": "chromium",
    "googlecalendar": "calendar",
    "androidcalendar": "calendar",
    "googlecamera": "cameragoogle",
    "gcam": "cameragoogle",
    "googlemessages": "messaging",
    "androidmessages": "messaging",
    "googlephone": "phone",
    "googledialer": "phone",
    "googlemail": "gmail",
    "googlemaps": "maps",
    "googlemapsgo": "mapsgo",
    "googlephotos": "photos",
    "googleplaystore": "playstore",
    "googleplaymusic": "playmusic",
    "googleplaygames": "playgames",
    "googleplaybooks": "playbooks",
    "googleplaymovies": "playmoviestv",
    "googlekeep": "keep",
    "googledrive": "drive",
    "googledocs": "docs",
    "googlesheets": "sheets",
    "googleslides": "slides",
    "googletranslate": "translate",
    "googleyoutube": "youtube",
    "microsoftoutlook": "outlook",
    "outlookmail": "outlook",
    "androidsettings": "settings",
    "aospbrowser": "browser",
    "aospcalculator": "calculator",
    "aospclock": "clock",
    "aospcamera": "camera",
    "aospdownloads": "downloads",
    "aospmusic": "music",
    "filesbygoogle": "filesgo",
    "googlefiles": "filesgo",
    "googlegmail": "gmail",
    "googledocsviewer": "docs",
    "googlecontacts": "contacts",
    "googlevoice": "voice",
    "googleassistant": "assistant",
    "googlemapsnavigation": "navigation",
    "googleearth": "earth",
    "googlefit": "fit",
    "googletranslatecamera": "translatecamera",
    "googlenews": "newsweather",
    "googlekeepnotes": "keep",
    "googlewallet": "wallet",
    "googletv": "googletv",
    "playstore": "playstore",
    "playmusic": "playmusic",
    "playgames": "playgames",
    "playbooks": "playbooks",
    "playmovies": "playmoviestv",
    "androidbeam": "androidbeam",
    "androidtv": "androidtvhome",
    "androidwear": "wear",
    "wearos": "wearos",
    "youtube": "youtube",
    "youtubeandroidtv": "youtubetv",
    "youtubeforandroidtv": "youtubetv",
    "youtubecreatorstudio": "youtubecreatorstudio",
    "youtubemusic": "youtubemusic",
    "youtubekids": "youtubekids",
    "facebookmessenger": "facebookmessenger",
    "messenger": "facebookmessenger",
    "instagramlite": "instagram",
    "whatsappbusiness": "whatsapp",
    "googleplus": "google",
    "google+": "google",
    "gplus": "google",
    "hangoutsdialer": "hangoutsdialer",
    "hangoutsdialer": "hangoutsdialer",
    "gmailgo": "gmailgo",
    "googlego": "googlego",
    "googlenow": "googlenow",
    "googleio": "googleio",
    "google settings": "googlesettings",
    "googlewallet": "wallet",
    "adwords": "adwords",
    "adwordsexpress": "adwordsexpress",
    "androidautolauncher": "androidauto",
    "chromecastbuiltin": "chromecastbuiltin",
    "chromecast": "chromecast",
    "cloudprint": "cloudprint",
    "cloudsearch": "cloudsearch",
    "fmradio": "fmradio",
    "filemanager": "filemanager",
    "findmydevice": "findmydevice",
    "quickoffice": "quickoffice",
    "voiceaccess": "voiceaccess",
    "voicesearch": "voicesearch",
    "voicedialer": "voicedialer",
    "soundrecorder": "soundrecorder",
    "videoplayer": "videos",
    "movieditor": "moviestudio",
    "moviestudio": "moviestudio",
    "email": "email",
    "mail": "mail",
    "browser": "browser",
    "calculator": "calculator",
    "calendar": "calendar",
    "camera": "camera",
    "clock": "clock",
    "contacts": "contacts",
    "downloads": "downloads",
    "messages": "messaging",
    "music": "music",
    "phone": "phone",
    "gallery": "gallery",
    "settings": "settings",
    "files": "files",
    "maps": "maps",
    "translate": "translate",
    "youtube": "youtube",
    "photos": "photos",
    "gmail": "gmail",
    "drive": "drive",
    "chrome": "chrome",
    "keep": "keep",
    "docs": "docs",
    "sheets": "sheets",
    "slides": "slides",
    "skype": "skype",
    "spotify": "spotify",
    "whatsapp": "whatsapp",
    "facebook": "facebook",
    "instagram": "instagram",
    "snapchat": "snapchat",
    "twitter": "twitter",
    "telegram": "telegram",
    "dropbox": "dropbox",
    "outlook": "outlook",
    "pinterest": "pinterest",
    "soundcloud": "soundcloud",
    "viber": "viber",
    "discord": "discord",
    "tiktok": "tiktok",
}


# Semantic fallbacks for catalog labels whose app names differ from the
# Jelly Bean artwork filenames. Every target below is an existing archive asset.
SEMANTIC_RULES = [
    (("calendar", "calender"), "calendar"),
    (("calculator", "calc"), "calculator"),
    (("clock", "watch", "time"), "clock"),
    (("camera", "gcam"), "camera"),
    (("dialer", "phone", "calling", "caller"), "phone"),
    (("contact", "people"), "people"),
    (("gallery", "album"), "gallery"),
    (("photo", "picture", "wallpaper"), "photos"),
    (("filemanager", "fileexplorer", "myfiles", "files"), "files"),
    (("download", "downloader"), "downloads"),
    (("browser", "webview", "chromium"), "browser"),
    (("map", "navigation", "osm2gmaps"), "maps"),
    (("message", "messenger", "sms", "chat", "telegram", "talk", "gram"), "messages"),
    (("email", "mail", "inbox"), "email"),
    (("music", "audio", "spotify", "soundcloud"), "music"),
    (("youtube", "yt"), "youtube"),
    (("setting", "configuration", "quicksettings"), "settings"),
    (("video", "movie", "stream"), "videos"),
]

EXPLICIT_ALIASES = {
    "acrphone": "phone", "aigallery": "gallery", "aospclock": "clock",
    "aospdialer": "phone", "asuscalculator": "calculator",
    "asuscalendar": "calendar", "asusgallery": "gallery",
    "asuscallingscreen": "phone", "asusdigitalclockwidget": "clock",
    "ahafast": "downloads", "alcatelcontacts": "people",
    "alcatelphone": "phone", "alightphone": "phone",
    "androidhiddensettings": "settings", "androidquicksettings": "settings",
    "androidfiles": "files", "appinfomanager": "settings",
    "axetscallrecorder": "soundrecorder", "bitcalculator": "calculator",
    "bromitedev": "chromium", "calcu": "calculator", "calcyou": "calculator",
    "calendarplanner": "calendar", "callassistant": "phone",
    "callrecorder": "soundrecorder", "callerid": "phone",
    "camera2": "camera", "camerawatch": "camera",
    "chromium": "chromium", "chronos": "clock",
    "clevcalc": "calculator", "clockmaster": "clock",
    "clockyou": "clock", "coloroscalendar": "calendar",
    "colorosdownloads": "downloads", "colorosmyfiles": "files",
    "colorosodialer": "phone", "colorosphotos": "photos",
    "contactsphonecall": "people", "dialer": "phone",
    "downloadvideonowatermark": "downloads", "easyphone": "phone",
    "everdialer": "phone", "fossbrowser": "browser",
    "fileexplorer": "files", "filemanager": "filemanager",
    "filemanagershortcut": "filemanager", "filesgoogleshortcutslauncher": "filesgo",
    "filesbygoogle": "filesgo", "filesshortcut": "files",
    "flashgram": "instagram", "fossifycalendar": "calendar",
    "fossifyclock": "clock", "fossifycontacts": "people",
    "fossifygallery": "gallery", "fossifymessages": "messages",
    "fossifyphone": "phone", "gbinstagram": "instagram",
    "gbwhatsapp": "whatsappplus", "yowhatsapp": "whatsappplus", "gcam": "cameragoogle",
    "gcammgc": "cameragoogle", "gmailgo": "gmailgo",
    "googlecalendar": "googlecalendar", "googlecamera": "cameragoogle",
    "googlecontacts": "people", "googlemaps": "maps",
    "googlemapsgo": "mapsgo", "googlemessages": "messaging",
    "googlephone": "phone", "googletranslate": "translate",
    "grapheneossecurecamera": "camera", "grapheneosvanadium": "browser",
    "grindrphone": "phone", "hiddensettings": "settings",
    "honorcalculator": "calculator", "honorcontacts": "people",
    "honorfiles": "files", "honorgallery": "gallery",
    "huaweiclock": "clock", "huaweicontacts": "people",
    "huaweifiles": "files", "hyperosclock": "clock",
    "hyperosfiles": "files", "instagramlite": "instagram",
    "instapro": "instagram", "instapro2": "instagram",
    "instafel": "instagram", "jtf acebook": "facebook",
    "kashcal": "calendar", "koler": "phone", "kwikpic": "gallery",
    "lgclock": "clock", "lgemail": "email", "lgfilemanager": "filemanager",
    "lmc83i": "cameragoogle", "lenovofilemanager": "filemanager",
    "lenovozuifilemanager": "filemanager", "lineageosgallery": "gallery",
    "liquiddialer": "phone", "miuicalculator": "calculator",
    "mail": "email", "materialfiles": "files", "mediadownloader": "downloads",
    "meizucalculator": "calculator", "messages": "messages",
    "messenger": "facebookmessenger", "mibrowser": "browser",
    "microsoftoutlook": "outlook", "mizu droid": "phone",
    "modgcam": "cameragoogle", "motocamera": "cameramoto",
    "motoemail": "email", "motogallery": "gallery",
    "mulch": "browser", "mydevicesetting": "settings",
    "myfiles": "files", "mycamguides": "camera",
    "myinsta": "instagram", "ncalc": "calculator",
    "ntcalculator": "calculator", "nothingdialer": "phone",
    "nubiafilemanager": "filemanager", "onepluscalculator": "calculator",
    "oneplusdialer": "phone", "oneplusfilemanager": "filemanager",
    "oneplusgallery": "gallery", "oneplusmessages": "messages",
    "opencamera": "camera", "opencalc": "calculator",
    "opencontacts": "people", "pdfscanner": "pdfviewer",
    "photostampcamera": "camera", "photoscompanion": "photos",
    "piko instagram": "instagram", "protonmail": "email",
    "pulsesms": "messages", "qksms": "messages", "quiksms": "messages",
    "rightdialer": "phone", "rightfiles": "files",
    "samsungcalculator": "calculator", "samsungcamera": "camera",
    "samsungcontacts": "people", "samsunggallery": "gallery",
    "samsunginternetbrowser": "browser", "samsunginternetlite": "browser",
    "samsungmessages": "messages", "samsungmyfiles": "files",
    "samsungphone": "phone", "showcaller": "phone",
    "silencesms": "messages", "simpleanalogclock": "clock",
    "simplecalculator": "calculator", "simplecalendar": "calendar",
    "simplecontacts": "people", "simplecontactsprose": "people",
    "simpledialer": "phone", "simplefilemanager": "filemanager",
    "simplegallery": "gallery", "simplesmsmessenger": "messages",
    "snapchat": "snapchat", "sonyalbum": "gallery",
    "son yphone": "phone", "soundcloud": "music",
    "spotify": "spotify", "spotify premium": "spotify",
    "spotifyweb": "spotify", "telegram": "messages",
    "telegrambeta": "messages", "telegramx": "messages",
    "textra sms": "messages", "thorium": "browser",
    "truecaller": "phone", "ungoogledchromium": "chromium",
    "ungoogledchromiumextensions": "chromium", "ungoogledmaps": "maps",
    "user settings": "settings", "videodownloader": "downloads",
    "whatsapp": "whatsapp", "whatsappbusiness": "whatsapp",
    "wingoscamera": "camera", "youtubego": "youtube go",
    "youtubekids": "youtube kids", "youtubemusic": "youtube music",
    "youtubetv": "youtube tv", "youtube for androidtv": "youtube tv",
    "youtuberevanced": "youtubealt", "youtubemorphe": "youtubealt",
    "youtub evalure": "youtube", "zen uidialercontacts": "phone",
    "zfile": "files",
    "fakecall": "phone", "fakescall": "phone", "mizudroid": "phone",
    "telefono": "phone", "tempnumber": "phone", "talkatone": "phone",
    "foap": "photos", "inst saver": "instagram", "instasaver": "instagram",
    "instaflow": "instagram", "pinterest": "photos", "relaxpic": "photos",
    "inspectandedithtmllive": "browser", "jolt": "browser", "lttrs": "browser",
    "microsoftword": "docs", "microsoftexcel": "sheets",
    "microsoftpowerpoint": "slides", "microsoftonenote": "notes",
    "skypeforbusiness": "skype", "snaptik": "tiktok",
    "soundloadmate": "downloads", "soundloader": "downloads",
    "spot iweb": "spotify", "spotiweb": "spotify",
    "spotifuck": "spotify", "spotishka": "spotify",
    "mpindirici": "downloads", "servicesinfo": "playservices",
    "itranslate": "translate", "apk signer": "settings",
    "apksigner": "settings", "exteraless": "files",
    "helium": "drive", "hideu": "vault", "network": "cloud",
    "applockvip": "vault", "brandsnap": "camera", "irlpro": "meet",
    "instsaver": "instagram", "nocture": "music", "protonvpn": "cloud",
    "talananext": "tasks", "telfono": "phone",
}


def semantic_artwork(label: str, artwork_by_label: dict[str, str]) -> str | None:
    normalized = normalize(label)
    alias = EXPLICIT_ALIASES.get(normalized) or ALIASES.get(normalized)
    if alias:
        target = normalize(alias)
        if target in artwork_by_label:
            return artwork_by_label[target]

    # Exact app-family hints for variants and localized labels.
    if "youtube" in normalized or normalized == "yt":
        for target in ("youtube", "youtubealt"):
            if target in artwork_by_label:
                return artwork_by_label[target]
    if "instagram" in normalized or normalized in {"insta", "flashgram", "wavegram"}:
        return artwork_by_label.get("instagram")
    if "whatsapp" in normalized or "yowhatsapp" in normalized:
        return artwork_by_label.get("whatsapp")
    if "facebook" in normalized:
        return artwork_by_label.get("facebook")
    if "spotify" in normalized:
        return artwork_by_label.get("spotify")
    if "chrome" in normalized or "chromium" in normalized or "browser" in normalized:
        return artwork_by_label.get("chrome") or artwork_by_label.get("browser")
    for tokens, target in SEMANTIC_RULES:
        if any(token in normalized for token in tokens):
            if target in artwork_by_label:
                return artwork_by_label[target]
    return None
# Additional verified Google launcher components missing from the older
# Lawnicons-derived component list. Only component identifiers are reused;
# all drawable artwork still comes from the user's supplied Jelly Bean ZIPs.
EXTRA_COMPONENTS = [
    ("ComponentInfo{com.google.android.keep/com.google.android.keep.activities.BrowseActivity}", "Google Keep", "keep"),
    ("ComponentInfo{com.google.android.apps.docs/com.google.android.apps.docs.app.NewMainProxyActivity}", "Google Drive", "drive"),
    ("ComponentInfo{com.google.android.apps.docs.editors.docs/com.google.android.apps.docs.editors.kix.KixEditorActivity}", "Google Docs", "docs"),
    ("ComponentInfo{com.google.android.apps.docs.editors.sheets/com.google.android.apps.docs.editors.sheets.SheetsEditorActivity}", "Google Sheets", "sheets"),
    ("ComponentInfo{com.google.android.apps.docs.editors.slides/com.google.android.apps.docs.editors.slides.SlidesEditorActivity}", "Google Slides", "slides"),
    ("ComponentInfo{com.google.android.apps.photos/com.google.android.apps.photos.home.HomeActivity}", "Google Photos", "photos"),
    ("ComponentInfo{com.google.android.apps.books/com.google.android.apps.books.app.HomeActivity}", "Google Play Books", "books"),
    ("ComponentInfo{com.google.android.apps.books/com.google.android.apps.books.app.BooksActivity}", "Google Play Books", "books"),
    ("ComponentInfo{com.google.android.apps.podcasts/com.google.android.apps.podcasts.app.LauncherActivity}", "Google Podcasts", "podcasts"),
    ("ComponentInfo{com.google.android.apps.youtube.music/com.google.android.apps.youtube.music.activities.MusicActivity}", "YouTube Music", "youtubemusic"),
    ("ComponentInfo{com.google.android.apps.classroom/com.google.android.apps.classroom.ClassListActivity}", "Google Classroom", "classroom"),
    ("ComponentInfo{com.google.android.apps.meetings/com.google.android.apps.meetings.MainActivity}", "Google Meet", "meet"),
    ("ComponentInfo{com.google.android.apps.meetings/com.google.android.apps.meetings.launch.MeetLaunchActivity}", "Google Meet", "meet"),
    ("ComponentInfo{com.google.android.apps.tachyon/com.google.android.apps.tachyon.ui.main.MainActivity}", "Google Duo", "duo"),
    ("ComponentInfo{com.google.android.apps.walletnfcrel/com.google.android.apps.walletnfcrel.WalletActivity}", "Google Wallet", "wallet"),
    ("ComponentInfo{com.google.android.apps.magazines/com.google.apps.magazines.activities.HomeActivity}", "Google News", "newsweather"),
    ("ComponentInfo{com.google.android.apps.translate/com.google.android.apps.translate.TranslateActivity}", "Google Translate", "translate"),
    ("ComponentInfo{com.android.vending/com.google.android.finsky.activities.MainActivity}", "Google Play Store", "playstore"),
    ("ComponentInfo{com.google.android.music/com.google.android.music.MusicBrowserActivity}", "Google Play Music", "playmusic"),
    ("ComponentInfo{com.google.android.videos/com.google.android.archive.ReactivateActivity}", "Google Play Movies & TV", "playmoviestv"),
    ("ComponentInfo{com.google.android.projection.gearhead/com.google.android.projection.gearhead.companion.MainActivity}", "Android Auto", "androidauto"),
    ("ComponentInfo{com.google.android.apps.nbu.files/com.google.android.apps.nbu.files.home.HomeActivity}", "Files by Google", "filesgo"),
    ("ComponentInfo{com.google.android.apps.googleassistant/com.google.android.apps.googleassistant.AssistantActivity}", "Google Assistant", "assistant"),
    ("ComponentInfo{com.google.android.googlequicksearchbox/com.google.android.googlequicksearchbox.SearchActivity}", "Google Now", "googlenow"),
    ("ComponentInfo{com.google.android.apps.fitness/com.google.android.apps.fitness.welcome.WelcomeActivity}", "Google Fit", "fit"),
    ("ComponentInfo{com.google.android.apps.wellbeing/com.google.android.apps.wellbeing.home.TopLevelActivity}", "Digital Wellbeing", "digitalwellbeing"),
    ("ComponentInfo{com.google.android.apps.safetyhub/com.google.android.apps.safetyhub.home.SafetyHubActivity}", "Personal Safety", "personalsafety"),
    ("ComponentInfo{com.google.android.apps.adwords/com.google.android.apps.adwords.ui.LaunchActivity}", "AdWords", "adwords"),
    ("ComponentInfo{com.google.android.apps.paidtasks/com.google.android.apps.paidtasks.ui.overview.OverviewActivity}", "Opinion Rewards", "opinionrewards"),
    ("ComponentInfo{com.google.android.apps.googlevoice/com.google.android.apps.googlevoice.SplashActivity}", "Google Voice", "voice"),
    ("ComponentInfo{com.google.android.apps.tasks/com.google.android.apps.tasks.ui.TaskListsActivity}", "Google Tasks", "tasks"),
    ("ComponentInfo{com.google.android.apps.kids.familylink/com.google.android.apps.kids.familylink.flutter.standalone.HomeActivity}", "Family Link", "familylink"),
    ("ComponentInfo{com.google.android.apps.kids.familylink/com.google.android.apps.kids.familylink.home.HomeActivityV2}", "Family Link", "familylink"),
    ("ComponentInfo{com.google.android.apps.chromecast.app/com.google.android.apps.chromecast.app.DiscoveryActivity}", "Google Home", "home"),
    ("ComponentInfo{com.google.android.apps.dynamite/com.google.android.apps.dynamite.startup.SplashActivity}", "Google Chat", "chat"),
    ("ComponentInfo{com.google.android.play.games/com.google.android.apps.play.games.app.atv.features.home.HomeActivity}", "Google Play Games", "playgames"),
    ("ComponentInfo{com.google.android.apps.plus/com.google.android.apps.plusone.app.HomeScreenActivity}", "Google+", "Google+"),
    ("ComponentInfo{com.google.android.apps.plus/com.google.android.apps.plus.phone.HomeActivity}", "Google+", "Google+"),
    ("ComponentInfo{com.sec.android.app.camera/com.sec.android.app.camera.Camera}", "Samsung Camera", "Camera Galaxy"),
    ("ComponentInfo{com.samsung.android.camera/com.sec.android.app.camera.Camera}", "Samsung Camera", "Camera Galaxy"),
    ("ComponentInfo{com.lge.camera/com.lge.camera.LGCameraActivity}", "LG Camera", "Camera LG"),
    ("ComponentInfo{com.motorola.camera2/com.motorola.camera2.CameraActivity}", "Motorola Camera", "Camera Moto"),
    ("ComponentInfo{com.motorola.camera2/com.motorola.camera.Camera}", "Motorola Camera", "Camera Moto"),
    ("ComponentInfo{com.oneplus.camera/com.oneplus.camera.OPCameraActivity}", "OnePlus Camera", "Camera One"),
    ("ComponentInfo{org.codeaurora.snapcam/com.android.camera.CameraLauncher}", "Snap Camera", "Camera ALT"),
    ("ComponentInfo{com.google.ar.lens/com.google.vr.apps.ornament.app.MainActivity}", "Google Lens", "Lens"),
    ("ComponentInfo{com.google.android.apps.recorder/com.google.android.apps.recorder.activity.RecorderActivity}", "Google Recorder", "Sound Recorder"),
    ("ComponentInfo{com.android.soundrecorder/com.android.soundrecorder.SoundRecorder}", "AOSP Sound Recorder", "Sound Recorder"),
    ("ComponentInfo{com.yahoo.mobile.client.android.mail/com.yahoo.mobile.client.android.mail.app.YahooMailActivity}", "Yahoo Mail", "Yahoo Mail"),
    ("ComponentInfo{com.chrome.canary/com.google.android.apps.chrome.Main}", "Chrome Canary", "Chrome Canary"),
    ("ComponentInfo{com.google.android.deskclock/com.android.deskclock.DeskClock}", "Google Clock", "Clock"),
    ("ComponentInfo{com.android.deskclock/com.android.deskclock.DeskClockTabActivity}", "AOSP Clock", "Clock"),
    ("ComponentInfo{com.samsung.android.app.clockpack/com.sec.android.app.clockpackage.ClockPackage}", "Samsung Clock", "Clock ALT"),

    # Historical Jelly Bean artwork with launcher components corroborated by
    # multiple independent public icon-pack appfilter catalogues. These are
    # explicit component IDs, not package-name guesses derived from artwork.
    ("ComponentInfo{com.amazon.mShop.android.shopping/com.amazon.mShop.home.HomeActivity}", "Amazon", "Amazon"),
    ("ComponentInfo{com.sec.android.app.samsungapps/com.sec.android.app.samsungapps.SamsungAppsMainActivity}", "Galaxy Store", "Galaxy Store"),
    ("ComponentInfo{com.google.android.apps.adm/com.google.android.apps.adm.MainActivity}", "Find My Device", "Find My Device"),
    ("ComponentInfo{com.google.android.apps.adm/com.google.android.apps.adm.activities.MainActivity}", "Find My Device", "Find My Device"),
    ("ComponentInfo{com.google.android.apps.cultural/com.google.android.apps.cultural.web.WebViewActivity}", "Arts & Culture", "Arts & Culture"),
    ("ComponentInfo{com.google.android.apps.youtube.creator/com.google.android.apps.youtube.creator.activities.SplashActivity}", "YouTube Creator Studio", "YouTube Creator Studio"),

    ("ComponentInfo{com.netflix.mediaclient/com.netflix.mediaclient.ui.launch.UIWebViewActivity}", "Netflix", "Netfilx"),
    ("ComponentInfo{com.netflix.mediaclient/com.netflix.mediaclient.UIWebViewActivity}", "Netflix", "Netfilx"),
    ("ComponentInfo{com.twitter.android/com.twitter.android.StartActivity}", "Twitter", "Twitter"),
    ("ComponentInfo{com.twitter.android/com.twitter.android.LoginActivity}", "Twitter", "Twitter"),
    ("ComponentInfo{com.google.android.apps.youtube.creator/.main.MainActivity}", "YouTube Studio", "YouTube Creator Studio"),
    ("ComponentInfo{com.google.android.apps.youtube.creator/com.google.android.apps.youtube.creator.activities.SplashActivity}", "YouTube Studio", "YouTube Creator Studio"),
    ("ComponentInfo{com.google.android.apps.adwords/com.google.android.apps.adwords.ui.LaunchActivity}", "AdWords Express", "AdWords Express"),
    ("ComponentInfo{com.google.android.apps.cloudprint/com.google.android.apps.cloudprint.printdialog.CloudPrintLauncherVisibility}", "Cloud Print", "Cloud Print"),
    ("ComponentInfo{com.google.android.apps.magazines/com.google.apps.dots.android.app.activity.CurrentsStartActivity}", "Currents", "Currents"),
    ("ComponentInfo{com.google.android.apps.unveil/com.google.android.apps.unveil.SearchHistoryActivity}", "Google Goggles", "Goggles"),
    ("ComponentInfo{com.google.android.apps.chromecast.app/com.google.android.apps.chromecast.app.DiscoveryActivity}", "Chromecast", "Chromecast"),
    ("ComponentInfo{com.google.android.apps.inbox/com.google.android.apps.bigtop.activities.InitActivity}", "Inbox", "Inbox"),
    ("ComponentInfo{com.google.android.apps.m4b/com.google.android.apps.mymaps.activities.maplist.MapListActivity}", "My Maps", "My Maps"),
    ("ComponentInfo{com.google.android.apps.maps/com.google.android.maps.driveabout.app.DestinationActivity}", "Google Maps Navigation", "Navigation"),
    ("ComponentInfo{com.google.android.street/com.google.android.apps.dragonfly.activities.main.MainActivity}", "Street View", "Street View"),
    ("ComponentInfo{com.google.android.talk/com.google.android.talk.SigningInActivity}", "Hangouts", "Hangouts"),
    ("ComponentInfo{com.google.android.apps.plus/com.google.android.apps.plus.phone.HomeActivity}", "Google+", "Google"),
    ("ComponentInfo{com.google.android.apps.plus/com.google.android.apps.plusone.app.HomeScreenActivity}", "Google+", "Google"),
    ("ComponentInfo{com.google.android.apps.plus/com.google.android.apps.circles.realtimechat.ConversationListActivity}", "Google+ Messenger", "G+ Messenger"),
    ("ComponentInfo{com.google.android.apps.maps/com.google.android.maps.PlacesActivity}", "Google Maps Places", "Places"),
    ("ComponentInfo{com.android.videoeditor/com.android.videoeditor.ProjectsActivity}", "Movie Studio", "Movie Studio"),
    ("ComponentInfo{com.android.voicedialer/com.android.voicedialer.VoiceDialerLauncherActivity}", "Voice Dialer", "Voice Dialer"),
    ("ComponentInfo{com.qo.android.am3/com.qo.android.quickoffice.QuickofficeDispatcher}", "Quickoffice", "Quickoffice"),
    ("ComponentInfo{com.google.android.gms/com.google.android.gms.app.settings.GoogleSettingsActivity}", "Google Settings", "Google Settings"),
    ("ComponentInfo{com.google.android.apps.currents/com.google.apps.dots.android.app.activity.CurrentsStartActivity}", "Google Currents", "Currents"),

    # Additional legacy Jelly Bean-era entries corroborated by independent
    # LineageOS and Nicque appfilter catalogues. These are historical IDs;
    # verify against the target APK before assuming current-version support.
    ("ComponentInfo{com.adobe.flashplayer/com.adobe.flashplayer.SettingsManager}", "Adobe Flash Player", "Flash Player"),
    ("ComponentInfo{com.dreamstep.wPicasaWeb/com.dreamstep.wPicasaWeb.MainNavigationActivity}", "Picasa Web Albums", "Picasa"),
    ("ComponentInfo{com.android.vending/com.android.vending.AssetBrowserActivity}", "Android Market", "Market"),
    ("ComponentInfo{com.android.stk/com.android.stk.StkLauncherActivity}", "SIM Toolkit", "SIM Manager"),
    ("ComponentInfo{com.google.android.inputmethod.latin/com.android.inputmethod.latin.setup.SetupActivity}", "Google Keyboard", "Keyboard"),
    ("ComponentInfo{com.google.android.inputmethod.pinyin/com.google.android.apps.inputmethod.libs.framework.core.LauncherActivity}", "Google Pinyin Input", "Pinyin Input"),
    ("ComponentInfo{com.google.android.inputmethod.pinyin/com.google.android.apps.inputmethod.preference.SettingsActivity}", "Google Pinyin Keyboard Settings", "Pinyin Keyboard"),
    # Further Jelly Bean-era Google apps corroborated by public historical appfilter catalogues.
    ("ComponentInfo{com.google.android.apps.giant/com.google.android.apps.giant.activity.ProfilePickerActivity}", "Google Analytics", "Analytics"),
    ("ComponentInfo{com.google.android.apps.plus/com.google.android.apps.plus.phone.ConversationListActivity}", "Google+ Photos", "G+ Photos"),
    ("ComponentInfo{com.google.android.apps.giant/com.google.android.apps.giant.activity.AnalyticsLaunchActivity}", "Google Analytics", "Analytics"),
    ("ComponentInfo{com.google.android.apps.hangoutsdialer/com.google.android.apps.hangoutsdialer.app.LaunchActivity}", "Hangouts Dialer", "Hangouts Dialer"),

    # Additional archive app artwork mapped in one batch from exact historical
    # launcher component records found in independent public appfilter catalogues.
    ("ComponentInfo{com.google.android.apps.offers/com.google.android.apps.offers.puzo.ui.home.HomeActivity}", "Google Offers", "Offers"),
    ("ComponentInfo{com.google.android.apps.vega/com.google.android.apps.vega.VegaMainActivity}", "Google My Business", "My Business"),
    ("ComponentInfo{com.google.samples.apps.cardboarddemo/com.google.research.airbender.paperscope.android.launcher.Launcher2D}", "Google Cardboard", "Cardboard Camera"),
    ("ComponentInfo{com.google.android.apps.travel.onthego/com.google.android.apps.travel.onthego.activities.MainActivity}", "Google Trips", "Trips"),
    ("ComponentInfo{com.google.chromeremotedesktop/org.chromium.chromoting.Chromoting}", "Chrome Remote Desktop", "Remote Desktop"),
    ("ComponentInfo{com.motorola.cameraone/com.motorola.camera.Camera}", "Motorola Camera One", "Camera One"),
    ("ComponentInfo{com.google.android.tv.remote/com.google.android.tv.remote.RemoteActivity}", "Android TV Remote", "Android TV"),
    ("ComponentInfo{com.google.android.apps.freighter/com.google.android.apps.nbu.freighter.splash.SplashActivity}", "Google Datally", "Datally"),
    ("ComponentInfo{com.google.samples.apps.cardboarddemo/com.google.vr.cardboard.paperscope.carton.Home2D}", "Google Cardboard", "Cardboard Camera"),
    ("ComponentInfo{com.google.samples.apps.cardboarddemo/com.google.vr.cardboard.paperscope.carton.Home2Dv2}", "Google Cardboard", "Cardboard Camera"),

]


def iter_archive_images(payload: bytes, source_path: str, depth: int = 0):
    """Walk ZIP/APK/JAR containers by file signature, not filename extension."""
    import io
    from PIL import Image

    if depth > 5:
        return
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as container:
            for info in container.infolist():
                if info.is_dir():
                    continue
                try:
                    data = container.read(info)
                except (OSError, RuntimeError, zipfile.BadZipFile):
                    continue
                member_path = f"{source_path}!/{info.filename}"
                # APK, XAPK, JAR and nested ZIPs are all ZIP containers.
                if data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
                    yield from iter_archive_images(data, member_path, depth + 1)
                    continue
                if Path(info.filename).suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                try:
                    with Image.open(io.BytesIO(data)) as image:
                        width, height = image.size
                        image.verify()
                except Exception:
                    continue
                if width < 48 or height < 48 or width > 4096 or height > 4096:
                    continue
                yield member_path, data, width, height
    except zipfile.BadZipFile:
        return


def main() -> None:
    missing = [str(path) for path in ARCHIVES if not path.is_file()]
    if missing:
        raise SystemExit("Missing Holokat source archive(s): " + ", ".join(missing))

    DRAWABLE_DIR.mkdir(parents=True, exist_ok=True)
    images: dict[str, tuple[bytes, str]] = {}
    hashes: set[str] = set()
    archive_inventory: list[dict[str, object]] = []
    for archive in ARCHIVES:
        archive_bytes = archive.read_bytes()
        with zipfile.ZipFile(archive) as outer:
            top_entries = [
                {"path": info.filename, "size": info.file_size}
                for info in outer.infolist() if not info.is_dir()
            ]
        archive_images = 0
        nested_containers = 0
        for original_path, data, width, height in iter_archive_images(archive_bytes, archive.name):
            archive_images += 1
            digest = hashlib.sha256(data).hexdigest()
            if digest in hashes:
                continue
            hashes.add(digest)
            member_name = original_path.split("!/")[-1]
            base = "jb_" + resource_name(Path(member_name).name)
            name = base
            suffix = 2
            while name in images:
                name = f"{base}_{suffix}"
                suffix += 1
            images[name] = (data, original_path)
        # Count APK/ZIP containers at the outer level for an audit trail.
        nested_containers = sum(
            1 for entry in top_entries
            if Path(entry["path"]).suffix.lower() in {".apk", ".zip", ".xapk", ".jar"}
        )
        archive_inventory.append({
            "archive": archive.name,
            "top_level_entries": len(top_entries),
            "top_level_entry_sample": top_entries[:80],
            "nested_container_entries": nested_containers,
            "supported_image_entries": archive_images,
        })

    report_dir = ROOT / "build/holokat-import-report"
    report_dir.mkdir(parents=True, exist_ok=True)
    if not images:
        (report_dir / "archive-inventory.json").write_text(
            __import__("json").dumps(archive_inventory, indent=2), encoding="utf-8"
        )
        raise SystemExit(
            "No supported raster artwork found. Inspect archive-inventory.json; "
            "the ZIP entries may be encrypted, unsupported, or non-image sources."
        )

    for name, (data, original_path) in images.items():
        member_name = original_path.split("!/")[-1]
        extension = Path(member_name).suffix.lower()
        (DRAWABLE_DIR / f"{name}{extension}").write_bytes(data)

    drawable_root = ET.parse(DRAWABLE_XML).getroot() if DRAWABLE_XML.is_file() else ET.Element("resources")
    existing_drawables = {item.attrib.get("name") for item in drawable_root.findall("item")}
    for name in sorted(images):
        if name not in existing_drawables:
            ET.SubElement(drawable_root, "item", {"drawable": name, "name": name})
    ET.indent(drawable_root, space="    ")
    DRAWABLE_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(drawable_root, encoding="unicode") + "\n",
        encoding="utf-8",
    )

    artwork_by_label: dict[str, str] = {}
    artwork_by_original_stem: dict[str, str] = {}
    for resource, (_, original_path) in images.items():
        original_stem = Path(original_path.split("!/")[-1]).stem
        label = normalize(original_stem)
        artwork_by_label.setdefault(label, resource)
        artwork_by_original_stem.setdefault(original_stem.casefold(), resource)

    old_root = ET.parse(APPFILTER_XML).getroot() if APPFILTER_XML.is_file() else ET.Element("resources")
    appfilter = ET.Element("resources")
    matched_components: set[str] = set()
    matched_artwork: Counter[str] = Counter()
    matched_labels: dict[str, set[str]] = defaultdict(set)
    unmatched_labels: set[str] = set()

    for item in old_root.findall("item"):
        component = item.attrib.get("component")
        label = item.attrib.get("name", "")
        if not component or component in matched_components:
            continue
        normalized = normalize(label)
        resource = artwork_by_label.get(normalized)
        if resource is None:
            resource = semantic_artwork(label, artwork_by_label)
        if resource is not None:
            ET.SubElement(appfilter, "item", {
                "component": component, "drawable": resource, "name": label,
            })
            matched_artwork[resource] += 1
            matched_labels[resource].add(label)
        else:
            ET.SubElement(appfilter, "item", dict(item.attrib))
            unmatched_labels.add(label)
        matched_components.add(component)

    for component, label, artwork in EXTRA_COMPONENTS:
        if component in matched_components:
            continue
        resource = artwork_by_original_stem.get(artwork.casefold()) or artwork_by_label.get(normalize(artwork))
        if resource is None:
            continue
        ET.SubElement(appfilter, "item", {
            "component": component, "drawable": resource, "name": label,
        })
        matched_components.add(component)
        matched_artwork[resource] += 1
        matched_labels[resource].add(label)

    upstream_url = (
        "https://raw.githubusercontent.com/LawnchairLauncher/lawnicons/"
        "cd91ff0bd00ff0a6c9d606d1c326b451b6563506/app/assets/appfilter.xml"
    )
    request = urllib.request.Request(
        upstream_url, headers={"User-Agent": "Insomdroid-Icon-Pack-Builder"}
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        upstream_root = ET.fromstring(response.read())
    upstream_added = 0
    for item in upstream_root.findall("item"):
        component = item.attrib.get("component", "").strip()
        if not component or component in matched_components:
            continue
        label = item.attrib.get("name", "").strip() or item.attrib.get("drawable", "").strip()
        resource = artwork_by_label.get(normalize(label)) or semantic_artwork(label, artwork_by_label)
        if resource is None:
            continue
        ET.SubElement(appfilter, "item", {
            "component": component,
            "drawable": resource,
            "name": label or component.split("/", 1)[0],
        })
        matched_components.add(component)
        matched_artwork[resource] += 1
        matched_labels[resource].add(label)
        upstream_added += 1

    ET.indent(appfilter, space="    ")
    APPFILTER_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(appfilter, encoding="unicode") + "\n",
        encoding="utf-8",
    )

    unused_assets = [
        {"resource": resource, "source": original, "mapped": False}
        for resource, (_, original) in images.items()
        if resource not in matched_artwork
    ]
    report = {
        "archives": archive_inventory,
        "unique_archive_images": len(images),
        "mapped_artworks": len(matched_artwork),
        "launcher_component_mappings": len(appfilter.findall("item")),
        "new_pinned_lawnicons_mappings": upstream_added,
        "unmapped_artworks": unused_assets,
        "mapped_artworks_detail": [
            {"resource": resource, "components": count, "labels": sorted(matched_labels[resource])}
            for resource, count in sorted(matched_artwork.items())
        ],
    }
    (report_dir / "report.json").write_text(
        __import__("json").dumps(report, indent=2), encoding="utf-8"
    )
    with (report_dir / "unmapped-artwork.txt").open("w", encoding="utf-8") as stream:
        for item in unused_assets:
            stream.write(f'{item["resource"]} <- {item["source"]}\n')

    print(f"Jelly Bean archive inventory: {archive_inventory}")
    print(f"Imported {len(images)} unique archive images.")
    print(f"Mapped {len(matched_artwork)} distinct archive artworks to {len(matched_components)} components.")
    print(f"Added {upstream_added} app components from pinned Lawnicons mapping.")
    print(f"Unmapped source artwork report: {report_dir / 'unmapped-artwork.txt'}")


if __name__ == "__main__":
    main()
