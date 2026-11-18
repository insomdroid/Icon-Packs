package com.insomdroid.iconpacks.kitkat

import android.Manifest
import android.app.WallpaperManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import org.xmlpull.v1.XmlPullParser
import java.util.Locale
import com.insomdroid.iconpacks.kitkat.widget.KitKatClockWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.KitKatCalendarWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.KitKatDigitalClockWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.KitKatSearchWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.KitKatMusicWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.KitKatGalleryWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.KitKatPowerWidgetProvider
import com.insomdroid.iconpacks.kitkat.widget.pinKitKatWidget

class PackInfoActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(
                colorScheme = lightColorScheme(
                    primary = Color(0xFF33B5E5),
                    onPrimary = Color.White,
                    surface = Color.White,
                    background = Color(0xFFF1F1F1)
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

                if (!drawableName.isNullOrBlank() &&
                    !drawableName.startsWith("kitkat_") &&
                    drawableName != "aosp_wallpaper"
                ) {
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
    var selectedIcon by remember { mutableStateOf<KitKatIcon?>(null) }
    var activeCategory by remember { mutableStateOf<String?>(null) }
    val kitKatIcons = remember(context) { loadKitKatIcons(context) }
    val calendarPermissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            pinKitKatWidget(context, KitKatCalendarWidgetProvider::class.java, "KitKat Calendar")
        } else {
            Toast.makeText(context, "Calendar access was not granted.", Toast.LENGTH_SHORT).show()
        }
    }

    BackHandler(enabled = activeCategory != null) {
        activeCategory = null
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                if (activeCategory == null) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Text(
                            "HoloKat",
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF212121)
                        )
                        Text(
                            "Android 4.4.4",
                            style = MaterialTheme.typography.bodySmall,
                            color = Color(0xFF666666)
                        )
                        CategoryTile(
                            title = "Icons",
                            subtitle = "${kitKatIcons.size} KitKat application icons"
                        ) { activeCategory = "Icons" }
                        CategoryTile(
                            title = "Widgets",
                            subtitle = "Seven classic home-screen widgets"
                        ) { activeCategory = "Widgets" }
                        CategoryTile(
                            title = "Wallpapers",
                            subtitle = "Original KitKat and AOSP wallpapers"
                        ) { activeCategory = "Wallpapers" }
                    }
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        TextButton(
                            onClick = { activeCategory = null },
                            contentPadding = PaddingValues(horizontal = 0.dp, vertical = 4.dp)
                        ) {
                            Text("‹  BACK")
                        }
                        Text(
                            activeCategory!!.uppercase(Locale.ROOT),
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0099CC)
                        )
                    }
                }
            }

            when (activeCategory) {
                "Icons" -> {
                    items(kitKatIcons.chunked(4)) { iconRow ->
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            iconRow.forEach { icon ->
                                IconTile(
                                    icon = icon,
                                    modifier = Modifier.weight(1f)
                                ) {
                                    selectedIcon = icon
                                }
                            }
                            repeat(4 - iconRow.size) {
                                Spacer(modifier = Modifier.weight(1f))
                            }
                        }
                    }
                }

                "Widgets" -> {
                    item {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            WidgetRow("Analog Clock", "Original KitKat clock face") {
                                pinKitKatWidget(context, KitKatClockWidgetProvider::class.java, "KitKat Analog Clock")
                            }
                            WidgetRow("Digital Clock", "Transparent digital time and date") {
                                pinKitKatWidget(context, KitKatDigitalClockWidgetProvider::class.java, "KitKat Digital Clock")
                            }
                            WidgetRow("Calendar", "Upcoming events") {
                                if (context.checkSelfPermission(Manifest.permission.READ_CALENDAR) == PackageManager.PERMISSION_GRANTED) {
                                    pinKitKatWidget(context, KitKatCalendarWidgetProvider::class.java, "KitKat Calendar")
                                } else {
                                    calendarPermissionLauncher.launch(Manifest.permission.READ_CALENDAR)
                                }
                            }
                            WidgetRow("Search", "Transparent Google search and voice search") {
                                pinKitKatWidget(context, KitKatSearchWidgetProvider::class.java, "KitKat Search")
                            }
                            WidgetRow("Music Player", "Original Google Play Music controls") {
                                pinKitKatWidget(context, KitKatMusicWidgetProvider::class.java, "KitKat Music Player")
                                try {
                                    context.startActivity(Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"))
                                } catch (_: Exception) {
                                }
                            }
                            WidgetRow("Photo Gallery", "Choose a photo for the home screen") {
                                pinKitKatWidget(context, KitKatGalleryWidgetProvider::class.java, "KitKat Photo Gallery")
                            }
                            WidgetRow("Power Control", "Classic system control shortcuts") {
                                pinKitKatWidget(context, KitKatPowerWidgetProvider::class.java, "KitKat Power Control")
                            }
                        }
                    }
                }

                "Wallpapers" -> {
                    item {
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            WallpaperOption(
                                "KitKat",
                                "Default",
                                R.drawable.kitkat_wallpaper,
                                Modifier.weight(1f)
                            ) {
                                applyWallpaper(context, R.drawable.kitkat_wallpaper)
                            }
                            WallpaperOption(
                                "AOSP",
                                "Classic",
                                R.drawable.aosp_wallpaper,
                                Modifier.weight(1f)
                            ) {
                                applyWallpaper(context, R.drawable.aosp_wallpaper)
                            }
                        }
                    }
                }
            }

            item {
                TextButton(
                    onClick = {
                        context.startActivity(
                            Intent(
                                Intent.ACTION_VIEW,
                                Uri.parse("https://github.com/insomdroid/Icon-Packs")
                            )
                        )
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("GitHub")
                }
            }
        }
    }

    selectedIcon?.let { icon ->
        AlertDialog(
            onDismissRequest = { selectedIcon = null },
            confirmButton = {
                TextButton(onClick = { selectedIcon = null }) {
                    Text("Close")
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
                }
            }
        )
    }
}

