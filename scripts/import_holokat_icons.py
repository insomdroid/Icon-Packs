#!/usr/bin/env python3
"""Merge the supplied Jelly Bean archive artwork into the single KitKat icon pack."""
from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
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
]


def main() -> None:
    missing = [str(path) for path in ARCHIVES if not path.is_file()]
    if missing:
        raise SystemExit("Missing Holokat source archive(s): " + ", ".join(missing))

    DRAWABLE_DIR.mkdir(parents=True, exist_ok=True)
    for old in DRAWABLE_DIR.iterdir():
        if old.is_file():
            old.unlink()

    images: dict[str, tuple[bytes, str]] = {}
    hashes: set[str] = set()
    for archive in ARCHIVES:
        with zipfile.ZipFile(archive) as zf:
            for info in zf.infolist():
                if info.is_dir() or Path(info.filename).suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                data = zf.read(info)
                digest = hashlib.sha256(data).hexdigest()
                if digest in hashes:
                    continue
                hashes.add(digest)
                base = "jb_" + resource_name(Path(info.filename).name)
                name = base
                suffix = 2
                while name in images:
                    name = f"{base}_{suffix}"
                    suffix += 1
                images[name] = (data, info.filename)

    if not images:
        raise SystemExit("No supported image files found in Holokat archives.")

    for name, (data, original_path) in images.items():
        extension = Path(original_path).suffix.lower()
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
    artwork_by_label_and_path: dict[str, str] = {}
    artwork_by_original_stem: dict[str, str] = {}
    for resource, (_, original_path) in images.items():
        original_stem = Path(original_path).stem
        label = normalize(original_stem)
        artwork_by_label.setdefault(label, resource)
        artwork_by_label_and_path[label] = resource
        artwork_by_original_stem[original_stem.casefold()] = resource

    old_filter = APPFILTER_XML
    appfilter = ET.parse(APPFILTER_XML).getroot() if APPFILTER_XML.is_file() else ET.Element("resources")
    matched_components: set[str] = set()
    matched_artwork: Counter[str] = Counter()
    matched_labels: dict[str, set[str]] = defaultdict(set)
    unmatched_labels: set[str] = set()

    if old_filter.is_file():
        old_root = ET.parse(old_filter).getroot()
        for item in old_root.findall("item"):
            component = item.attrib.get("component")
            label = item.attrib.get("name", "")
            if not component or component in matched_components:
                continue

            normalized = normalize(label)
            resource = artwork_by_label.get(normalized)
            if resource is None:
                resource = semantic_artwork(label, artwork_by_label)

            if resource is None:
                unmatched_labels.add(label)
                matched_components.add(component)
                continue

            existing_item = next(
                (entry for entry in appfilter.findall("item")
                 if entry.attrib.get("component") == component),
                None,
            )
            if existing_item is not None:
                existing_item.set("drawable", resource)
            else:
                ET.SubElement(appfilter, "item", {
                    "component": component,
                    "drawable": resource,
                    "name": label,
                })
            matched_components.add(component)
            matched_artwork[resource] += 1
            matched_labels[resource].add(label)

    for component, label, artwork in EXTRA_COMPONENTS:
        if component in matched_components:
            continue
        resource = artwork_by_original_stem.get(artwork.casefold())
        if resource is None:
            resource = artwork_by_label.get(normalize(artwork))
        if resource is None:
            continue
        ET.SubElement(appfilter, "item", {
            "component": component,
            "drawable": resource,
            "name": label,
        })
        matched_components.add(component)
        matched_artwork[resource] += 1
        matched_labels[resource].add(label)

    ET.indent(appfilter, space="    ")
    APPFILTER_XML.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        + ET.tostring(appfilter, encoding="unicode") + "\n",
        encoding="utf-8",
    )

    print(f"Jelly Bean imported {len(images)} unique image assets into the combined icon pack.")
    print(f"Generated {len(appfilter.findall('item'))} unique launcher component mappings.")
    print(f"Artwork used by mappings: {len(matched_artwork)} / {len(images)}.")
    print(f"Unmatched app labels: {len(unmatched_labels)}.")
    for resource, count in sorted(matched_artwork.items(), key=lambda entry: (-entry[1], entry[0])):
        labels = ", ".join(sorted(matched_labels[resource]))
        print(f"  {resource}: {count} components [{labels}]")
    if unmatched_labels:
        print("Unmatched labels: " + " | ".join(sorted(unmatched_labels)))
    print("Jelly Bean archive artwork is retained without redrawing or recoloring.")


if __name__ == "__main__":
    main()
