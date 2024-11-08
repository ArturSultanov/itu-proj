//
//  NetworkManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.11.2024.
//

import Foundation

@Observable
class NetworkManager {
    static let shared = NetworkManager()
    private let baseURL = "http://127.0.0.1:8000"

    // Login API Call
    func login(with login: String) async throws -> User {
        guard let url = URL(string: "\(baseURL)/login") else {
            throw URLError(.badURL)
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let body = ["login": login]
        request.httpBody = try JSONEncoder().encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let (data, response) = try await URLSession.shared.data(for: request)
        guard let response = response as? HTTPURLResponse, response.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            let user = try decoder.decode(User.self, from: data)
            return user
        } catch {
            throw URLError(.cannotDecodeContentData)
        }

    }

    // New Game API Call
    func newGame() async throws -> Game {
        guard let url = URL(string: "\(baseURL)/menu/new_game") else {
            throw URLError(.badURL)
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        let game = try JSONDecoder().decode(Game.self, from: data)
        return game
    }

    // Swap Gems API Call
    func swapGems(requestBody: SwapGemsRequest) async throws -> SwapGemsResponse {
        guard let url = URL(string: "\(baseURL)/board/swap_gems") else {
            throw URLError(.badURL)
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = try JSONEncoder().encode(requestBody)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(SwapGemsResponse.self, from: data)
        return response
    }
}
