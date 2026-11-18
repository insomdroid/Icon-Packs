package com.insomdroid.iconpacks.kitkat.widget

import android.Manifest
import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ContentUris
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.provider.CalendarContract
import android.widget.RemoteViews
import com.insomdroid.iconpacks.kitkat.R
import java.text.DateFormat
import java.util.Calendar
import java.util.Date
import java.util.concurrent.TimeUnit

class KitKatCalendarWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { updateWidget(context, manager, it) }
    }

    companion object {
        fun updateWidget(context: Context, manager: AppWidgetManager, appWidgetId: Int) {
            val views = RemoteViews(context.packageName, R.layout.kitkat_calendar_widget)
            val openCalendar = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_APP_CALENDAR)
            val pending = PendingIntent.getActivity(
                context,
                appWidgetId,
                openCalendar,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.calendar_widget_root, pending)

            val eventIds = listOf(
                R.id.calendar_event_1,
                R.id.calendar_event_2,
                R.id.calendar_event_3,
                R.id.calendar_event_4
            )

            if (context.checkSelfPermission(Manifest.permission.READ_CALENDAR) != PackageManager.PERMISSION_GRANTED) {
                views.setTextViewText(R.id.calendar_event_1, context.getString(R.string.calendar_permission_required))
                eventIds.drop(1).forEach { views.setTextViewText(it, "") }
                manager.updateAppWidget(appWidgetId, views)
                return
            }

            val now = Calendar.getInstance()
            val start = now.timeInMillis
            val end = start + TimeUnit.DAYS.toMillis(7)
            val builder = CalendarContract.Instances.CONTENT_URI.buildUpon()
            ContentUris.appendId(builder, start)
            ContentUris.appendId(builder, end)

            val lines = ArrayList<String>(4)
            try {
                val cursor = context.contentResolver.query(
                    builder.build(),
                    arrayOf(CalendarContract.Instances.TITLE, CalendarContract.Instances.BEGIN),
                    null,
                    null,
                    CalendarContract.Instances.BEGIN + " ASC"
                )
                cursor?.use {
                    while (it.moveToNext() && lines.size < 4) {
                        val title = it.getString(0)?.takeIf { value -> value.isNotBlank() } ?: "Untitled event"
                        val begin = it.getLong(1)
                        val time = DateFormat.getTimeInstance(DateFormat.SHORT).format(Date(begin))
                        lines.add("$time  $title")
                    }
                }
            } catch (_: SecurityException) {
                lines.clear()
                lines.add(context.getString(R.string.calendar_permission_required))
            } catch (_: Exception) {
                lines.clear()
                lines.add(context.getString(R.string.calendar_empty))
            }

            if (lines.isEmpty()) lines.add(context.getString(R.string.calendar_empty))
            eventIds.forEachIndexed { index, viewId ->
                views.setTextViewText(viewId, lines.getOrNull(index).orEmpty())
            }
            manager.updateAppWidget(appWidgetId, views)
        }
    }
}
