package com.insomdroid.iconpacks.kitkat.widget

import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Matrix
import android.widget.RemoteViews
import com.insomdroid.iconpacks.kitkat.R
import java.util.Calendar

class KitKatClockWidgetProvider : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        appWidgetIds.forEach { appWidgetId ->
            updateWidget(context, appWidgetManager, appWidgetId)
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        when (intent.action) {
            Intent.ACTION_TIME_TICK,
            Intent.ACTION_TIME_CHANGED,
            Intent.ACTION_TIMEZONE_CHANGED,
            Intent.ACTION_DATE_CHANGED -> {
                val manager = AppWidgetManager.getInstance(context)
                val ids = manager.getAppWidgetIds(
                    android.content.ComponentName(context, javaClass)
                )
                ids.forEach { updateWidget(context, manager, it) }
            }
        }
    }

    companion object {
        private fun updateWidget(
            context: Context,
            manager: AppWidgetManager,
            appWidgetId: Int
        ) {
            val now = Calendar.getInstance()
            val hour = now.get(Calendar.HOUR)
            val minute = now.get(Calendar.MINUTE)
            val views = RemoteViews(context.packageName, R.layout.kitkat_clock_widget)

            views.setImageViewBitmap(
                R.id.clock_hour,
                rotatedHand(context, R.drawable.kitkat_clock_hour, hour * 30f + minute * 0.5f)
            )
            views.setImageViewBitmap(
                R.id.clock_minute,
                rotatedHand(context, R.drawable.kitkat_clock_minute, minute * 6f)
            )
            manager.updateAppWidget(appWidgetId, views)
        }

        private fun rotatedHand(context: Context, drawableId: Int, degrees: Float): Bitmap {
            val source = android.graphics.BitmapFactory.decodeResource(
                context.resources,
                drawableId
            )
            val output = Bitmap.createBitmap(
                source.width,
                source.height,
                Bitmap.Config.ARGB_8888
            )
            val canvas = Canvas(output)
            val matrix = Matrix().apply {
                setRotate(degrees, source.width / 2f, source.height / 2f)
            }
            canvas.drawBitmap(source, matrix, android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG))
            source.recycle()
            return output
        }
    }
}