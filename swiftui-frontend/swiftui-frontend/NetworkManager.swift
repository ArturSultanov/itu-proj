//
//  NetworkRequestManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import Foundation


enum NetworkError: Error {
    case invalidURL
    case invalidResponse
    case decodingError
    case noData
}


class NetworkManager: ObservableObject {
    static let shared = NetworkManager()
    private init() {}

    private let baseURL = "http://127.0.0.1:8000"
    
    // MARK: - Login at the app start up
    func login(with loginID: String, playerDataManager: PlayerDataManager) async throws {
        guard let url = URL(string: "\(baseURL)/login") else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: String] = ["login": loginID]
        request.httpBody = try? JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidResponse
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let playerData = try decoder.decode(PlayerData.self, from: data)
            DispatchQueue.main.async {
                playerDataManager.playerData = playerData
            }
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
            throw NetworkError.invalidResponse
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let newGameSession = try decoder.decode(GameSession.self, from: data)
            DispatchQueue.main.async {
                playerDataManager.playerData?.lastGame = newGameSession
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
        
        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidResponse
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            let swapResponse = try JSONDecoder().decode(SwapResponse.self, from: data)
            DispatchQueue.main.async {
                playerDataManager.updateGameSession(with: swapResponse)
            }
        } catch {
            throw NetworkError.decodingError
        }
    }
}

