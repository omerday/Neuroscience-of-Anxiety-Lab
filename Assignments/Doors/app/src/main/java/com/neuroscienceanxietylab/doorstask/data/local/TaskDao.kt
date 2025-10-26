package com.neuroscienceanxietylab.doorstask.data.local

import androidx.room.Dao
import androidx.room.Insert
import com.neuroscienceanxietylab.doorstask.data.model.EventLog
import com.neuroscienceanxietylab.doorstask.data.model.SessionLog
import com.neuroscienceanxietylab.doorstask.data.model.VASResponse

@Dao
interface TaskDao {

    @Insert
    suspend fun insertSessionLog(log: SessionLog)

    @Insert
    suspend fun insertEventLog(log: EventLog)

    @Insert
    suspend fun insertVASResponse(response: VASResponse)

}