package com.example.myapplication.android.screen

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myapplication.android.Buttons
import com.example.myapplication.android.MyApplicationTheme
import com.example.myapplication.android.NavigationGraph
import com.example.myapplication.android.api.ApiException
import com.example.myapplication.android.api.GameApi

data object LoginScreen : AppScreen("login") {
    @Composable
    override fun Header(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Text(
            "Login",
            style = MaterialTheme.typography.titleLarge
        )
    }

    @Composable
    override fun Body(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        var login by remember { mutableStateOf(TextFieldValue()) }

        TextField(
            value = login,
            onValueChange = {
                var newLogin = it.text
                newLogin = newLogin.trim()
                if (newLogin.length <= 12) {
                    login = TextFieldValue(newLogin, it.selection)
                    if (errorOccurred) {
                        setErrorOccurred(false)
                        setErrorMessage("")
                    }
                } else {
                    setErrorOccurred(true)
                    setErrorMessage("Name must be 12 characters or less")
                }
            },
            label = {
                Text(
                    "Enter name",
                    style = MaterialTheme.typography.bodyLarge
                        .plus(TextStyle(textAlign = TextAlign.Center)),
                    modifier = Modifier.fillMaxWidth()
                )
            },
            modifier = Modifier
                .width(200.dp)
                .height(70.dp),
            textStyle = MaterialTheme.typography.bodyLarge
                .plus(TextStyle(textAlign = TextAlign.Center))
        )
        Buttons.LoginButton(login) {
            try {
                GameApi.login(login.text)
                NavigationGraph.navigateTo(UserProfileScreen)
            } catch (e: ApiException) {
                setErrorOccurred(true)
                setErrorMessage(e.message ?: "An error occurred")
            }
        }
    }

    @Composable
    override fun Footer(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {

    }
}

@Composable
@Preview
fun LoginScreenPreview() {
    MyApplicationTheme {
        LoginScreen.Content(false)
    }
}