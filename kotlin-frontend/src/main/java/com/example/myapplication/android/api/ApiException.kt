package com.example.myapplication.android.api

class ApiException(message: String) : Exception(message) {
    companion object {
        fun fromCode(code: Int, message: String): ApiException {
            return when (code) {
                400 -> BadRequestException()
                401 -> UnauthorizedException()
                403 -> ForbiddenException()
                404 -> NotFoundException()
                406 -> IllegalMove()
                500 -> InternalServerErrorException()
                else -> UnknownException(message)
            }
        }

        private fun IllegalMove(): ApiException {
            return ApiException("Illegal move")
        }

        private fun UnknownException(message: String): ApiException {
            return ApiException(message)
        }

        private fun InternalServerErrorException(): ApiException {
            return ApiException("Internal server error")
        }

        private fun NotFoundException(): ApiException {
            return ApiException("Not found")
        }

        private fun ForbiddenException(): ApiException {
            return ApiException("Forbidden")
        }

        private fun UnauthorizedException(): ApiException {
            return ApiException("Unauthorized")
        }

        private fun BadRequestException(): ApiException {
            return ApiException("Bad request")
        }
    }
}