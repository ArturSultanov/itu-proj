package com.example.myapplication.android.api.responses

import com.example.myapplication.android.api.entries.UpdateEntry

data class MoveResponse(
    val current_score: Int,
    val moves_left: Int,
    val updated_gems: List<UpdateEntry>
)