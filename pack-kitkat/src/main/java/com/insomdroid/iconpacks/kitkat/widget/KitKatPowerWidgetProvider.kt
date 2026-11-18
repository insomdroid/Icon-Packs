package com.insomdroid.iconpacks.kitkat.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.provider.Settings
import android.widget.RemoteViews
import com.insomdroid.iconpacks.kitkat.R

class KitKatPowerWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { id ->
            val views = RemoteViews(context.packageName, R.layout.kitkat_power_widget)
            val actions = listOf(
                R.id.power_wifi to Settings.ACTION_WIFI_SETTINGS,
                R.id.power_bluetooth to Settings.ACTION_BLUETOOTH_SETTINGS,
                R.id.power_location to Settings.ACTION_LOCATION_SOURCE_SETTINGS,
                R.id.power_sync to Settings.ACTION_SYNC_SETTINGS,
                R.id.power_brightness to Settings.ACTION_DISPLAY_SETTINGS
            )
            actions.forEachIndexed { index, (viewId, setting) ->
                val intent = Intent(context, KitKatPowerWidgetProvider::class.java)
                    .setAction("com.insomdroid.holokat.power.$index")
                    .putExtra("setting", setting)
                val pending = PendingIntent.getBroadcast(context, id * 10 + index, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
                views.setOnClickPendingIntent(viewId, pending)
            }
            manager.updateAppWidget(id, views)
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        val setting = intent.getStringExtra("setting") ?: return
        try {
            context.startActivity(Intent(setting).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        } catch (_: Exception) {
            context.startActivity(Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        }
    }
}
