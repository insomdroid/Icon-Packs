package com.insomdroid.iconpacks.kitkat.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.widget.RemoteViews
import com.insomdroid.iconpacks.kitkat.R

class KitKatGalleryWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { updateWidget(context, manager, it) }
    }

    companion object {
        fun updateWidget(context: Context, manager: AppWidgetManager, appWidgetId: Int) {
            val views = RemoteViews(context.packageName, R.layout.kitkat_gallery_widget)
            val preferences = context.getSharedPreferences("holokat_gallery_widgets", Context.MODE_PRIVATE)
            val uriValue = preferences.getString("photo_$appWidgetId", null)
            val photoUri = uriValue?.let(Uri::parse)

            if (photoUri != null) {
                views.setImageViewUri(R.id.gallery_widget_image, photoUri)
                val openIntent = Intent(Intent.ACTION_VIEW).apply {
                    setDataAndType(photoUri, "image/*")
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                val openPending = PendingIntent.getActivity(
                    context,
                    appWidgetId * 2,
                    openIntent,
                    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
                )
                views.setOnClickPendingIntent(R.id.gallery_widget_image, openPending)
            } else {
                views.setImageViewResource(R.id.gallery_widget_image, R.drawable.kitkat_gallery_preview)
            }

            val configureIntent = Intent(context, KitKatGalleryWidgetConfigureActivity::class.java)
                .putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
            val configurePending = PendingIntent.getActivity(
                context,
                appWidgetId * 2 + 1,
                configureIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.gallery_widget_open, configurePending)
            manager.updateAppWidget(appWidgetId, views)
        }

        fun updateAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(ComponentName(context, KitKatGalleryWidgetProvider::class.java))
            ids.forEach { updateWidget(context, manager, it) }
        }
    }
}
