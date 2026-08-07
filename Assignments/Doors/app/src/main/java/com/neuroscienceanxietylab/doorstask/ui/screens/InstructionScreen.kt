package com.neuroscienceanxietylab.doorstask.ui.screens

import android.graphics.Color as AndroidColor
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neuroscienceanxietylab.doorstask.data.model.InstructionFontFamily
import com.neuroscienceanxietylab.doorstask.data.model.InstructionImageAlignment
import com.neuroscienceanxietylab.doorstask.data.model.InstructionTextAlign
import com.neuroscienceanxietylab.doorstask.viewmodel.DoorTaskViewModel

@Composable
fun InstructionScreen(viewModel: DoorTaskViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    val pages = uiState.instructionPages
    val currentInstructionIndex = uiState.currentInstructionPageIndex

    if (pages.isEmpty()) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "Loading instructions...",
                style = MaterialTheme.typography.bodyLarge
            )
        }
        return
    }
    val currentPage = pages[currentInstructionIndex.coerceIn(0, pages.lastIndex)]
    val screenBackgroundColor = parseColorHex(currentPage.screenBackgroundColorHex, fallback = Color(0xFF101A2A))
    val titleColor = parseColorHex(currentPage.titleColorHex, fallback = Color.White)
    val bodyColor = parseColorHex(currentPage.bodyColorHex, fallback = Color(0xFFF2F4F8))
    val backButtonColor = parseColorHex(currentPage.backButtonColorHex, fallback = Color(0xFF2E5B8C))
    val nextButtonColor = parseColorHex(currentPage.nextButtonColorHex, fallback = Color(0xFF1C8E57))
    val buttonTextColor = parseColorHex(currentPage.buttonTextColorHex, fallback = Color.White)

    Box(modifier = Modifier.fillMaxSize()) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(screenBackgroundColor)
        )

        if (currentPage.slideImageRes != null) {
            Image(
                painter = painterResource(id = currentPage.slideImageRes),
                contentDescription = null,
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Fit
            )

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .align(Alignment.BottomCenter)
                    .padding(horizontal = 24.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Button(
                    onClick = viewModel::onInstructionBack,
                    enabled = currentInstructionIndex > 0,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = backButtonColor,
                        contentColor = buttonTextColor
                    )
                ) {
                    Text("Back")
                }

                Button(
                    onClick = viewModel::onInstructionNext,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = nextButtonColor,
                        contentColor = buttonTextColor
                    )
                ) {
                    Text(if (currentInstructionIndex < pages.lastIndex) "Next" else "Start Task")
                }
            }
        } else {
            currentPage.backgroundImageRes?.let { imageRes ->
                Image(
                    painter = painterResource(id = imageRes),
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.25f))
                )
            }

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp, vertical = 16.dp)
            ) {
                Spacer(modifier = Modifier.weight(0.08f))
                Text(
                    text = currentPage.title,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(0.15f),
                    fontSize = currentPage.titleFontSizeSp.sp,
                    fontFamily = toFontFamily(currentPage.fontFamily),
                    textAlign = toTextAlign(currentPage.textAlign),
                    color = titleColor
                )
                Text(
                    text = currentPage.body,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(0.45f),
                    fontSize = currentPage.bodyFontSizeSp.sp,
                    lineHeight = (currentPage.bodyFontSizeSp * 1.25f).sp,
                    fontFamily = toFontFamily(currentPage.fontFamily),
                    textAlign = toTextAlign(currentPage.textAlign),
                    color = bodyColor
                )

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(0.25f)
                ) {
                    currentPage.foregroundImageRes?.let { imageRes ->
                        Image(
                            painter = painterResource(id = imageRes),
                            contentDescription = "Instruction foreground",
                            modifier = Modifier
                                .fillMaxWidth(0.6f)
                                .fillMaxHeight(0.95f)
                                .align(toComposeAlignment(currentPage.foregroundImageAlignment)),
                            contentScale = ContentScale.Fit
                        )
                    }
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(0.07f),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Button(
                        onClick = viewModel::onInstructionBack,
                        enabled = currentInstructionIndex > 0,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = backButtonColor,
                            contentColor = buttonTextColor
                        )
                    ) {
                        Text("Back")
                    }

                    Button(
                        onClick = viewModel::onInstructionNext,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = nextButtonColor,
                            contentColor = buttonTextColor
                        )
                    ) {
                        Text(if (currentInstructionIndex < pages.lastIndex) "Next" else "Start Task")
                    }
                }
            }
        }
    }
}

private fun toFontFamily(fontFamily: InstructionFontFamily): FontFamily {
    return when (fontFamily) {
        InstructionFontFamily.DEFAULT -> FontFamily.Default
        InstructionFontFamily.SERIF -> FontFamily.Serif
        InstructionFontFamily.MONOSPACE -> FontFamily.Monospace
    }
}

private fun toTextAlign(textAlign: InstructionTextAlign): TextAlign {
    return when (textAlign) {
        InstructionTextAlign.START -> TextAlign.Start
        InstructionTextAlign.CENTER -> TextAlign.Center
        InstructionTextAlign.END -> TextAlign.End
    }
}

private fun toComposeAlignment(alignment: InstructionImageAlignment): Alignment {
    return when (alignment) {
        InstructionImageAlignment.TOP_START -> Alignment.TopStart
        InstructionImageAlignment.TOP_CENTER -> Alignment.TopCenter
        InstructionImageAlignment.TOP_END -> Alignment.TopEnd
        InstructionImageAlignment.CENTER -> Alignment.Center
        InstructionImageAlignment.BOTTOM_START -> Alignment.BottomStart
        InstructionImageAlignment.BOTTOM_CENTER -> Alignment.BottomCenter
        InstructionImageAlignment.BOTTOM_END -> Alignment.BottomEnd
    }
}

private fun parseColorHex(hex: String, fallback: Color): Color {
    return try {
        Color(AndroidColor.parseColor(hex))
    } catch (_: IllegalArgumentException) {
        fallback
    }
}
