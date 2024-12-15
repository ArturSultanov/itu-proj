package com.example.myapplication.android

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.myapplication.android.api.ApiException
import com.example.myapplication.android.api.GameApi
import com.example.myapplication.android.screen.LeaderBoardScreen
import com.example.myapplication.android.screen.LoginScreen
import com.example.myapplication.android.screen.PauseScreen
import com.example.myapplication.android.screen.PlaygroundScreen
import com.example.myapplication.android.screen.SettingsScreen
import com.example.myapplication.android.screen.UserProfile

class Buttons {

    companion object {

        private val padding = 8.dp
        private val width = 200.dp


        @Composable
        fun BackButton() {
            var clicked by remember { mutableStateOf(false) }
            Button(
                onClick = {
                    clicked = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width)
            ) {
                Text("Back")
            }

            LaunchedEffect(clicked) {
                if (clicked) {
                    NavigationGraph.navigateBack()
                    clicked = false
                }
            }
        }

        @Composable
        fun SettingsButton() {
            var clicked by remember { mutableStateOf(false) }
            Button(
                onClick = {
                    clicked = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width)
            ) {
                Text("Settings")
            }

            LaunchedEffect(clicked) {
                if (clicked) {
                    NavigationGraph.navigateTo(SettingsScreen)
                    clicked = false
                }
            }
        }

        @Composable
        fun NewGameButton(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
            var clicked by remember { mutableStateOf(false) }

            Button(
                onClick = {
                    clicked = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
                enabled = !clicked
            ) {
                Text(if (!clicked) "New Game" else "Loading...")
            }

            LaunchedEffect(clicked) {
                if (clicked) {
                    try {
                        GameApi.new()
                        NavigationGraph.navigateTo(PlaygroundScreen)
                    } catch (e: ApiException) {
                        setErrorMessage("Failed to start a new game.")
                        setErrorOccurred(true)
                    }
                    clicked = false
                }
            }
        }

        @Composable
        fun LoginButton(login: TextFieldValue, onClick: () -> Unit) {
            var clicked by remember { mutableStateOf(false) }

            // Button component
            Button(
                onClick = {
                    clicked = true
                },
                modifier = Modifier
                    .padding(16.dp)
                    .width(200.dp),
                enabled = login.text.isNotEmpty() && !clicked
            ) {
                Text(if (clicked) "Loading..." else "Login")
            }

            // Button click event
            LaunchedEffect(clicked) {
                if (clicked) {
                    onClick()
                    clicked = false
                }
            }
        }

        @Composable
        fun LeaderBoardButton() {
            var clicked by remember { mutableStateOf(false) }
            Button(
                onClick = {
                    clicked = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width)
            ) {
                Text("Leaderboard")
            }

            LaunchedEffect(clicked) {
                if (clicked) {
                    NavigationGraph.navigateTo(LeaderBoardScreen)
                    clicked = false
                }
            }
        }

        @Composable
        fun QuitGameButton() {
            var showQuitDialog by remember { mutableStateOf(false) }
            Button(
                onClick = {
                    showQuitDialog = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
                colors = ButtonDefaults.buttonColors()
            ) {
                Text("Quit Game")
            }
            if (showQuitDialog) {
                Dialog(onDismissRequest = { showQuitDialog = false }) {
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
                                text = "Are you sure you want to quit the game?",
                                style = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold),
                                textAlign = TextAlign.Center
                            )

                            Spacer(modifier = Modifier.height(16.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceEvenly
                            ) {
                                // Cancel button
                                Button(onClick = { showQuitDialog = false }) {
                                    Text("Cancel")
                                }

                                // Confirm quit button
                                Button(onClick = {
                                    showQuitDialog = false
                                    NavigationGraph.navigateTo(UserProfile) // Navigate to a new screen or exit
                                }) {
                                    Text("Quit")
                                }
                            }
                        }
                    }
                }
            }
        }

