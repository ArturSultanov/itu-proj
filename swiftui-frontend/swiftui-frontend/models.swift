//
//  models.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.11.2024.
//

import Foundation

// MARK: - Login
struct LoginRequest: Codable {
    let login: String
}

struct LastGame: Codable {
    let current_score: Int
    let moves_left: Int
    let board_status: [[Int]]?
}

struct UserData: Codable {
    let login: String
    let id: Int
    let highest_score: Int
    let last_game: LastGame?
}

// MARK: - New Game
struct NewGameResponse: Codable {
    let current_score: Int
    let moves_left: Int
    let board_status: [[Int]]
}

// MARK: - Swap Gems
struct SwapGemsRequest: Codable {
    struct Gem: Codable {
        let x: Int
        let y: Int
    }
    let gems: [Gem]
}

struct SwapGemsResponse: Codable {
    let current_score: Int
    let moves_left: Int
    let updated_gems: [UpdatedGem]
}

struct UpdatedGem: Codable, Identifiable {
    var id = UUID()
    let x: Int
    let y: Int
    let type: Int
}
