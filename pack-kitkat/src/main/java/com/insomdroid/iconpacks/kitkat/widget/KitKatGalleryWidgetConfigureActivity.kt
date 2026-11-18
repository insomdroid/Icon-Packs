package com.insomdroid.iconpacks.kitkat.widget

import android.app.Activity
import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.RemoteViews
import android.widget.Toast
import com.insomdroid.iconpacks.kitkat.R

class KitKatGalleryWidgetConfigureActivity : Activity() {
    private var appWidgetId = AppWidgetManager.INVALID_APPWIDGET_ID

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setResult(RESULT_CANCELED)
        appWidgetId = intent.getIntExtra(
            AppWidgetManager.EXTRA_APPWIDGET_ID,
            AppWidgetManager.INVALID_APPWIDGET_ID
        )
        if (appWidgetId == AppWidgetManager.INVALID_APPWIDGET_ID) {
            finish()
            return
        }

        val picker = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/*"
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
        }

        try {
            startActivityForResult(picker, REQUEST_IMAGE)
        } catch (_: Exception) {
            Toast.makeText(this, "No photo picker is available.", Toast.LENGTH_LONG).show()
            finish()
        }
    }

    @Deprecated("Deprecated by Android in favor of Activity Result APIs")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_IMAGE) return

        val uri: Uri? = data?.data
        if (resultCode == RESULT_OK && uri != null) {
            try {
                val readPermission = data.flags and Intent.FLAG_GRANT_READ_URI_PERMISSION
                contentResolver.takePersistableUriPermission(uri, readPermission)
            } catch (_: SecurityException) {
            } catch (_: IllegalArgumentException) {
            }

            getSharedPreferences(PREFERENCES, MODE_PRIVATE)
                .edit()
                .putString("photo_$appWidgetId", uri.toString())
                .apply()

            val manager = AppWidgetManager.getInstance(this)
            val views = RemoteViews(packageName, R.layout.kitkat_gallery_widget)
            views.setImageViewUri(R.id.gallery_widget_image, uri)

            val openIntent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(uri, "image/*")
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            val openPending = PendingIntent.getActivity(
                this,
                appWidgetId * 2,
                openIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.gallery_widget_image, openPending)

            val configureIntent = Intent(this, KitKatGalleryWidgetConfigureActivity::class.java)
                .putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
            val configurePending = PendingIntent.getActivity(
                this,
                appWidgetId * 2 + 1,
                configureIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.gallery_widget_open, configurePending)
            manager.updateAppWidget(appWidgetId, views)

            setResult(RESULT_OK, Intent().putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId))
        } else {
            AppWidgetManager.getInstance(this).deleteAppWidgetId(appWidgetId)
        }
        finish()
    }

    private companion object {
        const val REQUEST_IMAGE = 4104
        const val PREFERENCES = "holokat_gallery_widgets"
    }
}
