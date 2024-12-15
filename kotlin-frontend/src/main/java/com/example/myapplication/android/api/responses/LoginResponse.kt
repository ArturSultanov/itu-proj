package com.example.myapplication.android.api.responses

import com.example.myapplication.android.api.entries.BoardEntry

data class LoginResponse(
    val id: Int,
    val login: String,
    val highest_score: Int,
    var last_game: BoardEntry?
)