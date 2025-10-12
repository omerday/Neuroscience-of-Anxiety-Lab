package com.neuroscienceanxietylab.doorstask.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.neuroscienceanxietylab.doorstask.data.model.EventLog
import com.neuroscienceanxietylab.doorstask.data.model.SessionLog
import com.neuroscienceanxietylab.doorstask.data.model.VASResponse

@Database(entities = [SessionLog::class, EventLog::class, VASResponse::class], version = 1, exportSchema = false)
abstract class DoorsDatabase : RoomDatabase() {

    abstract fun taskDao(): TaskDao

    companion object {
        @Volatile
        private var INSTANCE: DoorsDatabase? = null

        fun getDatabase(context: Context): DoorsDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    DoorsDatabase::class.java,
                    "doors_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}