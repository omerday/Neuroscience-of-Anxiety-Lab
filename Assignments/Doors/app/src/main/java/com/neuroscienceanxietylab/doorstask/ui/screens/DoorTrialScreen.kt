package com.neuroscienceanxietylab.doorstask.ui.screens

import android.content.Context
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neuroscienceanxietylab.doorstask.R
import com.neuroscienceanxietylab.doorstask.util.SoundPlayer
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorOutcome
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorTaskViewModel
import kotlinx.coroutines.delay

@Composable
fun DoorTrialScreen(viewModel: DoorTaskViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current

    val animatedScale by animateFloatAsState(
        targetValue = 1.0f + (uiState.currentDistance / 100f),
        label = "doorScaleAnimation"
    )

    Box(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.TopCenter)
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(text = "Trial: ${uiState.currentTrialIndex + 1}/${uiState.totalTrials}", fontSize = 20.sp)
            Text(text = "Coins: ${uiState.totalCoins}", fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }

        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {

            val doorImage = getDoorImageResource(uiState.currentReward, uiState.currentPunishment)

            Image(
                painter = painterResource(id = doorImage),
                contentDescription = "Door",
                modifier = Modifier
                    .size(300.dp)
                    .graphicsLayer(
                        scaleX = animatedScale,
                        scaleY = animatedScale
                    ),
                contentScale = ContentScale.Fit
            )

            Spacer(modifier = Modifier.height(32.dp))

            GradientSlider(
                value = uiState.currentDistance,
                onValueChange = { viewModel.onDistanceChanged(it) },
                valueRange = 0f..100f,
                modifier = Modifier.fillMaxWidth(0.8f),
                enabled = !uiState.isLockedIn
            )
            Text(text = "Chance to open: ${uiState.currentDistance.toInt()}%")

            Spacer(modifier = Modifier.height(32.dp))

            Button(
                onClick = { viewModel.onLockInPressed() },
                enabled = !uiState.isLockedIn
            ) {
                Text(text = "Lock In", fontSize = 18.sp)
            }
        }

        if (uiState.isLockedIn && uiState.outcome != DoorOutcome.Undetermined) {
            OutcomeOverlay(outcome = uiState.outcome, context = context) {
                viewModel.onNextTrial()
            }
        }
    }
}

@Composable
private fun OutcomeOverlay(outcome: DoorOutcome, context: Context, onNext: () -> Unit) {
    val outcomeImageRes: Int
    val outcomeText: String

    when (outcome) {
        is DoorOutcome.Opened -> {
            if (outcome.didWin) {
                outcomeImageRes = R.drawable.outcome_reward
                outcomeText = "YOU WON!"
                SoundPlayer.playSound(context, R.raw.sound_new_reward)
            } else {
                outcomeImageRes = R.drawable.outcome_punishment
                outcomeText = "YOU LOST..."
                SoundPlayer.playSound(context, R.raw.sound_monster_mp3)
            }
        }
        DoorOutcome.Closed -> {
            outcomeImageRes = R.drawable.d1_lock
            outcomeText = "DOOR DID NOT OPEN"
            SoundPlayer.playSound(context, R.raw.sound_click_1s)
        }
        DoorOutcome.Undetermined -> return
    }

    LaunchedEffect(outcome) {
        delay(2000)
        onNext()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .alpha(0.9f)
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Image(painter = painterResource(id = outcomeImageRes), contentDescription = outcomeText)
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = outcomeText, fontSize = 32.sp, fontWeight = FontWeight.Bold, color = Color.White)
    }
}

@Composable
private fun GradientSlider(
    value: Float,
    onValueChange: (Float) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    valueRange: ClosedFloatingPointRange<Float> = 0f..100f
) {
    Box(modifier = modifier) {
        // Gradient track background - positioned to align with Material3 slider track
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(14.dp)
                .align(Alignment.Center)
                .clip(RoundedCornerShape(7.dp))
                .background(
                    Brush.horizontalGradient(
                        colors = listOf(
                            Color(0xFFE53935), // Red (left)
                            Color(0xFFFF9800), // Orange
                            Color(0xFFFFEB3B), // Yellow
                            Color(0xFF4CAF50)  // Green (right)
                        )
                    )
                )
                .border(1.dp, Color(0xFF424242), RoundedCornerShape(7.dp))
        )
        
        // Material3 Slider with transparent tracks to show gradient background
        Slider(
            value = value,
            onValueChange = onValueChange,
            valueRange = valueRange,
            modifier = Modifier.fillMaxWidth(),
            enabled = enabled,
            colors = SliderDefaults.colors(
                activeTrackColor = Color.Transparent,
                inactiveTrackColor = Color.Transparent,
                thumbColor = Color(0xFFFFFFFF),
                disabledThumbColor = Color(0xFF9E9E9E)
            )
        )
    }
}

@Composable
private fun getDoorImageResource(reward: Int, punishment: Int): Int {
    val context = LocalContext.current
    val resourceName = "d1_p${punishment}r${reward}"
    val resourceId = context.resources.getIdentifier(resourceName, "drawable", context.packageName)
    return if (resourceId != 0) resourceId else R.drawable.d1_p0r0 // Fallback image
}
