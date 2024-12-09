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

@MainActor
class NetworkManager: ObservableObject {
    static let shared = NetworkManager()
    private init() {}

    private let baseURL = "http://127.0.0.1:8000"
    
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
    
    func newGame(playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/menu/new_game") else {
            throw NetworkError.invalidURL
        }

        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidLogin
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let newGameSession = try decoder.decode(GameSession.self, from: data)
            
//            playerDataManager.playerData?.lastGame = newGameSession
            
            if var player = playerDataManager.playerData {
                player.lastGame = newGameSession
                playerDataManager.playerData = player
            }
        } catch {
            throw NetworkError.decodingError
        }
    }
    
    func swapGems(gem1: Gem, gem2: Gem, playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/board/swap_gems") else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: [[String: Int]]] = [
            "gems": [
                ["x": gem1.x, "y": gem1.y],
                ["x": gem2.x, "y": gem2.y]
            ]
        ]
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse(statusCode: 0)
        }

        if (200...299).contains(httpResponse.statusCode) {
            // Proceed with decoding
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase

            let swapResponse = try decoder.decode(SwapResponse.self, from: data)
            playerDataManager.updateGameSession(with: swapResponse)
        } else {
            throw NetworkError.invalidResponse(statusCode: httpResponse.statusCode)
        }
    }
    
    
}


//extension NetworkManager {
//    func fetchLeaderboard(with limit: Int) async throws -> [LeaderboardEntry] {
//        var urlComponents = URLComponents(string: "\(baseURL)/menu/leaderboard")
//        urlComponents?.queryItems = [URLQueryItem(name: "limit", value: limit)]
//        guard let url = urlComponents?.url else {
//            throw NetworkError.invalidURL
//        }
//        
//        // Create a GET request
//        var request = URLRequest(url: url)
//        request.httpMethod = "GET"
//
//        
//        let (data, response) = try await URLSession.shared.data(for: request)
//        
//        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
//            throw URLError(.badServerResponse)
//        }
//        
//        let leaderboard = try JSONDecoder().decode([LeaderboardEntry].self, from: data)
//        return leaderboard
//    }
//}

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



extension NetworkManager {
    func updateLogin(newLogin: String, playerDataManager: PlayerDataManager) async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/settings/update_login")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["login": newLogin]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        // Update local player data
        if var player = playerDataManager.playerData {
            player.login = newLogin
            playerDataManager.playerData = player
        }
    }
    
    func setDifficulty(_ difficulty: Int, playerDataManager: PlayerDataManager) async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/settings/set_difficulty")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
                
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["difficulty": difficulty]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }

        if var player = playerDataManager.playerData {
            // Assuming you have a difficulty property in PlayerData
            player.difficulty = difficulty
            playerDataManager.playerData = player
        }
    }
}


extension NetworkManager {
    func getDifficulty() async throws -> Int {
        let urlComponents = URLComponents(string: "\(baseURL)/settings/get_difficulty")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
                
        var request = URLRequest(url: url)
        
        request.httpMethod = "GET"
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        struct DifficultyResponse: Codable {
            let difficulty: Int
        }
        
        let difficultyData = try JSONDecoder().decode(DifficultyResponse.self, from: data)
        return difficultyData.difficulty
    }
}


extension NetworkManager {
    func continue_game(playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/menu/continue") else {
            throw NetworkError.invalidURL
        }

        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidLogin
        }
        
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


extension NetworkManager {
    func quitGame() async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/utils/exit")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
    }
}


extension NetworkManager {
    func deleteGame(playerDataManager: PlayerDataManager) async throws {
        let urlComponents = URLComponents(string: "\(baseURL)/menu/delete_game")
        
        guard let url = urlComponents?.url else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        // Set lastGame to nil after successful deletion
        if var player = playerDataManager.playerData {
            player.lastGame = nil
            playerDataManager.playerData = player
        }
    }
}


extension NetworkManager {
    func clickGem(gem: Gem, playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/board/click_gem") else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Int] = [
            "x": gem.x,
            "y": gem.y
        ]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse(statusCode: 0)
        }

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
