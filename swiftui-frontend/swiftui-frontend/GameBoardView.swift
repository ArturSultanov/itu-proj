//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

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

struct GemView: View {
    let iconType: IconType
    let isSelected: Bool

    var body: some View {
        Image(systemName: iconType.symbolName)
            .symbolRenderingMode(.palette)
            .foregroundStyle(iconType.color)
            .frame(width: 40, height: 40)
            .background(isSelected ? Color.yellow.opacity(0.3) : Color.clear)
            .clipShape(Circle())
            .overlay(
                Circle().stroke(Color.yellow, lineWidth: isSelected ? 2 : 0)
            )
    }
}



struct GameBoardView: View {
    @State var viewModel: GameViewModel = GameViewModel(boardStatus: initialBoardStatus)

    var body: some View {
        VStack {
            Text("Game Board")
                .font(.title)
                .padding()

            ForEach(0..<viewModel.boardStatus.count, id: \.self) { rowIndex in
                HStack {
                    ForEach(0..<viewModel.boardStatus[rowIndex].count, id: \.self) { colIndex in
                        let iconType = IconType.getGemIcon(for: viewModel.boardStatus[rowIndex][colIndex])
                        let isSelected = viewModel.selectedGem?.x == colIndex && viewModel.selectedGem?.y == rowIndex
                        GemView(iconType: iconType, isSelected: isSelected)
                            .onTapGesture {
                                viewModel.selectGem(at: (x: colIndex, y: rowIndex))
                            }
                    }
                }
            }
        }
    }
}



//struct ContentView: View {
//    @State private var viewModel = GameViewModel(boardStatus: initialBoardStatus)
//
//    var body: some View {
//        GameBoardView(viewModel: viewModel)
//    }
//}
//
//let initialBoardStatus: [[Int]] = [
//    [0, 1, 2, 3, 4],
//    [1, 2, 3, 4, 0],
//    [2, 3, 4, 0, 1],
//    [3, 4, 0, 1, 2],
//    [4, 0, 1, 2, 3]
//]



//struct GameBoardView: View {
//    var body: some View {
//        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)
//    }
//}
//
//#Preview {
//    GameBoardView()
//}



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

