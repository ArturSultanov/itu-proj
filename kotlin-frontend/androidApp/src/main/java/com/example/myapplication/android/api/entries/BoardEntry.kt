package com.example.myapplication.android.api.entries

data class BoardEntry(
    var current_score: Int,
    var moves_left: Int,
    var board_status: MutableList<MutableList<Int>>
)