//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI


import SwiftUI

@Observable class GameViewModel {
    var boardStatus: [[Int]]
    var selectedGem: (x: Int, y: Int)?

    init(boardStatus: [[Int]]) {
        self.boardStatus = boardStatus
    }

    func selectGem(at position: (x: Int, y: Int)) {
        if let firstSelection = selectedGem {
            if areAdjacent(firstSelection, position) {
                swapGems(firstSelection, position)
                selectedGem = nil
            } else {
                selectedGem = position
            }
        } else {
            selectedGem = position
        }
    }

    private func areAdjacent(_ first: (x: Int, y: Int), _ second: (x: Int, y: Int)) -> Bool {
        let dx = abs(first.x - second.x)
        let dy = abs(first.y - second.y)
        return (dx == 1 && dy == 0) || (dx == 0 && dy == 1)
    }

    private func swapGems(_ first: (x: Int, y: Int), _ second: (x: Int, y: Int)) {
        let temp = boardStatus[first.y][first.x]
        boardStatus[first.y][first.x] = boardStatus[second.y][second.x]
        boardStatus[second.y][second.x] = temp
    }
}



struct GameBoardView: View {
    var body: some View {
        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)
    }
}

#Preview {
    GameBoardView()
}



enum IconType: CaseIterable, Equatable {
    case triangle
    case circle
    case square
    case diamond
    case heart

    var color: Color {
        switch self {
        case .triangle: return .purple
        case .circle: return .pink
        case .square: return .orange
        case .diamond: return .yellow
        case .heart: return .red
        }
    }

    var symbolName: String {
        switch self {
        case .triangle: return "triangle.fill"
        case .circle: return "circle.fill"
        case .square: return "square.fill"
        case .diamond: return "diamond.fill"
        case .heart: return "heart.fill"
        }
    }

    static func getGemIcon(for typeIndex: Int) -> IconType {
        let allCases = Array(Self.allCases)
        return allCases[typeIndex % allCases.count]
    }
}

