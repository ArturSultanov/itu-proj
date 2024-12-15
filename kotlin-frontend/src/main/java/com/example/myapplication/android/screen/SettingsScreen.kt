package com.example.myapplication.android.screen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myapplication.android.Buttons
import com.example.myapplication.android.NavigationGraph
import com.example.myapplication.android.api.GameApi

data object SettingsScreen : AppScreen("settings") {
    @Composable
    override fun Header(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Text(
            "Settings",
            style = MaterialTheme.typography.titleLarge
        )
    }

    @Composable
    override fun Body(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {

        var startDiff = 0f

        try {
            startDiff = GameApi.getDifficulty()
        } catch (e: Exception) {
            setErrorOccurred(true)
            setErrorMessage(e.message ?: "Cannot fetch difficulty.")
        }

        var difficulty by remember { mutableFloatStateOf(startDiff) }
        var username by remember { mutableStateOf(GameApi.getUsername()) }

        Column {
            Text(
                text = "Username: $username",
                style = TextStyle(
                    fontWeight = FontWeight.Bold,
                    fontSize = 20.sp,
                    textAlign = TextAlign.Center
                ),
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )
            Spacer(modifier = Modifier.height(10.dp))
            Buttons.ChangeUsernameButton {
                username = GameApi.getUsername()
            }
        }

        Spacer(modifier = Modifier.height(30.dp))

        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Difficulty:"
            )
            Slider(
                value = difficulty,
                onValueChange = { difficulty = it },
                onValueChangeFinished = { GameApi.setDifficulty(difficulty) },
                valueRange = 0f..2f,
                steps = 1,
                colors = SliderDefaults.colors(
                    thumbColor = MaterialTheme.colorScheme.secondary,
                    activeTrackColor = MaterialTheme.colorScheme.primary,
                    inactiveTrackColor = MaterialTheme.colorScheme.primary
                ),
                modifier = Modifier.width(300.dp)
            )
            Row(
                modifier = Modifier.width(320.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(text = "Easy")
                Text(text = "Medium")
                Text(text = "Hard")
            }
        }
    }

    @Composable
    override fun Footer(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Buttons.BackButton()
    }
}


@Preview
@Composable
fun SettingsScreenPreview() {
    SettingsScreen.Content(true)
}