@Composable
private fun CategoryTile(
    title: String,
    subtitle: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(4.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 18.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Text(
                    title,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF222222)
                )
                Text(
                    subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color(0xFF666666)
                )
            }
            Text(
                "›",
                color = Color(0xFF0099CC),
                fontSize = 28.sp
            )
        }
    }
}

private fun applyWallpaper(context: Context, resourceId: Int) {
    try {
        val manager = WallpaperManager.getInstance(context)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) manager.setResource(resourceId, WallpaperManager.FLAG_SYSTEM) else manager.setResource(resourceId)
        Toast.makeText(context, "Wallpaper applied successfully", Toast.LENGTH_SHORT).show()
    } catch (error: Exception) {
        Toast.makeText(context, "Could not apply wallpaper: ${error.localizedMessage}", Toast.LENGTH_LONG).show()
    }
}

@Composable
private fun WallpaperOption(title: String, subtitle: String, wallpaperId: Int, modifier: Modifier = Modifier, onApply: () -> Unit) {
    Card(modifier = modifier, shape = RoundedCornerShape(4.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Image(painter = painterResource(wallpaperId), contentDescription = title, modifier = Modifier.fillMaxWidth().height(112.dp), contentScale = ContentScale.Crop)
            Text(title, modifier = Modifier.padding(start = 10.dp, end = 10.dp), fontWeight = FontWeight.Bold)
            Text(subtitle, modifier = Modifier.padding(horizontal = 10.dp), style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            TextButton(onClick = onApply, modifier = Modifier.fillMaxWidth()) { Text("Apply") }
        }
    }
}

@Composable
private fun WidgetRow(title: String, subtitle: String, onAdd: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 14.dp, vertical = 10.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(modifier = Modifier.weight(1f)) {
                Text(title, fontWeight = FontWeight.SemiBold, color = Color(0xFF212121))
                Text(subtitle, style = MaterialTheme.typography.bodySmall, color = Color(0xFF757575))
            }
            TextButton(onClick = onAdd) { Text("ADD") }
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
        shape = RoundedCornerShape(4.dp),
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
                color = Color(0xFF0099CC)
            )
            Text(
                text = label,
                style = MaterialTheme.typography.bodySmall,
                color = Color(0xFF666666)
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
            .aspectRatio(1f)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(4.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Image(
            painter = painterResource(icon.resourceId),
            contentDescription = icon.name,
            modifier = Modifier
                .fillMaxSize()
                .padding(7.dp),
            contentScale = ContentScale.Fit
        )
    }
}
