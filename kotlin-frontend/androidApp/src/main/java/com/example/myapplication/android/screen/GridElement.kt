package com.example.myapplication.android.screen

import androidx.compose.ui.graphics.Color

data class GridElement(var value: Int, var x: Int, var y: Int) {

    private val first = Color(187, 190, 242)
    private val second = Color(247, 193, 121)
    private val third = Color(154, 127, 112)
    private val fourth = Color(99, 106, 141)
    private val bonus = Color(83, 74, 78)

    fun getColor(): Color {
        return when (value) {
            0 -> first
            1 -> second
            2 -> third
            3 -> fourth
            4 -> bonus
            else -> Color.Black
        }
    }

    fun getValue(): String {
        return value.toString()
    }

    fun isBonus(): Boolean {
        return value >= 4
    }
}
