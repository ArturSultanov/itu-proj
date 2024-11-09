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
}

class PlayerData: Codable {
    var id: Int
    var login: String
    var highestScore: Int
    var lastGame: GameSession?
}

struct GameSession: Codable {
    let currentScore: Int
    let movesLeft: Int
    let boardStatus: [[Int]]
}


class Gem: Identifiable, Codable{
    var color: Int?
    var position: GemPosition?
}

class GemPosition: Codable{
    var x: Int
    var y: Int
}

