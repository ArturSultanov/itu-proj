//
//  DataModels.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.11.2024.
//

import Foundation

// MARK: - User Data Model
struct User: Codable {
    let login: String
    let id: Int
    let highestScore: Int
    let lastGame: Game?

}

// MARK: - Game Data Model
struct Game: Codable {
    var currentScore: Int
    var movesLeft: Int
    var boardStatus: [[Int]]?

    enum CodingKeys: String, CodingKey {
        case currentScore = "current_score"
        case movesLeft = "moves_left"
        case boardStatus = "board_status"
    }
}

// MARK: - Gem Swap Request Model
struct SwapGemsRequest: Codable {
    let gems: [GemPosition]
}

// MARK: - Gem Position Model
struct GemPosition: Codable {
    let x: Int
    let y: Int
}

// MARK: - Gem Update Model
struct GemUpdate: Codable {
    let x: Int
    let y: Int
    let type: Int
}

// MARK: - Swap Gems Response Model
struct SwapGemsResponse: Codable {
    let currentScore: Int
    let movesLeft: Int
    let updatedGems: [GemUpdate]
}
