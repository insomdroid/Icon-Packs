package com.insomdroid.iconpacks.nothink

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(
            TextView(this).apply {
                text = "Nothink Icon Pack\n\nMonochrome, Nothing-inspired icons.\n\nApply Nothink from your launcher's icon pack settings. Wallpaper-tinted themed icons are available in compatible launchers."
                textSize = 16f
                setTextColor(0xFF111111.toInt())
                setBackgroundColor(0xFFF5F5F5.toInt())
                setPadding(32, 48, 32, 32)
            }
        )
    }
}
