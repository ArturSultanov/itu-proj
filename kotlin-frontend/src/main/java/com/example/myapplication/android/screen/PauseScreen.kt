package com.example.myapplication.android.screen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.myapplication.android.Buttons
import com.example.myapplication.android.api.GameApi

data object PauseScreen : AppScreen("pause") {
    @Composable
    override fun Header(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Text(
            "Pause",
            style = MaterialTheme.typography.titleLarge
        )
    }

    @Composable
    override fun Body(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        var showResetDialog by remember { mutableStateOf(false) }

        Buttons.ResumeButton()
        Buttons.ResetPlaygroundButton()
        Buttons.SettingsButton()

        // Reset confirmation dialog
        if (showResetDialog) {
            Dialog(onDismissRequest = { showResetDialog = false }) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    shadowElevation = 8.dp,
                ) {
                    Column(
                        modifier = Modifier
                            .padding(16.dp)
                            .fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Are you sure you want to reset the game?",
                            style = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold),
                            textAlign = TextAlign.Center
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly
                        ) {
                            // Cancel button
                            Button(onClick = { showResetDialog = false }) {
                                Text("Cancel")
                            }

                            // Confirm reset button
                            Button(onClick = {
                                GameApi.new() // Reset the game
                                showResetDialog = false
                                navController?.navigate(PlaygroundScreen.route)
                            }) {
                                Text("Reset")
                            }
                        }
                    }
                }
            }
        }

    }

    @Composable
    override fun Footer(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Buttons.QuitGameButton()
    }
}
