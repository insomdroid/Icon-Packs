package com.insomdroid.iconpacks.kitkat

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

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
    val resourceId: Int,
    val description: String
)

private val kitKatIcons = listOf(
    KitKatIcon("Apps", R.drawable.apps, "Ikon umum aplikasi"),
    KitKatIcon("Browser", R.drawable.browser, "Browser bawaan Android"),
    KitKatIcon("Calculator", R.drawable.calculator, "Kalkulator"),
    KitKatIcon("Calendar", R.drawable.calendar, "Kalender"),
    KitKatIcon("Camera", R.drawable.camera, "Kamera"),
    KitKatIcon("Chrome", R.drawable.chrome, "Google Chrome"),
    KitKatIcon("Clock", R.drawable.clock, "Jam"),
    KitKatIcon("Downloads", R.drawable.downloads, "Unduhan dan pengelola berkas"),
    KitKatIcon("Drive", R.drawable.drive, "Google Drive"),
    KitKatIcon("Email", R.drawable.mail, "Email AOSP"),
    KitKatIcon("Gallery", R.drawable.gallery, "Galeri AOSP"),
    KitKatIcon("Gmail", R.drawable.gmail, "Gmail"),
    KitKatIcon("Google+", R.drawable.google_plus, "Google Plus"),
    KitKatIcon("Google Search", R.drawable.google_search, "Google Search"),
    KitKatIcon("Google Settings", R.drawable.google_settings, "Pengaturan layanan Google"),
    KitKatIcon("Hangouts", R.drawable.hangouts, "Google Hangouts"),
    KitKatIcon("Keep", R.drawable.keep, "Google Keep"),
    KitKatIcon("Maps", R.drawable.maps, "Google Maps"),
    KitKatIcon("News & Weather", R.drawable.news_weather, "Google News & Weather"),
    KitKatIcon("Newsstand", R.drawable.newsstand, "Google Play Newsstand"),
    KitKatIcon("People", R.drawable.contacts, "Kontak Android"),
    KitKatIcon("Phone", R.drawable.phone, "Telepon"),
    KitKatIcon("Photos", R.drawable.photos, "Google Photos"),
    KitKatIcon("Play Books", R.drawable.play_books, "Google Play Books"),
    KitKatIcon("Play Games", R.drawable.play_games, "Google Play Games"),
    KitKatIcon("Play Movies", R.drawable.play_movies, "Google Play Movies"),
    KitKatIcon("Play Music", R.drawable.play_music, "Google Play Music"),
    KitKatIcon("Quickoffice", R.drawable.quickoffice, "Quickoffice"),
    KitKatIcon("Settings", R.drawable.settings, "Pengaturan Android"),
    KitKatIcon("Voice Search", R.drawable.voice_search, "Google Voice Search"),
    KitKatIcon("Wallet", R.drawable.wallet, "Google Wallet"),
    KitKatIcon("YouTube", R.drawable.youtube, "YouTube")
)

@Composable
private fun KitKatPackDashboard() {
    var selectedIcon by remember { mutableStateOf<KitKatIcon?>(null) }

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
                text = "INSOMDROID",
                style = MaterialTheme.typography.labelLarge,
                color = Color(0xFF687080),
                fontWeight = FontWeight.Bold,
                letterSpacing = 2.sp
            )

            Text(
                text = "KitKat Icon Pack",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF171923)
            )

            Text(
                text = "Android 4.4.4 • Original artwork collection",
                style = MaterialTheme.typography.bodyMedium,
                color = Color(0xFF687080)
            )

            WallpaperHero()

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
                    text = "Jelajahi ikon",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF171923)
                )
                Text(
                    text = "Ketuk ikon untuk melihat artwork dalam ukuran lebih besar.",
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
                        text = "Tentang koleksi",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Koleksi ini mempertahankan seluruh ikon asli KitKat, termasuk aplikasi yang sudah dihentikan. Pemetaan launcher juga mencakup aplikasi penerus ketika nama atau fungsinya berubah.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color(0xFF687080)
                    )
                    Text(
                        text = "Wallpaper dan artwork berasal dari arsip Android Time Machine versi 4.4.4.",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color(0xFF687080)
                    )
                }
            }

            Text(
                text = "INSOMDROID ICON PACKS",
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
private fun WallpaperHero() {
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
