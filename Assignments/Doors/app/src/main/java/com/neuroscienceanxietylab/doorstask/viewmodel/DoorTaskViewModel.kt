package com.neuroscienceanxietylab.doorstask.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.random.Random

private const val TRIAL_TIMEOUT_MS = 10000L
private const val NUM_TRIALS_PER_BLOCK = 5 // For demo; original is 49. Let's do 2 blocks.

enum class TaskPhase {
    INSTRUCTIONS,
    TRIAL,
    VAS,
    SUMMARY
}

// Sealed class to represent the various outcomes of a door trial
sealed class DoorOutcome {
    data class Opened(val didWin: Boolean) : DoorOutcome()
    object Closed : DoorOutcome()
    object Undetermined : DoorOutcome()
}

// Represents the state of the entire task UI
data class TaskUiState(
    val phase: TaskPhase = TaskPhase.INSTRUCTIONS,
    val totalCoins: Int = 0,
    val currentTrialIndex: Int = 0,
    val totalTrials: Int = NUM_TRIALS_PER_BLOCK * 2,
    val currentReward: Int = 0,
    val currentPunishment: Int = 0,
    val currentDistance: Float = 50f, // Start at 50%
    val isLockedIn: Boolean = false,
    val outcome: DoorOutcome = DoorOutcome.Undetermined
)

class DoorTaskViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(TaskUiState())
    val uiState: StateFlow<TaskUiState> = _uiState.asStateFlow()

    private var trialList: List<Pair<Int, Int>> = emptyList()
    private var autoLockJob: Job? = null

    init {
        setupTrials()
    }

    private fun setupTrials() {
        val scenarios = mutableListOf<Pair<Int, Int>>().apply {
            for (r in 1..7) {
                for (p in 1..7) {
                    add(Pair(r, p))
                }
            }
        }
        trialList = (scenarios.shuffled() + scenarios.shuffled()).take(NUM_TRIALS_PER_BLOCK * 2)
    }

    private fun loadCurrentTrial() {
        val trial = trialList[_uiState.value.currentTrialIndex]
        _uiState.update {
            it.copy(
                phase = TaskPhase.TRIAL,
                currentReward = trial.first,
                currentPunishment = trial.second,
                isLockedIn = false,
                outcome = DoorOutcome.Undetermined,
                currentDistance = 50f
            )
        }
        startAutoLockTimer()
    }

    private fun startAutoLockTimer() {
        autoLockJob?.cancel()
        autoLockJob = viewModelScope.launch {
            delay(TRIAL_TIMEOUT_MS)
            if (!_uiState.value.isLockedIn) {
                onLockInPressed()
            }
        }
    }

    fun onInstructionsFinished() {
        loadCurrentTrial()
    }

    fun onDistanceChanged(newDistance: Float) {
        if (!_uiState.value.isLockedIn) {
            _uiState.update { it.copy(currentDistance = newDistance) }
        }
    }

    fun onLockInPressed() {
        if (_uiState.value.isLockedIn) return
        autoLockJob?.cancel()

        viewModelScope.launch {
            _uiState.update { it.copy(isLockedIn = true) }
            delay(3000)

            val distance = _uiState.value.currentDistance
            val doorOpens = Random.nextFloat() * 100 <= distance

            if (doorOpens) {
                val didWin = Random.nextBoolean()
                val coinsChange = if (didWin) _uiState.value.currentReward else -_uiState.value.currentPunishment
                _uiState.update {
                    it.copy(
                        outcome = DoorOutcome.Opened(didWin),
                        totalCoins = it.totalCoins + coinsChange
                    )
                }
            } else {
                _uiState.update { it.copy(outcome = DoorOutcome.Closed) }
            }
        }
    }

    fun onNextTrial() {
        val nextTrialIndex = _uiState.value.currentTrialIndex + 1

        // Time for VAS screen in the middle
        if (nextTrialIndex == NUM_TRIALS_PER_BLOCK) {
            _uiState.update { it.copy(phase = TaskPhase.VAS, currentTrialIndex = nextTrialIndex) }
            return
        }

        // Time for Summary screen at the end
        if (nextTrialIndex >= uiState.value.totalTrials) {
            _uiState.update { it.copy(phase = TaskPhase.SUMMARY) }
            return
        }

        // Otherwise, load the next trial
        _uiState.update { it.copy(currentTrialIndex = nextTrialIndex) }
        loadCurrentTrial()
    }

    fun onVasResponse(score: Int) {
        // TODO: Save VAS response to database
        println("VAS Score: $score")

        // After VAS, continue to next trial block
        loadCurrentTrial()
    }
}