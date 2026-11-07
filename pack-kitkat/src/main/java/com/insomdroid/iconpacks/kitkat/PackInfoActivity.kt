package com.insomdroid.iconpacks.kitkat

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val message = """
            KitKat Icon Pack

            32 original KitKat-inspired icons are included in this build, with launcher mappings for Android system apps, Google apps and popular third-party apps.

            Apply the pack:
            1. Open your launcher's settings.
            2. Find the Icon style or Icon pack option.
            3. Select KitKat Icon Pack.

            Launcher integrations are provided for Nova Launcher, ADW Launcher, Action Launcher and Lawnchair. Actual coverage depends on the app versions and launcher activities installed on your device.

            More icons and device-specific mappings will be added in later updates.
        """.trimIndent()

        setContentView(TextView(this).apply {
            text = message
            textSize = 16f
            setLineSpacing(6f, 1f)
            setPadding(32, 48, 32, 32)
        })
    }
}
