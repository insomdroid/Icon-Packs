# Android 4.4.4 AOSP icon assets

This project imports the following original PNG application icons from the Android Open Source Project source tag `android-4.4.4_r2`:

| Pack drawable | AOSP source repository | Source resource |
|---|---|---|
| `contacts` | [platform_packages_apps_mms](https://github.com/aosp-mirror/platform_packages_apps_mms/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_contacts.png` |
| `messages` | [platform_packages_apps_mms](https://github.com/aosp-mirror/platform_packages_apps_mms/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_smsmms.png` |
| `settings` | [platform_packages_apps_settings](https://github.com/aosp-mirror/platform_packages_apps_settings/tree/android-4.4.4_r2) | `res/mipmap-xxxhdpi/ic_launcher_settings.png` |
| `camera` | [platform_packages_apps_camera](https://github.com/aosp-mirror/platform_packages_apps_camera/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_camera.png` |
| `calendar` | [platform_packages_apps_calendar](https://github.com/aosp-mirror/platform_packages_apps_calendar/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_calendar.png` |
| `calculator` | [platform_packages_apps_calculator](https://github.com/aosp-mirror/platform_packages_apps_calculator/tree/android-4.4.4_r2) | `res/mipmap-xxxhdpi/ic_launcher_calculator.png` |
| `mail` | [platform_packages_apps_email](https://github.com/aosp-mirror/platform_packages_apps_email/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_email.png` |
| `browser` | [platform_packages_apps_browser](https://github.com/aosp-mirror/platform_packages_apps_browser/tree/android-4.4.4_r2) | `res/mipmap-xxhdpi/ic_launcher_browser.png` |

Each listed AOSP module contains the `MODULE_LICENSE_APACHE2` marker and a `NOTICE` file. The applicable license text is included in this repository at [third_party/lawnicons/LICENSE](../lawnicons/LICENSE). The files are imported without redrawing or changing their artwork; only their Android resource filenames and density-folder placement are adapted for this icon-pack APK.

The build script downloads from the pinned Android 4.4.4 release tag and fails the build if a required PNG cannot be retrieved or does not have a valid PNG signature.

These eight assets cover only the listed AOSP built-in apps. The other icons in the KitKat pack are not claimed to be original Android 4.4.4 artwork until their sources are verified.
