package com.neuroscienceanxietylab.doorstask.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "vas_response")
data class VASResponse(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val subjectId: String,
    val session: Int,
    val round: Int, // e.g., Beginning, Middle, End
    val questionNumber: Int,
    val vasType: String,
    val score: Int,
    val responseTime: Long,
    val timestamp: Long = System.currentTimeMillis()
)