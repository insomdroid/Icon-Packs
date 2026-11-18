package com.insomdroid.iconpacks.kitkat

import android.app.WallpaperManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.xmlpull.v1.XmlPullParser
import java.util.Locale

class PackInfoActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(
                colorScheme = lightColorScheme(
                    primary = Color(0xFF3F51B5),
                    onPrimary = Color.White,
                    surface = Color(0xFFF7F7FA),
                    background = Color(0xFFF7F7FA)
                )
            ) {
                KitKatPackDashboard()
            }
        }
    }
}

private data class KitKatIcon(
    val name: String,
    val resourceId: Int
)

private fun loadKitKatIcons(context: Context): List<KitKatIcon> {
    val parser = context.resources.getXml(R.xml.drawable)
    val iconsByResource = linkedMapOf<Int, KitKatIcon>()

    try {
        while (parser.eventType != XmlPullParser.END_DOCUMENT) {
            if (parser.eventType == XmlPullParser.START_TAG && parser.name == "item") {
                val drawableName = parser.getAttributeValue(null, "drawable")
                    ?: parser.getAttributeValue(null, "name")

                if (!drawableName.isNullOrBlank()) {
                    val resourceId = context.resources.getIdentifier(
                        drawableName,
                        "drawable",
                        context.packageName
                    )

                    if (resourceId != 0 && !iconsByResource.containsKey(resourceId)) {
                        val displayName = drawableName
                            .split('_')
                            .joinToString(" ") { part ->
                                part.replaceFirstChar { character -> character.uppercase() }
                            }
                        iconsByResource[resourceId] = KitKatIcon(displayName, resourceId)
                    }
                }
            }
            parser.next()
        }
    } finally {
        parser.close()
    }

    return iconsByResource.values.sortedBy { it.name.lowercase(Locale.ROOT) }
}

