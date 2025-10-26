package com.neuroscienceanxietylab.doorstask.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "session_log")
data class SessionLog(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val subjectId: String,
    val session: Int,
    val round: Int,
    val subtrial: Int,
    val rewardMagnitude: Int,
    val punishmentMagnitude: Int,
    val distanceAtStart: Float,
    val distanceFromDoor: Float,
    val distanceMax: Float,
    val distanceMin: Float,
    val distanceLock: Boolean,
    val doorActionRT: Float,
    val doorOpened: Boolean,
    val doorOutcome: String?, // "reward", "punishment", or null
    val didWin: Boolean?,
    val totalCoins: Int,
    val timestamp: Long = System.currentTimeMillis()
)