        @Composable
        fun ProfileButton() {
            Button(
                onClick = {
                    NavigationGraph.navigateTo(UserProfile)
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
                colors = ButtonDefaults.buttonColors()
            ) {
                Text("My Profile")
            }
        }

        @Composable
        fun DeleteGameButton(enabled: Boolean, onClick: () -> Unit) {
            var showDeleteDialog by remember { mutableStateOf(false) }
            Button(
                onClick = {
                    showDeleteDialog = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(70.dp),
                colors = ButtonDefaults.buttonColors(disabledContainerColor = Color.Gray),
                enabled = enabled
            ) {
                // Trashcan emoji
                Text("🗑️")
            }

            if (showDeleteDialog) {
                Dialog(onDismissRequest = { showDeleteDialog = false }) {
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
                                text = "Are you sure you want to delete the last game?",
                                style = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold),
                                textAlign = TextAlign.Center
                            )

                            Spacer(modifier = Modifier.height(16.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceEvenly
                            ) {
                                // Cancel button
                                Button(onClick = { showDeleteDialog = false }) {
                                    Text("Cancel")
                                }

                                // Confirm delete button
                                Button(onClick = {
                                    onClick()
                                    showDeleteDialog = false
                                }) {
                                    Text("Delete")
                                }
                            }
                        }
                    }
                }
            }
        }

        @Composable
        fun ContinueGameButton(enabled: Boolean) {
            Button(
                onClick = {
                    NavigationGraph.navigateTo(PlaygroundScreen)
                },
                modifier = Modifier
                    .padding(padding)
                    .width(130.dp),
                colors = ButtonDefaults.buttonColors(disabledContainerColor = Color.Gray),
                enabled = enabled
            ) {
                Text("Continue")
            }
        }

        @Composable
        fun ResetPlaygroundButton() {
            var showResetDialog by remember { mutableStateOf(false) }
            Button(
                onClick = {
                    showResetDialog = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
                colors = ButtonDefaults.buttonColors()
            ) {
                Text("Reset Playground")
            }

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
                                    NavigationGraph.navigateTo(PlaygroundScreen)
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
        fun PauseButton() {
            Button(
                onClick = {
                    NavigationGraph.navigateTo(PauseScreen)
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
                colors = ButtonDefaults.buttonColors()
            ) {
                Text("Pause")
            }
        }

        @Composable
        fun ResumeButton() {
            Button(
                onClick = {
                    NavigationGraph.navigateTo(PlaygroundScreen)
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
                colors = ButtonDefaults.buttonColors()
            ) {
                Text("Resume")
            }
        }

        @Composable
        fun LogoutButton() {
            Button(
                onClick = {
                    GameApi.exit()
                    NavigationGraph.navigateTo(LoginScreen)
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
            ) {
                Text("Logout")
            }
        }

        @Composable
        fun ChangeUsernameButton(
            function: () -> Unit
        ) {
            var showNameDialog by remember { mutableStateOf(false) }
            var errorMessage by remember { mutableStateOf("") }
            Button(
                onClick = {
                    showNameDialog = true
                },
                modifier = Modifier
                    .padding(padding)
                    .width(width),
            ) {
                Text("Change Username")
            }

            if (showNameDialog) {
                Dialog(onDismissRequest = { showNameDialog = false }) {
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
                                text = "Username changing",
                                style = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold),
                                textAlign = TextAlign.Center
                            )

                            if (errorMessage.isNotEmpty()) {
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = errorMessage,
                                    style = TextStyle(fontSize = 14.sp, color = Color.Red),
                                    textAlign = TextAlign.Center
                                )
                            }

                            Spacer(modifier = Modifier.height(16.dp))

                            // Username text field
                            var username by remember { mutableStateOf(TextFieldValue()) }
                            var confirmActive by remember { mutableStateOf(false) }
                            TextField(
                                value = username,
                                onValueChange = {
                                    var newLogin = it.text
                                    newLogin = newLogin.trim()
                                    if (newLogin.length <= 12) {
                                        username = TextFieldValue(newLogin, it.selection)
                                        errorMessage = ""
                                    } else {
                                        errorMessage = "Limit 12 characters"
                                    }
                                    confirmActive = username.text.isNotEmpty()
                                },
                                label = { Text("Username") },
                                modifier = Modifier.width(200.dp)
                            )

                            Spacer(modifier = Modifier.height(16.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceEvenly
                            ) {
                                // Cancel button
                                Button(onClick = { showNameDialog = false }) {
                                    Text("Cancel")
                                }

                                // Confirm change username button
                                Button(
                                    onClick = {
                                        if (username.text.isNotEmpty()) {
                                            confirmActive = false
                                            try {
                                                GameApi.updateUsername(username.text)
                                                showNameDialog = false
                                                function()
                                            } catch (e: ApiException) {
                                                errorMessage = e.message ?: "An error occurred"
                                                confirmActive = true
                                            }
                                        }
                                    },
                                    enabled = confirmActive
                                ) {
                                    Text("Change")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
@Preview
fun DeleteGameButtonPreview() {
    var deleteGameEnabled by remember { mutableStateOf(true) }
    Row {
        Buttons.ContinueGameButton(deleteGameEnabled)
        Buttons.DeleteGameButton(deleteGameEnabled) {
            deleteGameEnabled = false
        }
    }
}