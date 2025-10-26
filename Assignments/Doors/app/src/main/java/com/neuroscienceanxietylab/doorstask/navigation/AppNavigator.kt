package com.neuroscienceanxietylab.doorstask.navigation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.CircularProgressIndicator
impofrt androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.neuroscienceanxietylab.doorstask.ui.screens.*
import com.neuroscienceanxietylab.doorstask.viewmodel.AuthViewModel
import com.neuroscienceanxietylab.doorstask.viewmodel.AuthState
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorTaskViewModel
import com.neuroscienceanxietylab.doorstask.viewmodel.TaskPhase

object AuthRoutes {
    const val LOGIN = "login" // blah blah
    const val REGISTER = "register"
}

@Composable
fun AppNavigator(
    authViewModel: AuthViewModel = viewModel(),
    doorTaskViewModel: DoorTaskViewModel = viewModel()
) {
    val authState by authViewModel.authState.collectAsState()
    val taskState by doorTaskViewModel.uiState.collectAsState()

    // This effect will run whenever the authState changes.
    LaunchedEffect(authState) {
        if (authState is AuthState.Authenticated) {
            // Once authenticated, trigger the remote config load.
            doorTaskViewModel.loadRemoteConfig()
        }
    }

    when (authState) {
        is AuthState.Authenticated -> {
            // Once authenticated, show the main task flow based on its phase
            when (taskState.phase) {
                TaskPhase.LOADING -> {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                TaskPhase.INSTRUCTIONS -> InstructionScreen(doorTaskViewModel)
                TaskPhase.TRIAL -> DoorTrialScreen(doorTaskViewModel)
                TaskPhase.VAS_PRE, TaskPhase.VAS_MID, TaskPhase.VAS_POST -> VASScreen(doorTaskViewModel)
                TaskPhase.SUMMARY -> SummaryScreen(doorTaskViewModel)
            }
        }
        is AuthState.Loading -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        else -> {
            // If not authenticated, show the login/register flow
            val navController = rememberNavController()
            NavHost(navController = navController, startDestination = AuthRoutes.LOGIN) {
                composable(AuthRoutes.LOGIN) {
                    LoginScreen(
                        onLoginClick = { email, password -> authViewModel.login(email, password) },
                        onNavigateToRegister = { navController.navigate(AuthRoutes.REGISTER) }
                    )
                }
                composable(AuthRoutes.REGISTER) {
                    RegistrationScreen(
                        onRegisterClick = { email, password -> authViewModel.signUp(email, password) },
                        onNavigateToLogin = { navController.popBackStack() }
                    )
                }
            }
        }
    }
}