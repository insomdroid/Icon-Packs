# Holokat Mapping Follow-up

Six component records for five archived artwork identities were added to `EXTRA_COMPONENTS` in `scripts/import_holokat_icons.py`. The importer regenerates `appfilter.xml`, so maintaining these entries in the importer is required.

| Artwork | Component | Public catalogue corroboration |
|---|---|---|
| Amazon | `com.amazon.mShop.android.shopping/com.amazon.mShop.home.HomeActivity` | [NanoIconPack](https://github.com/by-syk/NanoIconPack/blob/856fb33ad544aa595a60897f83c7c3a95e17ebee/out/appfilter_originalwish.xml), [Snow](https://github.com/baitmooth/snow/blob/5ac6528aa59cc1381b5cbe86b57c5f709a5950fa/newicons/appfilter.xml) |
| Galaxy Store | `com.sec.android.app.samsungapps/com.sec.android.app.samsungapps.SamsungAppsMainActivity` | [NanoIconPack](https://github.com/by-syk/NanoIconPack/blob/856fb33ad544aa595a60897f83c7c3a95e17ebee/out/appfilter_originalwish.xml), [Snow requests](https://github.com/baitmooth/snow/blob/5ac6528aa59cc1381b5cbe86b57c5f709a5950fa/docs/assets/requests.txt) |
| Find My Device | `com.google.android.apps.adm/com.google.android.apps.adm.MainActivity` | [Candybar](https://github.com/zixpo/candybar/blob/0aa2f57789ef9e0af1a2edb5e646ac45ebe8ca26/app/src/main/assets/appfilter.xml), [MBEStyle](https://github.com/meolunr/MBEStyle/blob/969e0e0921223a1e470c1417fd4ca0fbee7b5f73/app/src/main/assets/appfilter.xml) |
| Find My Device | `com.google.android.apps.adm/com.google.android.apps.adm.activities.MainActivity` | [Snow](https://github.com/baitmooth/snow/blob/5ac6528aa59cc1381b5cbe86b57c5f709a5950fa/newicons/appfilter.xml), [Papirus](https://github.com/PapirusDevelopmentTeam/papirus_icons/blob/b901e193c802dc9821acda30b5c7bd5f240bdaf5/data.json) |
| Arts & Culture | `com.google.android.apps.cultural/com.google.android.apps.cultural.web.WebViewActivity` | [Candybar](https://github.com/zixpo/candybar/blob/0aa2f57789ef9e0af1a2edb5e646ac45ebe8ca26/app/src/main/assets/appfilter.xml), [Raphael](https://github.com/srvraj311/Raphael-Icon-Pack/blob/29a50606aeb319538816f411e3b4bf87f6bec01c/app/src/main/assets/appfilter.xml) |
| YouTube Creator Studio | `com.google.android.apps.youtube.creator/com.google.android.apps.youtube.creator.activities.SplashActivity` | [Candybar](https://github.com/zixpo/candybar/blob/0aa2f57789ef9e0af1a2edb5e646ac45ebe8ca26/app/src/main/assets/appfilter.xml), [Papirus](https://github.com/PapirusDevelopmentTeam/papirus_icons/blob/b901e193c802dc9821acda30b5c7bd5f240bdaf5/data.json) |

These are cross-catalogue corroborated component strings, not official APK-manifest certification. Community appfilter databases can retain stale activity aliases. Device/APK verification remains necessary before claiming every alias works across all versions and OEMs.

## Second mapping pass

Six additional component records covering three more artwork identities were added:

| Artwork | Component | Corroborating public catalogues |
|---|---|---|
| Netflix (archive filename is misspelled `Netfilx.png`) | `com.netflix.mediaclient/com.netflix.mediaclient.ui.launch.UIWebViewActivity` | [CrapCons](https://github.com/the-dagger/CrapCons-IconPack/blob/master/app/src/main/res/xml/appfilter.xml), [MaterialOS](https://github.com/materialos/android-icon-pack/blob/ed0b35adffc74e500680f70db6e344deaca358d8/app/src/main/assets/appfilter.xml), [CoreBuildsApps](https://github.com/brevityA/CoreBuildsApps/blob/f7c29360919ee0a802ad0e511fbcefb1353e832d/app/src/main/assets/appfilter.xml) |
| Netflix | `com.netflix.mediaclient/com.netflix.mediaclient.UIWebViewActivity` | [CrapCons](https://github.com/the-dagger/CrapCons-IconPack/blob/master/app/src/main/res/xml/appfilter.xml), [Nicque appfilter](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml) |
| Twitter | `com.twitter.android/com.twitter.android.StartActivity` | [MaterialIconPackTemplate](https://github.com/architjn/MaterialIconPackTemplate/blob/9e96add46e9b9fc199771c27c1192035a92fe183/app/src/main/assets/appfilter.xml), [Launcher Theme Template](https://github.com/haxzamatic/Launcher-Theme-Template/blob/ff4a898c8c63d5320ac61e4f7961fcfd54d05c40/assets/appfilter.xml) |
| Twitter | `com.twitter.android/com.twitter.android.LoginActivity` | [NanoIconPack](https://github.com/by-syk/NanoIconPack/blob/856fb33ad544aa595a60897f83c7c3a95e17ebee/out/appfilter_originalwish.xml), [Launcher Theme Template](https://github.com/haxzamatic/Launcher-Theme-Template/blob/ff4a898c8c63d5320ac61e4f7961fcfd54d05c40/assets/appfilter.xml) |
| YouTube Studio | `com.google.android.apps.youtube.creator/.main.MainActivity` | [GoogleIcons](https://github.com/amirzaidi/GoogleIcons/blob/f346215f3556b6cfc7cac93238a92b3238b007ea/app/src/main/res/xml/appfilter.xml), [win95-mode](https://github.com/sindriax/win95-mode/blob/10cd4e466168b6a0226fab07d144a554de66f262/app/src/main/res/xml/appfilter.xml) |
| YouTube Studio | `com.google.android.apps.youtube.creator/com.google.android.apps.youtube.creator.activities.SplashActivity` | [win95-mode](https://github.com/sindriax/win95-mode/blob/10cd4e466168b6a0226fab07d144a554de66f262/app/src/main/res/xml/appfilter.xml), [monotone-icons](https://github.com/gaurav712/monotone-icons/blob/08bbd04c8c52045938d953e0a21184dd70a70ff9/app/src/main/res/xml/appfilter.xml) |

The six strings are catalogue-corroborated, not official APK-manifest certification. Launcher Activity aliases may vary by installed app version. Actual device/APK verification is still required.

The remaining artwork is retained without guessed mappings. Many are platform features, input methods, widgets, TV-only surfaces, retired products, generic labels, or feature sub-screens rather than standalone launcher apps.

The importer change triggers the combined release workflow. Check the regenerated report and release build before considering this pass complete.


## Third mapping pass

Twelve component records were added for legacy Google-era artwork with matching public appfilter evidence: AdWords Express, Cloud Print, Currents, Google Goggles, Chromecast companion, Inbox, My Maps, Maps Navigation, Street View, Hangouts, and two Google+ activity aliases. Sources include [SysAdminDoc iOSIconPack](https://github.com/SysAdminDoc/iOSIconPack/blob/db0ccf25ff695a076eee16833fd868a1a454cda6/app/src/main/assets/appfilter.xml), [LineageOS theme template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml), [Candybar](https://github.com/zixpo/candybar/blob/0aa2f57789ef9e0af1a2edb5e646ac45ebe8ca26/app/src/main/assets/appfilter.xml), [SmartIconPack](https://github.com/Mr-XiaoLiang/SmartIconPack/blob/7e22e2d0eaf40172dbd65a0c06e08eeb3bc0017c/app/src/main/res/xml/appfilter.xml), [CircoIconPack](https://github.com/Mookiies/CircoIconPack/blob/b481af802201a662845c182a20961a898704521e/res/xml/appfilter.xml), and [GreatFreedom](https://github.com/elelinux/GreatFreedom/blob/959dd69b204936a83426e415c65191bc206153c9/assets/icons/res/xml/appfilter.xml).

These historical components are intentionally retained as legacy aliases; they may only resolve on older APK versions or devices. Do not interpret an appfilter match as proof that the app is still distributed or installed today.


## Fourth mapping pass

Seven additional legacy component records were added after checking the archived artwork against historical public appfilter catalogues. The source catalogues include the [LineageOS/CyanogenMod theme template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) and [Nicque appfilter catalogue](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml).

| Artwork | Component | Evidence |
|---|---|---|
| G+ Messenger | `com.google.android.apps.plus/com.google.android.apps.circles.realtimechat.ConversationListActivity` | LineageOS template |
| Places | `com.google.android.apps.maps/com.google.android.maps.PlacesActivity` | LineageOS template |
| Movie Studio | `com.android.videoeditor/com.android.videoeditor.ProjectsActivity` | LineageOS template |
| Voice Dialer | `com.android.voicedialer/com.android.voicedialer.VoiceDialerLauncherActivity` | LineageOS template |
| Quickoffice | `com.qo.android.am3/com.qo.android.quickoffice.QuickofficeDispatcher` | LineageOS template |
| Google Settings | `com.google.android.gms/com.google.android.gms.app.settings.GoogleSettingsActivity` | Nicque appfilter catalogue |
| Currents | `com.google.android.apps.currents/com.google.apps.dots.android.app.activity.CurrentsStartActivity` | LineageOS template (historical package alias) |

These component IDs are historical community-catalogue entries, not device-verified manifests. The importer only adds a record if the matching source artwork is present in the supplied archive. The next workflow report is authoritative for how many unique artworks were actually covered.


## Fifth mapping pass

Seven historical component entries were added for archive assets that are genuine app/settings launch surfaces and have corroborating public appfilter records:

| Artwork | Component | Evidence |
|---|---|---|
| Flash Player | `com.adobe.flashplayer/com.adobe.flashplayer.SettingsManager` | [LineageOS template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml), [Nicque catalogue](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml) |
| Picasa | `com.dreamstep.wPicasaWeb/com.dreamstep.wPicasaWeb.MainNavigationActivity` | [LineageOS template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) |
| Android Market | `com.android.vending/com.android.vending.AssetBrowserActivity` | [Nicque catalogue](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml), [LineageOS template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) |
| SIM Toolkit | `com.android.stk/com.android.stk.StkLauncherActivity` | [Nicque catalogue](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml), [LineageOS template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) |
| Google Keyboard | `com.google.android.inputmethod.latin/com.android.inputmethod.latin.setup.SetupActivity` | [Nicque catalogue](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml) |
| Google Pinyin Input | `com.google.android.inputmethod.pinyin/com.google.android.apps.inputmethod.libs.framework.core.LauncherActivity` | [LineageOS template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) |
| Google Pinyin Keyboard Settings | `com.google.android.inputmethod.pinyin/com.google.android.apps.inputmethod.preference.SettingsActivity` | [LineageOS template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) |

These are historical catalogue-backed IDs, not claims that these apps are currently installed or that the same activities exist in modern releases. The importer skips components already claimed by an earlier mapping. The build report from the fifth-pass workflow is the authority for how many distinct artwork resources this pass actually adds.

The other remaining artwork is not automatically an app icon. Names such as platform capabilities, input methods, widgets, TV/Wear system surfaces, and feature-specific artwork must be classified before mapping. An icon can remain available in the drawable picker without having a launcher component.


## Sixth mapping pass

Two additional Google-era artwork entries were added after confirming their exact component IDs in independent historical public appfilter catalogues:

| Artwork | Component | Evidence |
|---|---|---|
| Analytics | `com.google.android.apps.giant/com.google.android.apps.giant.activity.ProfilePickerActivity` | [Nicque appfilter catalogue](https://github.com/Nicque/appfilter-1/blob/master/appfilter.xml) |
| G+ Photos | `com.google.android.apps.plus/com.google.android.apps.plus.pho` | [LineageOS theme template](https://github.com/LineageOS/android_packages_themes_Template/blob/master/theme/build/intermediates/assets/debug/icons/res/xml/appfilter.xml) |

These are historical component IDs supported by public icon-pack catalogues, not proof that the same activities remain available in current releases. The build report determines whether each distinct archive artwork was newly covered.


## Seventh mapping pass

Two further legacy launcher components were corroborated in the historical CrapCons appfilter catalogue:

| Artwork | Component | Evidence |
|---|---|---|
| Analytics | `com.google.android.apps.giant/com.google.android.apps.giant.activity.AnalyticsLaunchActivity` | [CrapCons appfilter](https://github.com/the-dagger/CrapCons-IconPack/blob/master/app/src/main/res/xml/appfilter.xml) |
| Hangouts Dialer | `com.google.android.apps.hangoutsdialer/com.google.android.apps.hangoutsdialer.app.LaunchActivity` | [CrapCons appfilter](https://github.com/the-dagger/CrapCons-IconPack/blob/master/app/src/main/res/xml/appfilter.xml) |

The Analytics profile-picker component from the previous pass is retained as a historical alias. Both Analytics activity IDs are catalogue-backed. These entries are not device-manifest verification; the next CI report will show the distinct artwork count actually covered.


## Eighth mapping pass

Google Admin was added using the package/activity pair exposed by the public icon metadata catalogue:

| Artwork | Component | Evidence |
|---|---|---|
| Admin | `com.google.android.apps.enterprise.cpanel/com.google.android.apps.enterprise.cpanel.activities.EntryPointActivity` | [IconPusher Admin package metadata](https://iconpusher.com/package/com.google.android.apps.enterprise.cpanel) |

The activity is a historical component candidate. It remains subject to verification against an actual target APK; the build report will confirm whether the archive artwork was newly mapped.