@Composable
private fun KitKatPackDashboard() {
    val context = LocalContext.current
    var selectedIcon by remember { mutableStateOf<KitKatIcon?>(null) }\n    val kitKatIcons = remember(context) { loadKitKatIcons(context) }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 18.dp),
            verticalArrangement = Arrangement.spacedBy(18.dp)
        ) {
            Text(
                text = "HOLOKAT",
                style = MaterialTheme.typography.labelLarge,
                color = Color(0xFF687080),
                fontWeight = FontWeight.Bold,
                letterSpacing = 2.sp
            )

            Text(
                text = "HoloKat Icon Pack",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF171923)
            )

            Text(
                text = "Android 4.4.4 • Original artwork collection",
                style = MaterialTheme.typography.bodyMedium,
                color = Color(0xFF687080)
            )

            WallpaperHero(
                onApply = {
                    try {
                        val manager = WallpaperManager.getInstance(context)
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                            manager.setResource(R.drawable.kitkat_wallpaper, WallpaperManager.FLAG_SYSTEM)
                        } else {
                            manager.setResource(R.drawable.kitkat_wallpaper)
                        }
                        Toast.makeText(context, "KitKat wallpaper applied successfully", Toast.LENGTH_SHORT).show()
                    } catch (error: Exception) {
                        Toast.makeText(context, "Could not apply wallpaper: ${error.localizedMessage}", Toast.LENGTH_LONG).show()
                    }
                }
            )

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White)
            ) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("KitKat Analog Clock", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Text(
                        "An analog clock featuring the original KitKat dial and hands. Add it to your home screen using the Android widget picker.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color(0xFF687080)
                    )
                    Button(
                        onClick = {
                            try {
                                val pinIntentSupported = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O &&
                                    android.appwidget.AppWidgetManager.getInstance(context).isRequestPinAppWidgetSupported
                                if (pinIntentSupported) {
                                    android.appwidget.AppWidgetManager.getInstance(context).requestPinAppWidget(
                                        ComponentName(context, com.insomdroid.iconpacks.kitkat.widget.KitKatClockWidgetProvider::class.java),
                                        null,
                                        null
                                    )
                                } else {
                                    Toast.makeText(context, "Open the home screen widget picker and select KitKat Analog Clock.", Toast.LENGTH_LONG).show()
                                }
                            } catch (error: Exception) {
                                Toast.makeText(context, "Buka daftar Widget dari home screen lalu pilih KitKat Analog Clock.", Toast.LENGTH_LONG).show()
                            }
                        },
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Text("Add clock widget")
                    }
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                SummaryTile(
                    value = "32",
                    label = "Ikon klasik",
                    modifier = Modifier.weight(1f)
                )
                SummaryTile(
                    value = "4.4.4",
                    label = "Android KitKat",
                    modifier = Modifier.weight(1f)
                )
            }

            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = "Explore icons",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF171923)
                )
                Text(
                    text = "Tap any icon to preview the artwork at a larger size.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color(0xFF687080)
                )
            }

            kitKatIcons.chunked(4).forEach { iconRow ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    iconRow.forEach { icon ->
                        IconTile(
                            icon = icon,
                            modifier = Modifier.weight(1f),
                            onClick = { selectedIcon = icon }
                        )
                    }
                    repeat(4 - iconRow.size) {
                        Spacer(modifier = Modifier.weight(1f))
                    }
                }
            }

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White)
            ) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Text(
                        text = "About this collection",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "This collection preserves original KitKat icons, including artwork for discontinued apps. Launcher mappings also cover successor apps when names or functions have changed.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color(0xFF687080)
                    )
                    Text(
                        text = "The wallpaper and original artwork are sourced from the Android Time Machine Android 4.4.4 archive.",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color(0xFF687080)
                    )
                }
            }

            Text(
                text = "HOLOKAT ICON PACK",
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                style = MaterialTheme.typography.labelSmall,
                color = Color(0xFF9299A5)
            )
        }
    }

    selectedIcon?.let { icon ->
        AlertDialog(
            onDismissRequest = { selectedIcon = null },
            confirmButton = {
                TextButton(onClick = { selectedIcon = null }) {
                    Text("Tutup")
                }
            },
            title = {
                Text(icon.name, fontWeight = FontWeight.Bold)
            },
            text = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Image(
                        painter = painterResource(icon.resourceId),
                        contentDescription = icon.name,
                        modifier = Modifier.size(176.dp),
                        contentScale = ContentScale.Fit
                    )
                    Text(
                        text = icon.description,
                        color = Color(0xFF687080),
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }
        )
    }
}

@Composable
private fun WallpaperHero(onApply: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(224.dp)
            .clip(RoundedCornerShape(22.dp))
    ) {
        Image(
            painter = painterResource(R.drawable.kitkat_wallpaper),
            contentDescription = "Wallpaper resmi Android KitKat 4.4.4",
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Crop
        )
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(Color.Transparent, Color(0xCC10131B))
                    )
                )
        )
        Column(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Text(
                text = "THE ANDROID CLASSIC",
                color = Color.White.copy(alpha = 0.82f),
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.5.sp
            )
            Text(
                text = "Android 4.4 KitKat",
                color = Color.White,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Button(
                onClick = onApply,
                contentPadding = PaddingValues(horizontal = 14.dp, vertical = 8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3F51B5))
            ) {
                Text("Terapkan wallpaper")
            }
        }
    }
}

@Composable
private fun SummaryTile(
    value: String,
    label: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(3.dp)
        ) {
            Text(
                text = value,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF303F9F)
            )
            Text(
                text = label,
                style = MaterialTheme.typography.bodySmall,
                color = Color(0xFF687080)
            )
        }
    }
}

@Composable
private fun IconTile(
    icon: KitKatIcon,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Card(
        modifier = modifier
            .aspectRatio(0.82f)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(15.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 5.dp, vertical = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Image(
                painter = painterResource(icon.resourceId),
                contentDescription = icon.name,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(5.dp),
                contentScale = ContentScale.Fit
            )
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = icon.name,
                style = MaterialTheme.typography.labelSmall,
                color = Color(0xFF303541),
                maxLines = 2,
                minLines = 2,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}
