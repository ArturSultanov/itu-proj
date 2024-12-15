package com.example.myapplication.android.api

import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.RequestBody.Companion.toRequestBody
import java.net.SocketTimeoutException

class HTTP {

    companion object {
        fun httpGet(url: String): Pair<Int, String> {
            val client = OkHttpClient.Builder()
                .connectTimeout(1, java.util.concurrent.TimeUnit.SECONDS) // Connection timeout
                .readTimeout(1, java.util.concurrent.TimeUnit.SECONDS)    // Read timeout
                .writeTimeout(1, java.util.concurrent.TimeUnit.SECONDS)   // Write timeout
                .build()
            val request = okhttp3.Request.Builder().url(url).build()
            var responseBody = ""
            var code = 0
            var success = false
            var threadException: Exception? = null
            val t = Thread {
                try {
                    val response = client.newCall(request).execute()
                    responseBody = response.body?.string() ?: ""
                    code = response.code
                    success = response.isSuccessful
                } catch (e: SocketTimeoutException) {
                    threadException = ApiException("Socket connection timeout.")
                } catch (e: Exception) {
                    threadException = e
                }
            }
            t.start()
            t.join()
            if (threadException != null) {
                throw ApiException(threadException!!.message ?: "Network error")
            }
            if (!success) {
                throw ApiException.fromCode(code, "Network error")
            }
            return Pair(code, responseBody)
        }

        fun httpPost(url: String, body: String): Pair<Int, String> {
            val client = OkHttpClient.Builder()
                .connectTimeout(1, java.util.concurrent.TimeUnit.SECONDS) // Connection timeout
                .readTimeout(1, java.util.concurrent.TimeUnit.SECONDS)    // Read timeout
                .writeTimeout(1, java.util.concurrent.TimeUnit.SECONDS)   // Write timeout
                .build()
            val requestBody = body.toRequestBody("application/json".toMediaTypeOrNull())
            val request = okhttp3.Request.Builder()
                .url(url)
                .post(requestBody)
                .build()
            var responseBody = ""
            var code = 0
            var success = false
            var threadException: Exception? = null
            val t = Thread {
                try {
                    val response = client.newCall(request).execute()
                    responseBody = response.body?.string() ?: ""
                    code = response.code
                    success = response.isSuccessful
                } catch (e: SocketTimeoutException) {
                    threadException = ApiException("Socket connection timeout.")
                } catch (e: Exception) {
                    threadException = e
                }
            }
            t.start()
            t.join()
            if (threadException != null) {
                throw ApiException(threadException!!.message ?: "Network error")
            }
            if (!success) {
                throw ApiException.fromCode(code, "Network error")
            }
            return Pair(code, responseBody)
        }

        fun httpPatch(url: String, body: String): Pair<Int, String> {
            val client = OkHttpClient.Builder()
                .connectTimeout(1, java.util.concurrent.TimeUnit.SECONDS) // Connection timeout
                .readTimeout(1, java.util.concurrent.TimeUnit.SECONDS)    // Read timeout
                .writeTimeout(1, java.util.concurrent.TimeUnit.SECONDS)   // Write timeout
                .build()
            val requestBody = body.toRequestBody("application/json".toMediaTypeOrNull())
            val request = okhttp3.Request.Builder()
                .url(url)
                .patch(requestBody)
                .build()
            var responseBody = ""
            var code = 0
            var success = false
            var threadException: Exception? = null
            val t = Thread {
                try {
                    val response = client.newCall(request).execute()
                    responseBody = response.body?.string() ?: ""
                    code = response.code
                    success = response.isSuccessful
                } catch (e: SocketTimeoutException) {
                    threadException = ApiException("Socket connection timeout.")
                } catch (e: Exception) {
                    threadException = e
                }
            }
            t.start()
            t.join()
            if (threadException != null) {
                throw ApiException(threadException!!.message ?: "Network error")
            }
            if (!success) {
                throw ApiException.fromCode(code, "Network error")
            }
            return Pair(code, responseBody)
        }

        fun httpDelete(url: String): Pair<Int, String> {
            val client = OkHttpClient.Builder()
                .connectTimeout(1, java.util.concurrent.TimeUnit.SECONDS) // Connection timeout
                .readTimeout(1, java.util.concurrent.TimeUnit.SECONDS)    // Read timeout
                .writeTimeout(1, java.util.concurrent.TimeUnit.SECONDS)   // Write timeout
                .build()
            val request = okhttp3.Request.Builder().url(url).delete().build()
            var responseBody = ""
            var code = 0
            var success = false
            var threadException: Exception? = null
            val t = Thread {
                try {
                    val response = client.newCall(request).execute()
                    responseBody = response.body?.string() ?: ""
                    code = response.code
                    success = response.isSuccessful
                } catch (e: SocketTimeoutException) {
                    threadException = ApiException("Socket connection timeout.")
                } catch (e: Exception) {
                    threadException = e
                }
            }
            t.start()
            t.join()
            if (threadException != null) {
                throw ApiException(threadException!!.message ?: "Network error")
            }
            if (!success) {
                throw ApiException.fromCode(code, "Network error")
            }
            return Pair(code, responseBody)
        }
    }
}