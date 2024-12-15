package com.example.myapplication.android.screen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import kotlinx.coroutines.delay

sealed class AppScreen(val route: String) {
    var navController: NavHostController? = null

    private var _errorOccurred by mutableStateOf(false)
    private var _errorMessage by mutableStateOf("")

    val errorOccurred: Boolean
        get() = _errorOccurred
    val errorMessage: String
        get() = _errorMessage

    private fun setErrorOccurred(value: Boolean) {
        _errorOccurred = value
    }

    private fun setErrorMessage(value: String) {
        _errorMessage = value
    }

    @Composable
    fun Content(preview: Boolean = false) {
        ScreenSurface {
            Column(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.weight(1f))
                Row(
                    modifier = Modifier
                        .fillMaxSize()
                        .weight(2f),
                    horizontalArrangement = Arrangement.Center
                ) {
                    HeaderTop(
                        errorOccurred = _errorOccurred,
                        errorMessage = _errorMessage,
                        setErrorOccurred = { setErrorOccurred(it) },
                        setErrorMessage = { setErrorMessage(it) }
                    )
                }
                Spacer(modifier = Modifier.weight(1f))
                Row(
                    modifier = Modifier
                        .fillMaxSize()
                        .weight(14f),
                    horizontalArrangement = Arrangement.Center
                ) {
                    BodyTop(
                        setErrorOccurred = { setErrorOccurred(it) },
                        setErrorMessage = { setErrorMessage(it) }
                    )
                }
                Spacer(modifier = Modifier.weight(1f))
                Row(
                    modifier = Modifier
                        .fillMaxSize()
                        .weight(2f),
                    horizontalArrangement = Arrangement.Center
                ) {
                    FooterTop(
                        setErrorOccurred = { setErrorOccurred(it) },
                        setErrorMessage = { setErrorMessage(it) }
                    )
                }
                Spacer(modifier = Modifier.weight(1f))
            }
        }
    }

    @Composable
    private fun HeaderTop(
        errorOccurred: Boolean,
        errorMessage: String,
        setErrorOccurred: (Boolean) -> Unit,
        setErrorMessage: (String) -> Unit
    ) {
        Column {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(1f),
                horizontalArrangement = Arrangement.Center
            ) {
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Header(setErrorOccurred, setErrorMessage)
                }
            }
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(1f),
                horizontalArrangement = Arrangement.Center
            ) {
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    HeaderErrorMessages(errorOccurred, errorMessage)
                }
            }
        }
    }

    @Composable
    abstract fun Header(
        setErrorOccurred: (Boolean) -> Unit,
        setErrorMessage: (String) -> Unit
    )

    @Composable
    fun HeaderErrorMessages(errorOccurred: Boolean, errorMessage: String) {
        Text(
            errorMessage,
            color = MaterialTheme.colorScheme.error
        )
        if (errorOccurred) {
            LaunchedEffect(errorMessage) {
                delay(5000)
                setErrorMessage("")
                setErrorOccurred(false)
            }
        }
    }

    @Composable
    private fun BodyTop(
        setErrorOccurred: (Boolean) -> Unit,
        setErrorMessage: (String) -> Unit
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Body(setErrorOccurred, setErrorMessage)
        }
    }

    @Composable
    abstract fun Body(
        setErrorOccurred: (Boolean) -> Unit,
        setErrorMessage: (String) -> Unit
    )

    @Composable
    private fun FooterTop(
        setErrorOccurred: (Boolean) -> Unit,
        setErrorMessage: (String) -> Unit
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Footer(setErrorOccurred, setErrorMessage)
        }
    }

    @Composable
    abstract fun Footer(
        setErrorOccurred: (Boolean) -> Unit,
        setErrorMessage: (String) -> Unit
    )


    companion object {

        @Composable
        private fun ScreenSurface(content: @Composable () -> Unit) {
            Surface(
                modifier = Modifier.fillMaxSize(),
                color = MaterialTheme.colorScheme.background
            ) {
                content()
            }
        }
    }
}