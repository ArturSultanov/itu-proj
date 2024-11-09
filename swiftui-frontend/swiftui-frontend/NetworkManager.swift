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
}

