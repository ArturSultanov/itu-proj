//
//  AppStateManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import Foundation
import SwiftUI
import Observation

@Observable @MainActor class PlayerDataManager {
    var playerData: PlayerData?
    
    func updateGameSession(with response: SwapResponse) {
        guard var lastGame = playerData?.lastGame else { return }
        
        lastGame.currentScore = response.currentScore
        lastGame.movesLeft = response.movesLeft
        
        for updatedGem in response.updatedGems {
            if lastGame.boardStatus.indices.contains(updatedGem.y),
               lastGame.boardStatus[updatedGem.y].indices.contains(updatedGem.x) {
                lastGame.boardStatus[updatedGem.y][updatedGem.x] = updatedGem.type
            }
        }
    }
}

class PlayerData: Codable {
    var id: Int
    var login: String
    var highestScore: Int
    var lastGame: GameSession?
}

struct GameSession: Codable {
    var currentScore: Int
    var movesLeft: Int
    var boardStatus: [[Int]]
}


class Gem: Identifiable, Codable{
    var type: Int
    var x: Int
    var y: Int
}

struct SwapResponse: Codable {
    let currentScore: Int
    let movesLeft: Int
    let updatedGems: [Gem]
}
