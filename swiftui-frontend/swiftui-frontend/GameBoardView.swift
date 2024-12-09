//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//
// GameBoardView.swift

import SwiftUI

struct GameBoardView: View {
    @Environment(PlayerDataManager.self) var playerDataManager

    @State private var gems: [Gem] = []
    @State private var swapInProgress = false
    
    private let gemSize: CGFloat = 50
    private let gridSpacing: CGFloat = 2

    var body: some View {
        ZStack {
            VStack {
                // Player metrics
                if let playerData = playerDataManager.playerData,
                   let lastGame = playerData.lastGame {
                    gameMetricsView(lastGame: lastGame)
                }

                GeometryReader { geometry in
                    ZStack {
                        ForEach(gems) { gem in
                            GemView(
                                gem: gem,
                                swapAction: { direction in handleSwapAction(gem: gem, direction: direction) },
                                clickAction: { gem in handleClickAction(gem: gem) }
                            )
                            .frame(width: gemSize, height: gemSize)
                            .position(position(for: gem, in: geometry.size))
                            .animation(.easeInOut, value: gems) // Animate gem layout changes
                        }
                    }
                    .onAppear {
                        initializeGems()
                    }
                }
            }
            .aspectRatio(1, contentMode: .fit)
            .padding([.leading, .trailing, .bottom], 20)
        }
        .navigationTitle("Game Board")
    }

    // MARK: - Subviews

    private func gameMetricsView(lastGame: GameSession) -> some View {
        HStack {
            Text("Current Score: \(lastGame.currentScore)")
                .font(.title2)
                .fontWeight(.bold)
                .padding(.trailing)

            Text("Moves Left: \(lastGame.movesLeft)")
                .font(.title2)
                .fontWeight(.bold)
        }
        .frame(maxWidth: .infinity, minHeight: 100)
        .background(Color.blue)
        .cornerRadius(10)
    }

    // MARK: - Positioning

    private func position(for gem: Gem, in size: CGSize) -> CGPoint {
        guard let rows = playerDataManager.playerData?.lastGame?.boardStatus.count,
              let cols = playerDataManager.playerData?.lastGame?.boardStatus.first?.count else {
            return .zero
        }

        let totalWidth = CGFloat(cols) * (gemSize + gridSpacing) - gridSpacing
        let totalHeight = CGFloat(rows) * (gemSize + gridSpacing) - gridSpacing
        
        let startX = (size.width - totalWidth) / 2 + gemSize / 2
        let startY = (size.height - totalHeight) / 2 + gemSize / 2
        
        let xPos = startX + CGFloat(gem.x) * (gemSize + gridSpacing)
        let yPos = startY + CGFloat(gem.y) * (gemSize + gridSpacing)
        
        return CGPoint(x: xPos, y: yPos)
    }

    // MARK: - Initialization & Updates

    private func initializeGems() {
        guard let boardStatus = playerDataManager.playerData?.lastGame?.boardStatus else { return }

        var updatedGems: [Gem] = []
        for (rowIndex, row) in boardStatus.enumerated() {
            for (colIndex, type) in row.enumerated() {
                let gem = Gem(type: type, x: colIndex, y: rowIndex)
                updatedGems.append(gem)
            }
        }

        withAnimation(.easeInOut) {
            gems = updatedGems
        }
    }

    // MARK: - Actions

    private func handleSwapAction(gem: Gem, direction: Direction) {
        guard !swapInProgress,
              let targetGem = getAdjacentGem(for: gem, in: direction) else { return }
        
        swapInProgress = true
        
        // Animate the initial swap optimistically
        withAnimation(.easeInOut) {
            swapPositions(gem, targetGem)
        }

        Task {
            do {
                try await NetworkManager.shared.swapGems(gem1: gem, gem2: targetGem, playerDataManager: playerDataManager)
                withAnimation(.easeInOut) {
                    initializeGems()
                }
                swapInProgress = false
            } catch let NetworkError.invalidResponse(statusCode) {
                handleSwapFailure(gem, targetGem, statusCode: statusCode)
            } catch {
                print("Swap failed: \(error)")
                swapInProgress = false
            }
        }
    }

    private func handleSwapFailure(_ gem: Gem, _ targetGem: Gem, statusCode: Int) {
        // If no matches found, revert swap
        if statusCode == 406 {
            withAnimation(.easeInOut) {
                swapPositions(gem, targetGem)
            }
        } else {
            print("Swap failed with status code: \(statusCode)")
        }
        swapInProgress = false
    }

    private func swapPositions(_ gem1: Gem, _ gem2: Gem) {
        let tempX = gem1.x
        let tempY = gem1.y
        gem1.x = gem2.x
        gem1.y = gem2.y
        gem2.x = tempX
        gem2.y = tempY
    }

    private func getAdjacentGem(for gem: Gem, in direction: Direction) -> Gem? {
        let x = gem.x
        let y = gem.y
        
        switch direction {
        case .up:
            return gems.first { $0.x == x && $0.y == y - 1 }
        case .down:
            return gems.first { $0.x == x && $0.y == y + 1 }
        case .left:
            return gems.first { $0.x == x - 1 && $0.y == y }
        case .right:
            return gems.first { $0.x == x + 1 && $0.y == y }
        }
    }

    private func handleClickAction(gem: Gem) {
        let iconType = IconType.getGemIcon(for: gem.type)
        guard iconType == .heart else { return }
        
        Task {
            do {
                try await NetworkManager.shared.clickGem(gem: gem, playerDataManager: playerDataManager)
                withAnimation(.easeInOut) {
                    initializeGems()
                }
            } catch {
                print("Click gem failed: \(error)")
            }
        }
    }
}

enum Direction {
    case up, down, left, right
}
