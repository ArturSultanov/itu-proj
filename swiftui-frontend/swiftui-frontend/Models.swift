//
//  AppStateManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import Foundation
import SwiftUI
import Observation

@Observable @MainActor class Player: Identifiable {
    var login: String = ""
    var isLoggedIn: Bool = false
    var highestScore: Int = 0
    var lastGame: LastGame?
    
}


class LastGame: Codable{
    var currentScore: Int = 0
    var movesLeft: Int = 0
    var boardStatus: [Int]?
}

class Gem: Identifiable, Codable{
    var color: Int?
    var position: GemPosition?
}

class GemPosition: Codable{
    var x: Int
    var y: Int
}




