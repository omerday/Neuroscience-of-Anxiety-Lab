package com.neuroscienceanxietylab.doorstask.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.neuroscienceanxietylab.doorstask.ui.screens.DoorTrialScreen
import com.neuroscienceanxietylab.doorstask.ui.screens.InstructionScreen
import com.neuroscienceanxietylab.doorstask.ui.screens.SummaryScreen
import com.neuroscienceanxietylab.doorstask.ui.screens.VASScreen
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorTaskViewModel
import com.neuroscienceanxietylab.doorstask.viewmodel.TaskPhase

@Composable
fun AppNavigator(viewModel: DoorTaskViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    when (uiState.phase) {
        TaskPhase.INSTRUCTIONS -> InstructionScreen(viewModel)
        TaskPhase.TRIAL -> DoorTrialScreen(viewModel)
        TaskPhase.VAS -> VASScreen(viewModel)
        TaskPhase.SUMMARY -> SummaryScreen(viewModel)
    }
}