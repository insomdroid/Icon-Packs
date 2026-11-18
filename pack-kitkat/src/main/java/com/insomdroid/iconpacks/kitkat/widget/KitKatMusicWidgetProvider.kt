package com.insomdroid.iconpacks.kitkat.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.media.MediaMetadata
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
        if (
            intent.action == ACTION_PLAY ||
            intent.action == ACTION_PAUSE ||
            intent.action == ACTION_NEXT ||
            intent.action == ACTION_PREVIOUS ||
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
                manager.getActiveSessions(component).forEach { controller ->
                    when (action) {
                        ACTION_PLAY -> controller.transportControls.play()
                        ACTION_PAUSE -> controller.transportControls.pause()
                        ACTION_NEXT -> controller.transportControls.skipToNext()
                        ACTION_PREVIOUS -> controller.transportControls.skipToPrevious()
                    }
                }
            } catch (_: SecurityException) {
                // Notification-listener access is required by Android for media session control.
            } catch (_: Exception) {
            }
        }

        private fun refreshAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(
                ComponentName(context, KitKatMusicWidgetProvider::class.java)
            )
            ids.forEach { update(context, manager, it) }
        }

        private fun update(context: Context, manager: AppWidgetManager, id: Int) {
            val views = RemoteViews(context.packageName, R.layout.kitkat_music_widget)
            val listener = ComponentName(context, KitKatMusicNotificationListener::class.java)
            var title = "No music playing"
            var artist = "Start playback in Google Play Music"
            var playing = false
            var albumArt: android.graphics.Bitmap? = null

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                try {
                    val session = (context.getSystemService(Context.MEDIA_SESSION_SERVICE) as MediaSessionManager)
                        .getActiveSessions(listener)
                        .firstOrNull()
                    val metadata = session?.metadata
                    title = metadata?.getString(MediaMetadata.METADATA_KEY_TITLE)
                        ?.takeIf { it.isNotBlank() } ?: title
                    artist = metadata?.getString(MediaMetadata.METADATA_KEY_ARTIST)
                        ?.takeIf { it.isNotBlank() } ?: artist
                    albumArt = metadata?.getBitmap(MediaMetadata.METADATA_KEY_ALBUM_ART)
                        ?: metadata?.getBitmap(MediaMetadata.METADATA_KEY_ART)
                    playing = session?.playbackState?.state == PlaybackState.STATE_PLAYING
                } catch (_: SecurityException) {
                    title = "Notification access required"
                    artist = "Enable HoloKat in notification access settings"
                } catch (_: Exception) {
                }
            }

            views.setImageViewResource(R.id.music_widget_art, R.drawable.kitkat_music_unknown)
            if (albumArt != null) {
                views.setImageViewBitmap(R.id.music_widget_art, albumArt)
            }
            views.setTextViewText(R.id.music_widget_title, title)
            views.setTextViewText(R.id.music_widget_artist, artist)
            views.setImageViewResource(
                R.id.music_widget_play,
                if (playing) R.drawable.kitkat_music_pause else R.drawable.kitkat_music_play
            )

            attach(context, views, R.id.music_widget_previous, ACTION_PREVIOUS, id * 10 + 1)
            attach(context, views, R.id.music_widget_play, if (playing) ACTION_PAUSE else ACTION_PLAY, id * 10 + 2)
            attach(context, views, R.id.music_widget_next, ACTION_NEXT, id * 10 + 3)

            val openMusic = context.packageManager.getLaunchIntentForPackage("com.google.android.music")
                ?: Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_APP_MUSIC)
            openMusic.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            val openPending = PendingIntent.getActivity(
                context,
                id * 10 + 4,
                openMusic,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.music_widget_art, openPending)
            views.setOnClickPendingIntent(R.id.music_widget_text, openPending)
            manager.updateAppWidget(id, views)
        }

        private fun attach(
            context: Context,
            views: RemoteViews,
            viewId: Int,
            action: String,
            request: Int
        ) {
            val intent = Intent(context, KitKatMusicWidgetProvider::class.java).setAction(action)
            val pending = PendingIntent.getBroadcast(
                context,
                request,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(viewId, pending)
        }
    }
}
