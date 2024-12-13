//
//  NetworkRequestManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import Foundation


enum NetworkError: Error {
    case invalidURL
    case invalidLogin
    case invalidResponse(statusCode: Int)
    case decodingError
    case noMatchesFound
    case noData
}

/// Handles all network interactions for the app
@MainActor @Observable class NetworkManager {
//    static let shared = NetworkManager() // Singleton instance.
//    private init() {}

    private let baseURL = "http://127.0.0.1:8000" // Base URL for API requests.
}

/// Login request
extension NetworkManager {
    /// Logs in a user by their login ID and updates the `PlayerDataManager`.
    /// - Parameters:
    ///   - loginID: The login identifier for the user.
    ///   - playerDataManager: The shared player data manager to update upon successful login.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding is unsuccessful.
    func login(with loginID: String, playerDataManager: PlayerDataManager) async throws {
        // Construct the URL with query parameters
        var urlComponents = URLComponents(string: "\(baseURL)/login")
        urlComponents?.queryItems = [URLQueryItem(name: "login", value: loginID)]
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        // Create a GET request
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        // Perform the network request
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidLogin
        }
        
        // Decode the response data
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let playerData = try decoder.decode(PlayerData.self, from: data)
            playerDataManager.playerData = playerData
        } catch {
            throw NetworkError.decodingError
        }
    }
}

/// New game request
extension NetworkManager {
    /// Starts a new game and updates the player's data.
    /// - Parameter playerDataManager: The shared player data manager to update upon successful game initialization.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding is unsuccessful.
    func newGame(playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/menu/new_game") else {
            throw NetworkError.invalidURL
        }

        let (data, response) = try await URLSession.shared.data(from: url)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidLogin
        }
        
        // Decode the response data
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let newGameSession = try decoder.decode(GameSession.self, from: data)
            
            if let player = playerDataManager.playerData {
                player.lastGame = newGameSession
                playerDataManager.playerData = player
            }
        } catch {
            throw NetworkError.decodingError
        }
    }
}

/// Swap gems request
extension NetworkManager {
    /// Swaps two gems on the board and updates the game session with the server response.
    /// - Parameters:
    ///   - gem1: The first gem to swap.
    ///   - gem2: The second gem to swap.
    ///   - playerDataManager: The shared player data manager to update upon successful response.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding is unsuccessful.
    func swapGems(gem1: Gem, gem2: Gem, playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/board/swap_gems") else {
            throw NetworkError.invalidURL
        }

        // Create the POST request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Prepare the request body
        let body: [String: [[String: Int]]] = [
            "gems": [
                ["x": gem1.x, "y": gem1.y],
                ["x": gem2.x, "y": gem2.y]
            ]
        ]
        request.httpBody = try JSONEncoder().encode(body)

        // Perform the network request
        let (data, response) = try await URLSession.shared.data(for: request)

        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidResponse(statusCode: (response as? HTTPURLResponse)?.statusCode ?? 0)
        }

        // Decode the response and update the game session
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase

            let swapResponse = try decoder.decode(SwapResponse.self, from: data)
            playerDataManager.updateGameSession(with: swapResponse)
        } catch {
            throw NetworkError.decodingError
        }
    }
}

/// Click gem request
extension NetworkManager {
    /// Sends a click action for a gem to the backend and updates the local game session.
    /// - Parameters:
    ///   - gem: The gem that was clicked.
    ///   - playerDataManager: The shared player data manager.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding fails.
    func clickGem(gem: Gem, playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/board/click_gem") else {
            throw NetworkError.invalidURL
        }
        
        // Prepare POST request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Int] = ["x": gem.x, "y": gem.y]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse(statusCode: 0)
        }

        // Decode the response
        if (200...299).contains(httpResponse.statusCode) {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            let clickResponse = try decoder.decode(SwapResponse.self, from: data)
            playerDataManager.updateGameSession(with: clickResponse)
        } else {
            throw NetworkError.invalidResponse(statusCode: httpResponse.statusCode)
        }
    }
}

