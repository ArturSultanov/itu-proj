package com.example.myapplication.android.screen

import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myapplication.android.Buttons
import com.example.myapplication.android.api.GameApi

data object UserProfile : AppScreen("user_profile") {
    @Composable
    override fun Header(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Text(
            "Player Profile",
            style = MaterialTheme.typography.titleLarge
        )
    }

    @Composable
    override fun Body(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        val continueEnabled by remember {
            mutableStateOf(
                GameApi.hasGame() && GameApi.getGame().getMovesLeft() != 0
            )
        }
        var lastGameButtonsEnabled by remember { mutableStateOf(continueEnabled) }
        val username by remember { mutableStateOf(GameApi.getUsername()) }
        val score by remember { mutableIntStateOf(GameApi.getHighestScore()) }

        Text(
            "Welcome back, $username",
            style = TextStyle(
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            ),
            modifier = Modifier.padding(bottom = 20.dp)
        )
        Text(
            text = "Your highest score is $score",
            style = TextStyle(
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold
            ),
        )
        Spacer(modifier = Modifier.height(80.dp))
        if (continueEnabled) {
            Row {
                Buttons.ContinueGameButton(lastGameButtonsEnabled)
                Buttons.DeleteGameButton(lastGameButtonsEnabled) {
                    GameApi.delete()
                    lastGameButtonsEnabled = false
                }
            }
        }
        Buttons.NewGameButton(setErrorOccurred, setErrorMessage)
        Buttons.LeaderBoardButton()
        Buttons.SettingsButton()
    }

    @Composable
    override fun Footer(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Buttons.LogoutButton()
    }
}

@Preview
@Composable
fun NewGameScreenPreview() {
    UserProfile.Content(true)
}