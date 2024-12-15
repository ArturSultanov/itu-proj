package com.example.myapplication.android.api

import com.example.myapplication.android.api.entries.BoardEntry
import com.example.myapplication.android.screen.GridElement

class Game(var boardEntry: BoardEntry) {

    fun getScore(): Int {
        return boardEntry.current_score
    }

    fun getMovesLeft(): Int {
        return boardEntry.moves_left
    }

    fun getGrid(): List<List<GridElement>> {
        val board_status = boardEntry.board_status
        return List(board_status.size) { y ->
            List(board_status.size) { x ->
                GridElement(board_status[y][x], x, y)
            }
        }
    }

    fun makeMove(x1: Int, y1: Int, x2: Int, y2: Int) {
        // Get the updated gems from the API
        val res = GameApi.move(x1, y1, x2, y2)
        val updatedGems = res.updated_gems

        // Loop through the board and update it with the new gems
        for (update in updatedGems) {
            boardEntry.board_status[update.y][update.x] = update.type
        }
        if (res.moves_left != -1) {
            boardEntry.moves_left = res.moves_left
        }
        if (res.current_score != -1) {
            boardEntry.current_score = res.current_score
        }
        if (res.current_score == -1 && res.moves_left == -1) {
            throw ApiException("Invalid move.")
        }
    }

    fun bonusMove(x1: Int, y1: Int) {
        // Get the updated gems from the API
        val res = GameApi.click(x1, y1)
        val updatedGems = res.updated_gems

        // Loop through the board and update it with the new gems
        for (update in updatedGems) {
            boardEntry.board_status[update.y][update.x] = update.type
        }
        if (res.moves_left != -1) {
            boardEntry.moves_left = res.moves_left
        }
        if (res.current_score != -1) {
            boardEntry.current_score = res.current_score
        }
    }

    fun setDifficulty(difficulty: Float) {
        GameApi.setDifficulty(difficulty)
        println("Setting difficulty to ${difficulty.toInt()}")
    }

    fun getDifficulty(): Float {
        return GameApi.getDifficulty()
    }

    companion object {

        fun getDraft(): Game {
            return Game(BoardEntry(0, 0, MutableList(6) { MutableList(6) { 0 } }))
        }

    }

}