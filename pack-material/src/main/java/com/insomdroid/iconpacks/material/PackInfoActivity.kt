package com.insomdroid.iconpacks.material

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class PackInfoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(TextView(this).apply {
            text = "Material Icon Pack\n\nThis independently installable theme package is the project foundation. Verified launcher mappings and finished original icon artwork will be added in future updates."
            textSize = 18f
            setPadding(32, 48, 32, 32)
        })
    }
}
