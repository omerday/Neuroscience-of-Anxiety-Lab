package com.neuroscienceanxietylab.doorstask.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import androidx.room.Index

@Entity(
    tableName = "event_log",
    foreignKeys = [
        ForeignKey(
            entity = SessionLog::class,
            parentColumns = ["id"],
            childColumns = ["sessionId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index(value = ["sessionId"])]
)
data class EventLog(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val sessionId: Int,
    val subtrial: Int,
    val currentDistance: Float,
    val eventTime: Long // Relative to trial start
)