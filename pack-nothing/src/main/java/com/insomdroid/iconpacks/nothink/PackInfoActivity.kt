package com.insomdroid.iconpacks.nothink

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val message = """
            Nothink Icon Pack

            Monochrome app artwork exported from the Nothink Figma source.

            Apply the pack:
            1. Open Nova Launcher or Lawnchair settings.
            2. Find the Icon style or Icon pack option.
            3. Select Nothink Icon Pack.

            The available icons depend on the Figma artwork successfully matched to installed app components.
        """.trimIndent()
        setContentView(TextView(this).apply {
            text = message
            textSize = 16f
            setLineSpacing(6f, 1f)
            setPadding(32, 48, 32, 32)
        })
    }
}
