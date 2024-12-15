package com.example.myapplication.android

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.myapplication.android.screen.AppScreen
import com.example.myapplication.android.screen.GameOverScreen
import com.example.myapplication.android.screen.LeaderBoardScreen
import com.example.myapplication.android.screen.LoginScreen
import com.example.myapplication.android.screen.PauseScreen
import com.example.myapplication.android.screen.PlaygroundScreen
import com.example.myapplication.android.screen.SettingsScreen
import com.example.myapplication.android.screen.UserProfileScreen

class NavigationGraph(private val navController: NavHostController) {

    private val screens = listOf(
        LoginScreen,
        UserProfileScreen,
        PlaygroundScreen,
        PauseScreen,
        LeaderBoardScreen,
        GameOverScreen,
        SettingsScreen
    )

    @Composable
    fun SetupNavGraph(startDestination: AppScreen = LoginScreen) {
        NavHost(
            navController = navController,
            startDestination = startDestination.route
        ) {
            screens.forEach { screen ->
                composable(screen.route) {
                    screen.navController = navController; screen.Content(
                    false
                )
                }
            }
        }
        setNavController(navController)
    }

    companion object {
        private lateinit var navController: NavHostController

        fun setNavController(controller: NavHostController) {
            navController = controller
        }

        fun navigateTo(screen: AppScreen) {
            navController.navigate(screen.route)
        }

        fun navigateBack() {
            navController.popBackStack()
        }
    }
}