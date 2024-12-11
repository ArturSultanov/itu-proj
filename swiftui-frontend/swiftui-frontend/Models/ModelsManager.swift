//
//  AppStateManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import Foundation
import SwiftUI
import Observation

/// Manages the player's data and updates game sessions in response to server interactions.
@Observable @MainActor class PlayerDataManager {
    var playerData: PlayerData?
    
    /// Updates the game session with the provided response from the server.
    /// - Parameter response: The server response containing the updated game state.
    func updateGameSession(with response: SwapResponse) {
        guard let playerData = playerData else { return }

        // Update highest score
        if response.currentScore > playerData.highestScore {
            playerData.highestScore = response.currentScore
        }
        // Update last game
        if let lastGame = playerData.lastGame {
            lastGame.currentScore = response.currentScore
            lastGame.movesLeft = response.movesLeft
            // Update board status
            for updatedGem in response.updatedGems {
                if lastGame.boardStatus.indices.contains(updatedGem.y),
                   lastGame.boardStatus[updatedGem.y].indices.contains(updatedGem.x) {
                    lastGame.boardStatus[updatedGem.y][updatedGem.x] = updatedGem.type
                }
            }
        }
    }
}

/// Represents the player's data from server
class PlayerData: Codable {
    var id: Int
    var login: String
    var highestScore: Int
    var lastGame: GameSession?
    var difficulty: Int?
}

/// Represents the details of a game session from server
class GameSession: Codable {
    var currentScore: Int
    var movesLeft: Int
    var boardStatus: [[Int]]
}

/// Represents a single gem on the game board.
@Observable class Gem: Identifiable, Codable, Equatable {
    @ObservationIgnored var id = UUID() // Unique identifier for SwiftUI's List
    var type: Int
    var x: Int
    var y: Int

    init(type: Int, x: Int, y: Int) {
        self.type = type
        self.x = x
        self.y = y
    }
    
    // Equatable conformance to compare gems by their unique IDs
    static func ==(lhs: Gem, rhs: Gem) -> Bool {
       return lhs.id == rhs.id
   }

    // Codable Conformance
    
    enum CodingKeys: String, CodingKey {
        case type
        case x
        case y
    }

    required convenience init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let type = try container.decode(Int.self, forKey: .type)
        let x = try container.decode(Int.self, forKey: .x)
        let y = try container.decode(Int.self, forKey: .y)
        self.init(type: type, x: x, y: y)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(type, forKey: .type)
        try container.encode(x, forKey: .x)
        try container.encode(y, forKey: .y)
    }
}

/// Represents the response from the server after a gem swap.
struct SwapResponse: Codable {
    let currentScore: Int
    let movesLeft: Int
    let updatedGems: [Gem]
}

/// Represents an entry in the leaderboard.
struct LeaderboardEntry: Codable, Identifiable {
    // Assign a unique ID for SwiftUI's List
    var id: UUID { UUID() }
    let login: String
    let highest_score: Int
}

/// Represents the possible directions for gem swapping.
enum Direction {
    case up, down, left, right
}
