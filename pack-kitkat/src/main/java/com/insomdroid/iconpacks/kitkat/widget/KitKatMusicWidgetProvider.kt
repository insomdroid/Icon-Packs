package com.insomdroid.iconpacks.kitkat.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.media.session.MediaSessionManager
import android.media.session.PlaybackState
import android.os.Build
import android.widget.RemoteViews
import com.insomdroid.iconpacks.kitkat.R

class KitKatMusicWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        ids.forEach { update(context, manager, it) }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        if (intent.action == ACTION_PLAY || intent.action == ACTION_PAUSE ||
            intent.action == ACTION_NEXT || intent.action == ACTION_PREVIOUS ||
            intent.action == ACTION_REFRESH
        ) {
            sendMediaCommand(context, intent.action ?: ACTION_REFRESH)
            refreshAll(context)
        }
    }

    companion object {
        const val ACTION_PLAY = "com.insomdroid.holokat.music.PLAY"
        const val ACTION_PAUSE = "com.insomdroid.holokat.music.PAUSE"
        const val ACTION_NEXT = "com.insomdroid.holokat.music.NEXT"
        const val ACTION_PREVIOUS = "com.insomdroid.holokat.music.PREVIOUS"
        const val ACTION_REFRESH = "com.insomdroid.holokat.music.REFRESH"

        private fun sendMediaCommand(context: Context, action: String) {
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) return
            try {
                val manager = context.getSystemService(Context.MEDIA_SESSION_SERVICE) as MediaSessionManager
                val component = ComponentName(context, KitKatMusicNotificationListener::class.java)
                val controllers = manager.getActiveSessions(component)
                controllers.forEach { controller ->
                    when (action) {
                        ACTION_PLAY -> controller.transportControls.play()
                        ACTION_PAUSE -> controller.transportControls.pause()
                        ACTION_NEXT -> controller.transportControls.skipToNext()
                        ACTION_PREVIOUS -> controller.transportControls.skipToPrevious()
                    }
                }
            } catch (_: SecurityException) {
                // Android requires notification-listener access for active session control.
            } catch (_: Exception) {
            }
        }

        private fun refreshAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(ComponentName(context, KitKatMusicWidgetProvider::class.java))
            ids.forEach { update(context, manager, it) }
        }

        private fun update(context: Context, manager: AppWidgetManager, id: Int) {
            val views = RemoteViews(context.packageName, R.layout.kitkat_music_widget)
            val component = ComponentName(context, KitKatMusicNotificationListener::class.java)
            var title = "No music playing"
            var artist = "Start playback in your music app"
            var playing = false

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                try {
                    val sessions = (context.getSystemService(Context.MEDIA_SESSION_SERVICE) as MediaSessionManager)
                        .getActiveSessions(component)
                    val state = sessions.firstOrNull()
                    val metadata = state?.metadata
                    title = metadata?.getString(android.media.MediaMetadata.METADATA_KEY_TITLE) ?: title
                    artist = metadata?.getString(android.media.MediaMetadata.METADATA_KEY_ARTIST) ?: artist
                    playing = state?.playbackState?.state == PlaybackState.STATE_PLAYING
                    views.setTextViewText(R.id.music_widget_title, title)
                    views.setTextViewText(R.id.music_widget_artist, artist)
                    val album = metadata?.getBitmap(android.media.MediaMetadata.METADATA_KEY_ALBUM_ART)
                        ?: metadata?.getBitmap(android.media.MediaMetadata.METADATA_KEY_ART)
                    if (album != null) views.setImageViewBitmap(R.id.music_widget_art, album)
                } catch (_: SecurityException) {
                    title = "Notification access required"
                    artist = "Enable HoloKat in system notification access settings"
                } catch (_: Exception) {
                }
            }

            views.setTextViewText(R.id.music_widget_title, title)
            views.setTextViewText(R.id.music_widget_artist, artist)
            attach(context, views, R.id.music_widget_previous, ACTION_PREVIOUS, id * 10 + 1)
            attach(context, views, R.id.music_widget_play, if (playing) ACTION_PAUSE else ACTION_PLAY, id * 10 + 2)
            attach(context, views, R.id.music_widget_next, ACTION_NEXT, id * 10 + 3)
            manager.updateAppWidget(id, views)
        }

        private fun attach(context: Context, views: RemoteViews, viewId: Int, action: String, request: Int) {
            val intent = Intent(context, KitKatMusicWidgetProvider::class.java).setAction(action)
            val pending = PendingIntent.getBroadcast(context, request, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            views.setOnClickPendingIntent(viewId, pending)
        }
    }
}
