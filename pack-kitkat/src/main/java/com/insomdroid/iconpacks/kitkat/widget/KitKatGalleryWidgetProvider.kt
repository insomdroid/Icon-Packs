package com.insomdroid.iconpacks.kitkat.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.MediaStore
import android.widget.RemoteViews
import com.insomdroid.iconpacks.kitkat.R

class KitKatGalleryWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { id ->
            val views = RemoteViews(context.packageName, R.layout.kitkat_gallery_widget)
            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, "image/*")
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            val pending = PendingIntent.getActivity(context, id, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            views.setOnClickPendingIntent(R.id.gallery_widget_open, pending)
            manager.updateAppWidget(id, views)
        }
    }
}
