package com.insomdroid.iconpacks

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.insomdroid.iconpacks.core.PackCatalog
import com.insomdroid.iconpacks.core.PackDefinition

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(Modifier.fillMaxSize()) { CatalogScreen() }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun CatalogScreen() {
    Scaffold(topBar = {
        TopAppBar(title = {
            Column {
                Text("INSOMDROID")
                Text("ICON PACKS", style = MaterialTheme.typography.labelSmall)
            }
        })
    }) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Text("One collection. Four visual languages.", style = MaterialTheme.typography.headlineSmall)
                Text(
                    "Choose a style and install its independent icon pack APK. Installed packs are designed to work separately from this catalog.",
                    style = MaterialTheme.typography.bodyMedium,
                    modifier = Modifier.padding(top = 8.dp, bottom = 8.dp)
                )
            }
            items(PackCatalog.packs, key = PackDefinition::id) { pack ->
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(18.dp)) {
                        Text(pack.name, style = MaterialTheme.typography.titleLarge)
                        Text(pack.description, modifier = Modifier.padding(top = 6.dp))
                        Text(pack.designDirection, style = MaterialTheme.typography.labelMedium, modifier = Modifier.padding(top = 10.dp))
                        Text("Package: ${pack.applicationId}", style = MaterialTheme.typography.labelSmall, modifier = Modifier.padding(top = 10.dp))
                        Text("Status: foundation", style = MaterialTheme.typography.labelSmall)
                    }
                }
            }
            item {
                Text(
                    "This foundation does not yet contain a complete app icon collection. Verified mappings and finished original artwork will be added progressively.",
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}
