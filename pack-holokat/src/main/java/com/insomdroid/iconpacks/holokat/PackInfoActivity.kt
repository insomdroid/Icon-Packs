package com.insomdroid.iconpacks.holokat

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(TextView(this).apply {
            text = """
                Holokat Icon Pack

                An independent icon pack based on the two Jelly Bean icon collections supplied for this project.

                Apply the pack:
                1. Open your launcher's settings.
                2. Find Icon style or Icon pack.
                3. Select Holokat Icon Pack.

                The pack includes original image files from the supplied archives. Icon mappings are provided for supported applications where a reliable match is available.

                Artwork source: HKtorito, DeviantArt gallery.
                https://www.deviantart.com/hktorito/gallery

                Please see the project attribution notice for source and rights information.
            """.trimIndent()
            textSize = 16f
            setLineSpacing(6f, 1f)
            setPadding(32, 48, 32, 32)
        })
    }
}
