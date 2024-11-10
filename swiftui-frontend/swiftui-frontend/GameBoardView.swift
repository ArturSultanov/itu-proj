//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//
// GameBoardView.swift
import SwiftUI

import SwiftUI

struct GameBoardView: View {
    @Environment(PlayerDataManager.self) var playerDataManager

    @State private var gems: [Gem] = []
    @State private var swapInProgress = false
    
    let gemSize: CGFloat = 50
    let gridSpacing: CGFloat = 2

    var body: some View {
        VStack {
            if let lastGame = playerDataManager.playerData?.lastGame {
                Text("Score: \(lastGame.currentScore)")
                    .font(.headline)
                Text("Moves Left: \(lastGame.movesLeft)")
                    .font(.subheadline)
            }
            GeometryReader { geometry in
                ZStack {
                    ForEach(gems) { gem in
                        GemView(gem: gem, swapAction: { direction in
                            handleSwapAction(gem: gem, direction: direction)
                        })
                        .frame(width: gemSize, height: gemSize)
                        .position(position(for: gem, in: geometry.size))
                    }
                }
                .onAppear {
                    initializeGems()
                }
            }
        }
    }
    
    func position(for gem: Gem, in size: CGSize) -> CGPoint {
        let numRows = playerDataManager.playerData?.lastGame?.boardStatus.count ?? 0
        let numCols = playerDataManager.playerData?.lastGame?.boardStatus.first?.count ?? 0
        
        let totalWidth = CGFloat(numCols) * (gemSize + gridSpacing) - gridSpacing
        let totalHeight = CGFloat(numRows) * (gemSize + gridSpacing) - gridSpacing
        
        let startX = (size.width - totalWidth) / 2 + gemSize / 2
        let startY = (size.height - totalHeight) / 2 + gemSize / 2
        
        let xPosition = startX + CGFloat(gem.x) * (gemSize + gridSpacing)
        let yPosition = startY + CGFloat(gem.y) * (gemSize + gridSpacing)
        
        return CGPoint(x: xPosition, y: yPosition)
    }
    
//    func initializeGems() {
//        if let boardStatus = playerDataManager.playerData?.lastGame?.boardStatus {
//            if gems.isEmpty {
//                // Initialize gems array
//                gems = []
//                for (rowIndex, row) in boardStatus.enumerated() {
//                    for (colIndex, type) in row.enumerated() {
//                        let gem = Gem(type: type, x: colIndex, y: rowIndex)
//                        gems.append(gem)
//                    }
//                }
//            } else {
//                // Update existing gems
//                for gem in gems {
//                    if let type = playerDataManager.playerData?.lastGame?.boardStatus[gem.y][gem.x] {
//                        gem.type = type
//                    }
//                }
//            }
//        }
//    }
    
    func initializeGems() {
        if let boardStatus = playerDataManager.playerData?.lastGame?.boardStatus {
            // Clear existing gems and recreate them based on the updated boardStatus
            gems = []
            for (rowIndex, row) in boardStatus.enumerated() {
                for (colIndex, type) in row.enumerated() {
                    if let existingGem = gems.first(where: { $0.x == colIndex && $0.y == rowIndex }) {
                        existingGem.type = type
                    } else {
                        let gem = Gem(type: type, x: colIndex, y: rowIndex)
                        gems.append(gem)
                    }
                }
            }
        }
    }

    
    func handleSwapAction(gem: Gem, direction: Direction) {
        if swapInProgress { return }
        guard let targetGem = getAdjacentGem(for: gem, in: direction) else { return }
        swapInProgress = true

        // Swap gems in the array
        withAnimation {
            // Swap positions
            let tempX = gem.x
            let tempY = gem.y
            gem.x = targetGem.x
            gem.y = targetGem.y
            targetGem.x = tempX
            targetGem.y = tempY
        }
        
        // Send swap request to server
        Task {
            do {
                try await NetworkManager.shared.swapGems(gem1: gem, gem2: targetGem, playerDataManager: playerDataManager)
                
                // Update the gems based on response
                initializeGems()
                swapInProgress = false
            } catch let NetworkError.invalidResponse(statusCode) {
                if statusCode == 406 {
                    // No matches found, swap back
                    withAnimation {
                        let tempX = gem.x
                        let tempY = gem.y
                        gem.x = targetGem.x
                        gem.y = targetGem.y
                        targetGem.x = tempX
                        targetGem.y = tempY
                    }
                    swapInProgress = false
                } else {
                    print("Swap failed with status code: \(statusCode)")
                    swapInProgress = false
                }
            } catch {
                print("Swap failed: \(error)")
                swapInProgress = false
            }
        }
    }
    
    func getAdjacentGem(for gem: Gem, in direction: Direction) -> Gem? {
        let x = gem.x
        let y = gem.y
        switch direction {
        case .up:
            return gems.first(where: { $0.x == x && $0.y == y - 1 })
        case .down:
            return gems.first(where: { $0.x == x && $0.y == y + 1 })
        case .left:
            return gems.first(where: { $0.x == x - 1 && $0.y == y })
        case .right:
            return gems.first(where: { $0.x == x + 1 && $0.y == y })
        }
    }
}

enum Direction {
    case up, down, left, right
}
