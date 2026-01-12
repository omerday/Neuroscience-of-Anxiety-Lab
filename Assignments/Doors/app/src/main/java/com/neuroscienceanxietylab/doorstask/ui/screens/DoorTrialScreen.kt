package com.neuroscienceanxietylab.doorstask.ui.screens

import android.content.Context
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.zIndex
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onPlaced
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.layout.positionInParent
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.platform.LocalDensity
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

        Box(
            modifier = Modifier.fillMaxSize()
        ) {
            var imageTop by remember { mutableStateOf(0f) }
            
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
                        .onPlaced { coordinates ->
                            imageTop = coordinates.positionInParent().y
                        }
                        .graphicsLayer(
                            scaleX = animatedScale,
                            scaleY = animatedScale
                        ),
                    contentScale = ContentScale.Fit
                )

                Spacer(modifier = Modifier.height(32.dp))

                Text(text = "Chance to open: ${uiState.currentDistance.toInt()}%")

                Spacer(modifier = Modifier.height(32.dp))

                Button(
                    onClick = { viewModel.onLockInPressed() },
                    enabled = !uiState.isLockedIn
                ) {
                    Text(text = "Lock In", fontSize = 18.sp)
                }
            }

            // Slider positioned absolutely to align with image top and bottom
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .offset { IntOffset(0, imageTop.toInt()) }
                    .zIndex(1f),
                horizontalArrangement = Arrangement.End
            ) {
                VerticalGradientSlider(
                    value = uiState.currentDistance,
                    onValueChange = { viewModel.onDistanceChanged(it) },
                    valueRange = 0f..100f,
                    enabled = !uiState.isLockedIn,
                    modifier = Modifier
                        .height(300.dp)
                        .padding(end = 24.dp)
                )
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
    }
}

@Composable
fun VerticalGradientSlider(
    value: Float,
    onValueChange: (Float) -> Unit,
    valueRange: ClosedFloatingPointRange<Float>,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    trackWidth: Dp = 14.dp,
    thumbRadius: Dp = 10.dp
) {
    val range = valueRange.endInclusive - valueRange.start
    var sliderHeightPx by remember { mutableStateOf(1f) }
    val density = LocalDensity.current
    val thumbRadiusPx = with(density) { thumbRadius.toPx() }

    Box(
        modifier = modifier
            .width(40.dp)
            .fillMaxHeight()
    ) {
        Box(
            modifier = Modifier
                .width(trackWidth)
                .fillMaxHeight()
                .align(Alignment.TopStart)
                .clip(RoundedCornerShape(trackWidth / 2))
                .background(
                    Brush.verticalGradient(
                        colors = listOf(
                            Color(0xFF4CAF50),
                            Color(0xFFFFEB3B),
                            Color(0xFFFF9800),
                            Color(0xFFE53935)
                        )
                    )
                )
                .onSizeChanged { sliderHeightPx = it.height.toFloat() }
                .pointerInput(enabled, sliderHeightPx, thumbRadiusPx) {
                    if (!enabled || sliderHeightPx <= 0) return@pointerInput
                    // Calculate the valid range for thumb center (accounting for thumb radius)
                    // Position is relative to the track's top (y=0 is top of track)
                    val minY = thumbRadiusPx
                    val maxY = sliderHeightPx - thumbRadiusPx
                    val trackRange = maxY - minY
                    
                    detectVerticalDragGestures { change, _ ->
                        val y = change.position.y  // y is relative to the track's top
                        // Clamp to valid thumb center range
                        val clampedY = y.coerceIn(minY, maxY)
                        // Map from thumb center position to value (inverted: top = max, bottom = min)
                        val percent = 1f - ((clampedY - minY) / trackRange)
                        val newValue =
                            (valueRange.start + percent * range).coerceIn(valueRange.start, valueRange.endInclusive)
                        onValueChange(newValue)
                    }
                }
        )

        // Thumb - positioned relative to the track's coordinate system
        // The track starts at the top of the parent Box (after padding)
        // Calculate thumb center position, accounting for thumb radius bounds
        val minY = thumbRadiusPx
        val maxY = sliderHeightPx - thumbRadiusPx
        val trackRange = maxY - minY
        val percent = (value - valueRange.start) / range
        val thumbCenterY = if (trackRange > 0) {
            maxY - (percent * trackRange)
        } else {
            sliderHeightPx / 2f
        }

        Box(
            modifier = Modifier
                .align(Alignment.TopStart)
                .offset { 
                    val xOffset = with(density) { (trackWidth / 2 - thumbRadius).toPx().toInt() }
                    IntOffset(xOffset, (thumbCenterY - thumbRadiusPx).toInt()) 
                }
                .size(thumbRadius * 2)
                .clip(RoundedCornerShape(50))
                .background(Color.White)
                .border(1.dp, Color(0xFF424242), RoundedCornerShape(50))
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
