package com.neuroscienceanxietylab.doorstask.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neuroscienceanxietylab.doorstask.R
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorTaskViewModel

@Composable
fun InstructionScreen(viewModel: DoorTaskViewModel = viewModel()) {

    val instructionImages = remember {
        listOf(
            R.drawable.inst_en_1e,
            R.drawable.inst_en_2e,
            R.drawable.inst_en_3e,
            R.drawable.inst_en_4e,
            R.drawable.inst_en_5e,
            R.drawable.inst_en_6e,
            R.drawable.inst_en_7e,
            R.drawable.inst_en_8e,
            R.drawable.inst_en_9e,
            R.drawable.inst_en_10e,
            R.drawable.inst_en_11e,
            R.drawable.inst_en_12e,
            R.drawable.inst_en_13e,
            R.drawable.inst_en_14e,
            R.drawable.inst_en_15e,
            R.drawable.inst_en_16e,
            R.drawable.inst_en_17e,
            R.drawable.inst_en_18e,
            R.drawable.inst_en_19e,
            R.drawable.inst_en_20e,
            R.drawable.inst_en_21e,
            R.drawable.inst_en_22e,
            R.drawable.inst_en_23e,
            R.drawable.inst_en_24e,
            R.drawable.inst_en_25e,
            R.drawable.inst_en_26e,
            R.drawable.inst_en_27e,
            R.drawable.inst_en_practice_start,
            R.drawable.inst_en_simulationrunstart,
            R.drawable.inst_en_simulationrunend,
            R.drawable.inst_en_start_main_game,
            R.drawable.inst_en_end_slide
        )
    }

    var currentInstructionIndex by remember { mutableStateOf(0) }

    Box(modifier = Modifier.fillMaxSize()) {
        Image(
            painter = painterResource(id = instructionImages[currentInstructionIndex]),
            contentDescription = "Instruction Image",
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Fit
        )

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Button(
                onClick = { if (currentInstructionIndex > 0) currentInstructionIndex-- },
                enabled = currentInstructionIndex > 0
            ) {
                Text("Back")
            }

            Button(onClick = {
                if (currentInstructionIndex < instructionImages.size - 1) {
                    currentInstructionIndex++
                } else {
                    viewModel.onInstructionsFinished()
                }
            }) {
                Text(if (currentInstructionIndex < instructionImages.size - 1) "Next" else "Start Task")
            }
        }
    }
}