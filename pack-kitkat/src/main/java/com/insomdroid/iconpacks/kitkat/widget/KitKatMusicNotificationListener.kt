package com.insomdroid.iconpacks.kitkat.widget

import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.content.Intent

class KitKatMusicNotificationListener : NotificationListenerService() {
    override fun onListenerConnected() {
        super.onListenerConnected()
        sendBroadcast(Intent(KitKatMusicWidgetProvider.ACTION_REFRESH).setClass(this, KitKatMusicWidgetProvider::class.java))
    }

    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        sendBroadcast(Intent(KitKatMusicWidgetProvider.ACTION_REFRESH).setClass(this, KitKatMusicWidgetProvider::class.java))
    }

    override fun onNotificationRemoved(sbn: StatusBarNotification?) {
        sendBroadcast(Intent(KitKatMusicWidgetProvider.ACTION_REFRESH).setClass(this, KitKatMusicWidgetProvider::class.java))
    }
}
