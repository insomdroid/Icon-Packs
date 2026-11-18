# Android 4.4.4 AOSP icon assets

This project imports the following original PNG application icons from the Android Open Source Project source tag `android-4.4.4_r2`:

| Pack drawable | AOSP source repository | Source resource |
|---|---|---|
| `messages` | [platform_packages_apps_mms](https://github.com/aosp-mirror/platform_packages_apps_mms/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_smsmms.png` |
| `settings` | [platform_packages_apps_settings](https://github.com/aosp-mirror/platform_packages_apps_settings/tree/android-4.4.4_r2) | `res/mipmap-xxxhdpi/ic_launcher_settings.png` |
| `camera` | [platform_packages_apps_camera](https://github.com/aosp-mirror/platform_packages_apps_camera/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_camera.png` |
| `calendar` | [platform_packages_apps_calendar](https://github.com/aosp-mirror/platform_packages_apps_calendar/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_calendar.png` |
| `calculator` | [platform_packages_apps_calculator](https://github.com/aosp-mirror/platform_packages_apps_calculator/tree/android-4.4.4_r2) | `res/mipmap-xxxhdpi/ic_launcher_calculator.png` |
| `mail` | [platform_packages_apps_email](https://github.com/aosp-mirror/platform_packages_apps_email/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_mail.png` |
| `browser` | [platform_packages_apps_browser](https://github.com/aosp-mirror/platform_packages_apps_browser/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_browser.png` |
| `downloads` | [platform_packages_providers_downloadprovider](https://github.com/aosp-mirror/platform_packages_providers_downloadprovider/tree/android-4.4.4_r2) | `res/mipmap-xxxhdpi/ic_launcher_download.png` |
| `music` | [platform_packages_apps_music](https://github.com/aosp-mirror/platform_packages_apps_music/tree/android-4.4.4_r2) | `res/drawable-hdpi/app_music.png` |
| `clock` | [platform_packages_apps_deskclock](https://github.com/aosp-mirror-neo/platform_packages_apps_deskclock/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_alarmclock.png` |
| `gallery` | [platform_packages_apps_gallery2](https://github.com/aosp-mirror-neo/platform_packages_apps_gallery2/tree/android-4.4.4_r2) | `res/mipmap-xhdpi/ic_launcher_gallery.png` |

Each listed AOSP module contains the `MODULE_LICENSE_APACHE2` marker and a `NOTICE` file. The applicable license text is included in this repository at [LICENSE](LICENSE). The files are imported without redrawing or changing their artwork; only their Android resource filenames and density-folder placement are adapted for this icon-pack APK.

The build script downloads from the pinned Android 4.4.4 release tag and fails the build if a required PNG cannot be retrieved or does not have a valid PNG signature.

Contacts is deliberately excluded: although the Contacts manifest references `ic_launcher_contacts`, that PNG is absent from the pinned AOSP tag tree. Contacts is deliberately excluded: its manifest references an icon resource that is absent from the pinned source tree. The Phone icon is imported from [AOSP Phone, android-4.3_r1.1](https://github.com/aosp-mirror-neo/platform_packages_apps_phone/tree/android-4.3_r1.1/res/mipmap-xhdpi) because the Nexus 5 Android 4.4.4 image uses Google Phone instead of the AOSP Phone app. It remains Apache-2.0 AOSP artwork and is explicitly identified as Jelly Bean-era, not Android 4.4.4 artwork. The `phone` importer source is pinned separately in `scripts/import_kitkat_aosp_icons.py`.

`google_plus.png` is a separate public-domain asset from [Wikimedia Commons, Google Plus icon (2013–2015)](https://commons.wikimedia.org/wiki/File:Google_Plus_icon_(2013-2015).png), as identified in Android Time Machine third-party notices. It is not an AOSP asset and is not covered by the Apache license above.

The other icons in the KitKat pack are not claimed to be original Android 4.4.4 artwork until their sources are verified. Proprietary Google APK artwork (including Chrome and Maps) is intentionally not imported under the AOSP license.