/// Leaderboard request
extension NetworkManager {
    func fetchLeaderboard(with limit: Int) async throws -> [LeaderboardEntry] {
        // Construct the URL with query parameters
        var urlComponents = URLComponents(string: "\(baseURL)/menu/leaderboard")
        urlComponents?.queryItems = [URLQueryItem(name: "limit", value: String(limit))]
        
        guard let url = urlComponents?.url else {
            throw URLError(.badURL)
        }
        
        // Create a GET request
        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        // Perform the network call
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        // Decode the response
        let leaderboard = try JSONDecoder().decode([LeaderboardEntry].self, from: data)
        return leaderboard
    }
}

/// Update login request
extension NetworkManager {
    /// Updates the player's login name in the backend and local player data.
    /// - Parameters:
    ///   - newLogin: The new login name to be updated.
    ///   - playerDataManager: The shared player data manager.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding fails.
    func updateLogin(newLogin: String, playerDataManager: PlayerDataManager) async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/settings/update_login")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        // Prepare PATCH request
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["login": newLogin]
        request.httpBody = try JSONEncoder().encode(body)
        
        // Perform the network request
        let (_, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        // Update local player data
        if let player = playerDataManager.playerData {
            player.login = newLogin
            playerDataManager.playerData = player
        }
    }
}

/// Change difficulty request
extension NetworkManager {
    /// Updates the difficulty level in the backend and local player data.
    /// - Parameters:
    ///   - difficulty: The new difficulty level to be set.
    ///   - playerDataManager: The shared player data manager.
    /// - Throws: Throws a `NetworkError` if the request fails.
    func setDifficulty(_ difficulty: Int, playerDataManager: PlayerDataManager) async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/settings/set_difficulty")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
                
        // Prepare PATCH request
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["difficulty": difficulty]
        request.httpBody = try JSONEncoder().encode(body)
        
        // Perform the network request
        let (_, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }

        // Update local player data
        if let player = playerDataManager.playerData {
            player.difficulty = difficulty
            playerDataManager.playerData = player
        }
    }
}

/// Get diffuculty request
extension NetworkManager {
    /// Fetches the current difficulty level from the backend.
    /// - Returns: The current difficulty level.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding fails.
    func getDifficulty() async throws -> Int {
        let urlComponents = URLComponents(string: "\(baseURL)/settings/get_difficulty")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
                
        // Prepare GET request
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        // Decode the response
        struct DifficultyResponse: Codable {
            let difficulty: Int
        }
        
        let difficultyData = try JSONDecoder().decode(DifficultyResponse.self, from: data)
        return difficultyData.difficulty
    }
}

/// Continue game request
extension NetworkManager {
    /// Continues the last game session and updates the local player data.
    /// - Parameter playerDataManager: The shared player data manager.
    /// - Throws: Throws a `NetworkError` if the request fails or decoding fails.
    func continue_game(playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/menu/continue") else {
            throw NetworkError.invalidURL
        }

        let (data, response) = try await URLSession.shared.data(from: url)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidLogin
        }
        
        // Decode the response
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let continueGameSession = try decoder.decode(GameSession.self, from: data)
            playerDataManager.playerData?.lastGame = continueGameSession
        } catch {
            throw NetworkError.decodingError
        }
    }
}

/// Quit game handling (syncronization)
extension NetworkManager {
    /// Sends a quit request to the backend.
    /// - Throws: Throws a `NetworkError` if the request fails.
    func quitGame() async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/utils/exit")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        // Prepare POST request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Perform the network request
        let (_, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
    }
}

/// Delete game request
extension NetworkManager {
    /// Deletes the last game session and updates the local player data.
    /// - Parameter playerDataManager: The shared player data manager.
    /// - Throws: Throws a `NetworkError` if the request fails.
    func deleteGame(playerDataManager: PlayerDataManager) async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/menu/delete_game")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        // Prepare DELETE request
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        // Validate the response
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        // Update local player data
        if let player = playerDataManager.playerData {
            player.lastGame = nil
            playerDataManager.playerData = player
        }
    }
}
