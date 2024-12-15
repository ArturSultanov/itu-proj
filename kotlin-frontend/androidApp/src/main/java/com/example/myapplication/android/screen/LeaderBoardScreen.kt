package com.example.myapplication.android.screen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
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
import com.example.myapplication.android.api.entries.LeaderboardEntry

data object LeaderBoardScreen : AppScreen("leaderboard") {
    @Composable
    override fun Header(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Text(
            "Leaderboard",
            style = MaterialTheme.typography.titleLarge
        )
    }

    @Composable
    override fun Body(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Spacer(modifier = Modifier.height(16.dp))
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "Place",
                style = TextStyle(
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                ),
                modifier = Modifier.weight(2f),
                textAlign = TextAlign.Center
            )
            Text(
                text = "Name",
                style = TextStyle(
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                ),
                modifier = Modifier.weight(5f),
                textAlign = TextAlign.Center
            )
            Text(
                text = "Score",
                style = TextStyle(
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                ),
                modifier = Modifier.weight(2f),
                textAlign = TextAlign.Center
            )
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Leaderboard entries
        var leaderPairs = listOf<LeaderboardEntry>()

        try {
            leaderPairs = GameApi.leaderboard()
        } catch (e: Exception) {
            setErrorOccurred(true)
            setErrorMessage("Cannot retrieve leaderboard")
        }

        leaderPairs.forEachIndexed { i, (name, score) ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                val placeText = when (i) {
                    0 -> "🥇"
                    1 -> "🥈"
                    2 -> "🥉"
                    else -> "${i + 1}"
                }
                Text(
                    text = placeText,
                    style = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold),
                    modifier = Modifier.weight(2f),
                    textAlign = TextAlign.Center
                )
                Text(
                    text = name,
                    style = TextStyle(fontSize = 18.sp),
                    modifier = Modifier.weight(5f),
                    textAlign = TextAlign.Center
                )
                Text(
                    text = score.toString(),
                    style = TextStyle(fontSize = 18.sp),
                    modifier = Modifier.weight(2f),
                    textAlign = TextAlign.Center
                )
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
fun LeaderBoardPreview() {
    LeaderBoardScreen.Content(true)
}
