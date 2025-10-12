package com.neuroscienceanxietylab.doorstask.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.google.firebase.auth.ktx.auth
import com.google.firebase.firestore.ktx.firestore
import com.google.firebase.ktx.Firebase
import com.neuroscienceanxietylab.doorstask.data.local.DoorsDatabase
import com.neuroscienceanxietylab.doorstask.data.local.TaskDao
import com.neuroscienceanxietylab.doorstask.data.model.SessionLog
import com.neuroscienceanxietylab.doorstask.data.model.VASResponse
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.random.Random

data class VasQuestion(val question: String, val tag: String)

enum class TaskPhase {
    LOADING,
    INSTRUCTIONS,
    TRIAL,
    VAS_PRE,
    VAS_MID,
    VAS_POST,
    SUMMARY
}

sealed class DoorOutcome {
    data class Opened(val didWin: Boolean) : DoorOutcome()
    object Closed : DoorOutcome()
    object Undetermined : DoorOutcome()
}

data class TaskUiState(
    val phase: TaskPhase = TaskPhase.LOADING,
    val totalCoins: Int = 0,
    val currentTrialIndex: Int = 0,
    val totalTrials: Int = 0,
    val currentReward: Int = 0,
    val currentPunishment: Int = 0,
    val currentDistance: Float = 50f,
    val isLockedIn: Boolean = false,
    val outcome: DoorOutcome = DoorOutcome.Undetermined,
    val currentVasQuestionIndex: Int = 0
)

class DoorTaskViewModel(application: Application) : AndroidViewModel(application) {

    private val _uiState = MutableStateFlow(TaskUiState())
    val uiState: StateFlow<TaskUiState> = _uiState.asStateFlow()

    private val taskDao: TaskDao
    private val firestore = Firebase.firestore
    private val auth = Firebase.auth

    private var trialList: List<Pair<Int, Int>> = emptyList()
    private var autoLockJob: Job? = null
    private var trialStartTime: Long = 0L

    // In-memory lists for aggregation
    private val sessionLogsInMemory = mutableListOf<SessionLog>()
    private val vasResponsesInMemory = mutableListOf<VASResponse>()

    private var trialsPerBlock: Int = 25
    private var totalBlocks: Int = 2
    private var trialTimeoutMs: Long = 10000L

    val vasQuestions = listOf(
        VasQuestion("How anxious do you feel right now?", "Anxiety"),
        VasQuestion("How happy do you feel right now?", "Happiness")
    )

    init {
        taskDao = DoorsDatabase.getDatabase(application).taskDao()
    }

    fun loadRemoteConfig() {
        val userId = auth.currentUser?.uid ?: return
        firestore.collection("users").document(userId).get()
            .addOnSuccessListener { document ->
                if (document != null && document.exists()) {
                    trialsPerBlock = (document.getLong("trialsPerBlock") ?: 25).toInt()
                    totalBlocks = (document.getLong("totalBlocks") ?: 2).toInt()
                    trialTimeoutMs = document.getLong("trialTimeoutMs") ?: 10000L
                }
                setupTrials()
                _uiState.update { it.copy(phase = TaskPhase.INSTRUCTIONS, totalTrials = trialList.size) }
            }
            .addOnFailureListener {
                setupTrials()
                _uiState.update { it.copy(phase = TaskPhase.INSTRUCTIONS, totalTrials = trialList.size) }
            }
    }

    private fun setupTrials() {
        val scenarios = mutableListOf<Pair<Int, Int>>().apply {
            for (r in 1..7) { for (p in 1..7) { add(Pair(r, p)) } }
        }
        var fullTrialList = mutableListOf<Pair<Int, Int>>()
        for (i in 1..totalBlocks) { fullTrialList.addAll(scenarios.shuffled()) }
        trialList = fullTrialList.take(trialsPerBlock * totalBlocks)
    }

    private fun loadCurrentTrial() {
        val trial = trialList[_uiState.value.currentTrialIndex]
        trialStartTime = System.currentTimeMillis()
        _uiState.update { it.copy(phase = TaskPhase.TRIAL, currentReward = trial.first, currentPunishment = trial.second, isLockedIn = false, outcome = DoorOutcome.Undetermined, currentDistance = 50f) }
        startAutoLockTimer()
    }

    private fun startAutoLockTimer() {
        autoLockJob?.cancel()
        autoLockJob = viewModelScope.launch {
            delay(trialTimeoutMs)
            if (!_uiState.value.isLockedIn) { onLockInPressed(isAutoLocked = true) }
        }
    }

    fun onInstructionsFinished() { _uiState.update { it.copy(phase = TaskPhase.VAS_PRE) } }

