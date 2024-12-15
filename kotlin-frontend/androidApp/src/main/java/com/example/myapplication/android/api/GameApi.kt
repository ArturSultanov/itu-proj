package com.example.myapplication.android.api

import com.example.myapplication.android.api.HTTP.Companion.httpDelete
import com.example.myapplication.android.api.HTTP.Companion.httpGet
import com.example.myapplication.android.api.HTTP.Companion.httpPatch
import com.example.myapplication.android.api.HTTP.Companion.httpPost
import com.example.myapplication.android.api.entries.BoardEntry
import com.example.myapplication.android.api.entries.LeaderboardEntry
import com.example.myapplication.android.api.responses.LoginResponse
import com.example.myapplication.android.api.responses.MoveResponse
import com.google.gson.Gson

class GameApi {
    companion object {
        private const val API_LINK = "http://10.0.2.2:8000"
        private var username: String? = null
        private var game: Game? = null
        private var highestScore: Int = 0

        fun login(username: String): LoginResponse {
            this.username = username
            val url = "$API_LINK/login?login=$username"
            var response: Pair<Int, String>
            try {
                response = httpGet(url)
            } catch (e: ApiException) {
                throw ApiException("Login failed. ${e.message}")
            }
            val gson = Gson()
            val res = gson.fromJson(response.second, LoginResponse::class.java)
            game = if (res.last_game != null) {
                Game(res.last_game!!)
            } else {
                null
            }
            this.highestScore = res.highest_score
            this.username = username
            return res
        }

        fun leaderboard(): List<LeaderboardEntry> {
            val url = "$API_LINK/menu/leaderboard?limit=10"
            val response = httpGet(url)
            val gson = Gson()
            try {
                val res = gson.fromJson(response.second, Array<LeaderboardEntry>::class.java)
                return res.toList()
            } catch (e: Exception) {
                return emptyList()
            }
        }

        fun move(x1: Int, y1: Int, x2: Int, y2: Int): MoveResponse {
            val url = "$API_LINK/board/swap_gems"
            val response =
                httpPost(url, "{\"gems\":[{\"x\": $x1, \"y\": $y1}, {\"x\": $x2, \"y\": $y2}]}")
            val gson = Gson()
            if (response.first != 200) {
                return MoveResponse(-1, -1, emptyList())
            }
            return gson.fromJson(response.second, MoveResponse::class.java)
        }

        fun click(x1: Int, y1: Int): MoveResponse {
            val url = "$API_LINK/board/click_gem"
            val response = httpPost(url, "{\"x\": $x1, \"y\": $y1}")
            val gson = Gson()
            if (response.first != 200) {
                return MoveResponse(-1, -1, emptyList())
            }
            return gson.fromJson(response.second, MoveResponse::class.java)
        }

        fun new() {
            val url = "$API_LINK/menu/new_game"
            val response = httpGet(url)
            val gson = Gson()
            game = Game(gson.fromJson(response.second, BoardEntry::class.java))
        }

        fun setDifficulty(difficulty: Float): Boolean {
            val url = "$API_LINK/settings/set_difficulty"
            val res = httpPatch(url, "{\"difficulty\": ${difficulty.toInt()}}")
            return res.first == 200
        }

        fun getDifficulty(): Float {
            val url = "$API_LINK/settings/get_difficulty"
            val res = httpGet(url)
            val gson = Gson()
            val difficulty = gson.fromJson(res.second, Map::class.java)
            return difficulty["difficulty"].toString().toFloat()
        }

        fun hasGame(): Boolean {
            return game != null
        }

        fun getGame(): Game {
            if (game == null) {
                new()
            }
            return game!!
        }

        fun getHighestScore(): Int {
            if (game != null) {
                if (game!!.getScore() > highestScore) {
                    highestScore = game!!.getScore()
                }
            }
            return highestScore
        }

        fun getLastHighestScore(): Int {
            return highestScore
        }

        fun getUsername(): String {
            return username!!
        }

        fun delete() {
            val url = "$API_LINK/menu/delete_game"
            httpDelete(url)
            game = null
        }

        fun exit() {
            val url = "$API_LINK/utils/exit"
            httpPost(url, "")
            game = null
            username = null
        }

        fun updateUsername(username: String) {
            val url = "$API_LINK/settings/update_login"
            try {
                httpPatch(url, "{\"login\": \"$username\"}")
            } catch (e: ApiException) {
                throw ApiException("Username update failed. ${e.message}")
            }
            this.username = username
        }
    }
}