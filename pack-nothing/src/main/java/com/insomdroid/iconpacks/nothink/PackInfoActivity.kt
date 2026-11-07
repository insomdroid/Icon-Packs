package com.insomdroid.iconpacks.nothink

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val message = """
            Nothink Icon Pack

            Original geometric icon artwork with mappings for supported Android applications.

            Apply in Nova Launcher:
            1. Open Nova Settings.
            2. Select Look & feel, then Icon style.
            3. Open the Icon theme selector and choose Nothink.

            Apply in Lawnchair:
            1. Open Lawnchair Settings.
            2. Select General, then Icon pack.
            3. Choose Nothink.

            Coverage depends on the installed application package and activity matching a mapping included in this build.
        """.trimIndent()

        setContentView(TextView(this).apply {
            text = message
            textSize = 16f
            setLineSpacing(6f, 1f)
            setPadding(32, 48, 32, 32)
        })
    }
}
