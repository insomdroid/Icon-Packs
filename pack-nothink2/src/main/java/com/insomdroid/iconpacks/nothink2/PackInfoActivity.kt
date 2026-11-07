package com.insomdroid.iconpacks.nothink2

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val content = """
            Nothink2

            Lawnicons artwork with a restrained Nothing OS 5.0 dark presentation.

            Apply classic icons:
            1. Open your launcher settings.
            2. Open Icon Pack / Icon Style.
            3. Choose Nothink2.

            Enable Themed Icons in Android and your launcher to use wallpaper-derived colors.
            Icon shape is controlled by your launcher and follows its selected device shape.

            Artwork source: Lawnicons (Apache-2.0).
        """.trimIndent()
        setContentView(TextView(this).apply {
            text = content
            textSize = 16f
            setTextColor(0xFFF5F5F5.toInt())
            setBackgroundColor(0xFF101010.toInt())
            setLineSpacing(7f, 1f)
            setPadding(32, 48, 32, 32)
        })
    }
}
