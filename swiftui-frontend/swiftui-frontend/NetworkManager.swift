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
    
    // MARK: - Login at the app start up
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
    
    // MARK: - Start new game at the main menu
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
            playerDataManager.playerData?.lastGame = newGameSession
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

