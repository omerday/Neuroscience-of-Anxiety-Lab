package com.neuroscienceanxietylab.doorstask.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "vas_response")
data class VASResponse(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val subjectId: String,
    val session: Int,
    val taskPhase: String, // e.g., "pre-task", "midway", "post-task"
    val question: String,
    val tag: String, // e.g., "Anxiety", "Happiness"
    val score: Int,
    val responseTime: Long,
    val timestamp: Long = System.currentTimeMillis()
)