package com.neuroscienceanxietylab.doorstask.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Slider
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorTaskViewModel

@Composable
fun VASScreen(viewModel: DoorTaskViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    var sliderValue by remember { mutableStateOf(50f) }

    val currentQuestion = viewModel.vasQuestions[uiState.currentVasQuestionIndex]

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = currentQuestion.question,
            fontSize = 24.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth(0.8f)
        )

        Spacer(modifier = Modifier.height(64.dp))

        Slider(
            value = sliderValue,
            onValueChange = { sliderValue = it },
            valueRange = 0f..100f,
            modifier = Modifier.fillMaxWidth(0.9f)
        )

        Row(
            modifier = Modifier.fillMaxWidth(0.9f),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(text = "Not at all")
            Text(text = "Very much")
        }

        Spacer(modifier = Modifier.height(64.dp))

        Button(onClick = {
            viewModel.onVasResponse(sliderValue.toInt())
        }) {
            Text(text = "Submit", fontSize = 18.sp)
        }
    }
}
