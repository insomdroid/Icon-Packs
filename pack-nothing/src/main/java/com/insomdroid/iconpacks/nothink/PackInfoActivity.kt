package com.insomdroid.iconpacks.nothink

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val message = """
            Nothink Icon Pack — 100 App Trial

            This test build uses real launcher artwork extracted from application APKs and processed with the JusIcons monochrome pipeline.

            Apply the pack:
            1. Open Nova Launcher or Lawnchair settings.
            2. Find the Icon style or Icon pack option.
            3. Select Nothink Icon Pack.

            This trial targets 100 Google and popular applications. Actual coverage depends on the launcher activities and APK versions available during the build.
        """.trimIndent()
        setContentView(TextView(this).apply {
            text = message
            textSize = 16f
            setLineSpacing(6f, 1f)
            setPadding(32, 48, 32, 32)
        })
    }
}
