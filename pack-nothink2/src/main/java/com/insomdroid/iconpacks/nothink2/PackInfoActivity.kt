package com.insomdroid.iconpacks.nothink2

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class PackInfoActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(
                colorScheme = darkColorScheme(
                    background = Color(0xFF101010),
                    surface = Color(0xFF171717),
                    onBackground = Color(0xFFF5F5F5),
                    onSurface = Color(0xFFF5F5F5)
                )
            ) {
                Nothink2InfoScreen()
            }
        }
    }
}

@Composable
private fun Nothink2InfoScreen() {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = Color(0xFF101010)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 28.dp, vertical = 36.dp),
            verticalArrangement = Arrangement.Top
        ) {
            Text(
                text = "Nothink2",
                fontSize = 30.sp,
                fontWeight = FontWeight.SemiBold,
                color = Color(0xFFFFFFFF)
            )
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = "Lawnicons artwork with a restrained Nothing OS 5.0 dark presentation.",
                fontSize = 15.sp,
                lineHeight = 23.sp,
                color = Color(0xFFCCCCCC)
            )
            Spacer(modifier = Modifier.height(28.dp))
            Text(
                text = "APPLY ICONS",
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFFFFFFFF)
            )
            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = "1. Open your launcher settings.\n2. Open Icon Pack or Icon Style.\n3. Choose Nothink2.",
                fontSize = 15.sp,
                lineHeight = 25.sp,
                color = Color(0xFFCCCCCC)
            )
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "ADAPTIVE ICONS",
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFFFFFFFF)
            )
            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = "The original dark background and white artwork are retained. Compatible launchers can apply their selected adaptive shape. Launchers differ in how they handle adaptive icon-pack resources, so exact shape support cannot be guaranteed on every launcher.",
                fontSize = 15.sp,
                lineHeight = 23.sp,
                color = Color(0xFFCCCCCC)
            )
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "THEMED COLORS",
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFFFFFFFF)
            )
            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = "Enable Themed Icons in Android and in a compatible launcher to apply wallpaper-derived colors. Without themed-icon support, icons keep their original dark background and white artwork. Availability depends on Android version and launcher support.",
                fontSize = 15.sp,
                lineHeight = 23.sp,
                color = Color(0xFFCCCCCC)
            )
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Artwork source: Lawnicons (Apache-2.0). Nothink2 is an independent, unofficial project.",
                fontSize = 12.sp,
                lineHeight = 19.sp,
                color = Color(0xFF888888)
            )
        }
    }
}
