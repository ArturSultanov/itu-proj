//
//  NavigationManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

@Observable class NavigationManager {
    var path = NavigationPath()

    func navigateTo(_ destination: Destination) {
        path.append(destination)
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

enum Destination: Hashable {
    case loginScreen
    case mainMenu
    case newGame
    case settings
    case leaderBoard
}

