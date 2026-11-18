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

The remaining 132 report entries are intentionally retained without a guessed component. System services, input methods, widgets, TV-only surfaces, retired products, generic labels and feature sub-screens are not mapped to unrelated modern apps.

The importer change triggers the combined release workflow. The build and new report must be checked before declaring the mapping change complete.