    fun onDistanceChanged(newDistance: Float) { if (!_uiState.value.isLockedIn) { _uiState.update { it.copy(currentDistance = newDistance) } } }

    fun onLockInPressed(isAutoLocked: Boolean = false) {
        if (_uiState.value.isLockedIn) return
        autoLockJob?.cancel()
        val reactionTime = if (isAutoLocked) trialTimeoutMs else System.currentTimeMillis() - trialStartTime

        viewModelScope.launch {
            _uiState.update { it.copy(isLockedIn = true) }
            delay(3000)

            val distance = _uiState.value.currentDistance
            val doorOpens = Random.nextFloat() * 100 <= distance
            var didWin: Boolean? = null

            if (doorOpens) {
                didWin = Random.nextBoolean()
                val coinsChange = if (didWin) _uiState.value.currentReward else -_uiState.value.currentPunishment
                _uiState.update { it.copy(totalCoins = it.totalCoins + coinsChange, outcome = DoorOutcome.Opened(didWin)) }
            } else {
                _uiState.update { it.copy(outcome = DoorOutcome.Closed) }
            }

            val log = SessionLog(subjectId = auth.currentUser?.uid ?: "UNKNOWN", session = 1, round = (_uiState.value.currentTrialIndex / trialsPerBlock) + 1, subtrial = _uiState.value.currentTrialIndex, rewardMagnitude = _uiState.value.currentReward, punishmentMagnitude = _uiState.value.currentPunishment, distanceAtStart = 50f, distanceFromDoor = distance, distanceMax = 0f, distanceMin = 0f, distanceLock = true, doorActionRT = reactionTime.toFloat(), doorOpened = doorOpens, doorOutcome = if(doorOpens) if(didWin == true) "reward" else "punishment" else "closed", didWin = didWin, totalCoins = _uiState.value.totalCoins)
            
            // Save to local DB for robustness
            taskDao.insertSessionLog(log)
            // Add to in-memory list for final aggregation
            sessionLogsInMemory.add(log)
        }
    }

    fun onNextTrial() {
        val nextTrialIndex = _uiState.value.currentTrialIndex + 1
        if (nextTrialIndex % trialsPerBlock == 0 && nextTrialIndex < trialList.size) {
            _uiState.update { it.copy(phase = TaskPhase.VAS_MID, currentTrialIndex = nextTrialIndex, currentVasQuestionIndex = 0) }
            return
        }
        if (nextTrialIndex >= trialList.size) {
            saveAggregatedDataToFirestore()
            _uiState.update { it.copy(phase = TaskPhase.VAS_POST, currentVasQuestionIndex = 0) }
            return
        }
        _uiState.update { it.copy(currentTrialIndex = nextTrialIndex) }
        loadCurrentTrial()
    }

    fun onVasResponse(score: Int) {
        viewModelScope.launch {
            val currentState = _uiState.value
            val question = vasQuestions[currentState.currentVasQuestionIndex]
            val response = VASResponse(subjectId = auth.currentUser?.uid ?: "UNKNOWN", session = 1, taskPhase = currentState.phase.name, question = question.question, tag = question.tag, score = score, responseTime = 0L)
            
            // Save to local DB for robustness
            taskDao.insertVASResponse(response)
            // Add to in-memory list for final aggregation
            vasResponsesInMemory.add(response)

            val nextVasIndex = currentState.currentVasQuestionIndex + 1
            if (nextVasIndex < vasQuestions.size) {
                _uiState.update { it.copy(currentVasQuestionIndex = nextVasIndex) }
            } else {
                when (currentState.phase) {
                    TaskPhase.VAS_PRE -> loadCurrentTrial()
                    TaskPhase.VAS_MID -> loadCurrentTrial()
                    TaskPhase.VAS_POST -> _uiState.update { it.copy(phase = TaskPhase.SUMMARY) }
                    else -> {}
                }
            }
        }
    }

    private fun saveAggregatedDataToFirestore() {
        val userId = auth.currentUser?.uid ?: return

        val sessionDocument = hashMapOf(
            "userId" to userId,
            "subjectId" to "sub_${userId.take(6)}",
            "sessionTimestamp" to System.currentTimeMillis(),
            "finalCoinTotal" to _uiState.value.totalCoins,
            "behavioral_data" to sessionLogsInMemory,
            "vas_responses" to vasResponsesInMemory
        )

        firestore.collection("completed_sessions").add(sessionDocument)
            .addOnSuccessListener { 
                println("Aggregated session data saved successfully.")
                sessionLogsInMemory.clear()
                vasResponsesInMemory.clear()
             }
            .addOnFailureListener { e -> println("Error saving aggregated session data: $e") }
    }
}