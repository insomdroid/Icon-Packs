package com.insomdroid.iconpacks.kitkat.widget

import android.appwidget.AppWidgetManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.MediaStore
import android.provider.Settings
import android.widget.Toast

fun openWidgetTarget(context: Context, target: String) {
    val intent = when (target) {
        "search" -> Intent(Intent.ACTION_WEB_SEARCH)
        "gallery" -> Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, "image/*")
        }
        "wifi" -> Intent(Settings.ACTION_WIFI_SETTINGS)
        "bluetooth" -> Intent(Settings.ACTION_BLUETOOTH_SETTINGS)
        "location" -> Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
        "sync" -> Intent(Settings.ACTION_SYNC_SETTINGS)
        "brightness" -> Intent(Settings.ACTION_DISPLAY_SETTINGS)
        else -> Intent(Settings.ACTION_SETTINGS)
    }.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

    try {
        context.startActivity(intent)
    } catch (_: Exception) {
        Toast.makeText(context, "No compatible system screen was found.", Toast.LENGTH_SHORT).show()
    }
}

fun pinKitKatWidget(context: Context, provider: Class<*>, label: String) {
    val manager = AppWidgetManager.getInstance(context)
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O &&
        manager.isRequestPinAppWidgetSupported
    ) {
        manager.requestPinAppWidget(ComponentName(context, provider), null, null)
    } else {
        Toast.makeText(
            context,
            "Open the home screen widget picker and select $label.",
            Toast.LENGTH_LONG
        ).show()
    }
}
