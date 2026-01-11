package com.neuroscienceanxietylab.doorstask.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun OpeningScreen(
    onRunTaskClick: () -> Unit,
    onRepeatInstructionsClick: () -> Unit,
    onLogoutClick: () -> Unit
) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Doors Task",
            style = MaterialTheme.typography.headlineLarge
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Neuroscience of Anxiety Lab",
            style = MaterialTheme.typography.bodyMedium
        )

        Spacer(modifier = Modifier.height(40.dp))

        // Main option: run task without instructions
        Button(onClick = onRunTaskClick) {
            Text(text = "Run task without instructions")
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Secondary option: repeat instructions then run
        OutlinedButton(onClick = onRepeatInstructionsClick) {
            Text(text = "Repeat instructions and run the app")
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Logout option
        OutlinedButton(onClick = onLogoutClick) {
            Text(text = "Logout")
        }
    }
}

