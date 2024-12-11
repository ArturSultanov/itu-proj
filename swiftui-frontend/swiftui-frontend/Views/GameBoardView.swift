//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

// MARK: - Gameboard view
struct GameBoardView: View {
    @Environment(PlayerDataManager.self) var playerDataManager // Access shared player data.
    
    @State private var gems: [Gem] = [] // Array of gems displayed on the board.
    @State private var swapInProgress = false // Flag to prevent multiple swaps at the same time.
    
    private let gemSize: CGFloat = 50 // Size of each gem.
    private let gridSpacing: CGFloat = 2 // Spacing between gems.

    var body: some View {
        ZStack {
            VStack {
                Spacer()
                // Player metrics
                if let player = playerDataManager.playerData {
                    HStack {
                        Text("Current Score: \(player.lastGame!.currentScore)")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.trailing)
                        
                        Text("Moves Left: \(player.lastGame!.movesLeft)")
                            .font(.title2)
                            .fontWeight(.bold)
                    }
                    .frame(maxWidth: .infinity, minHeight: 100, idealHeight: 200)
                    .background(Color.tritanopiaPrimaryButton)
                    .cornerRadius(10)
                    .padding(.horizontal, 20)
                }
                    
                // Game board containing the gems
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
                        initializeGems() // Initialize the gems when the view appears.
                    }
                }
            }
            .padding([.leading, .trailing, .bottom], 20)
        }
        .navigationTitle("Game Board")
    }

    // MARK: - Positioning
    /// Calculates the position for a given gem on the board.
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
    /// Initializes the gems on the board based on the game's board status.
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
    /// Handles swapping a gem with an adjacent gem in the specified direction.
    private func handleSwapAction(gem: Gem, direction: Direction) {
        guard !swapInProgress, // Prevent multiple swaps at once.
              let targetGem = getAdjacentGem(for: gem, in: direction) else { return }
        swapInProgress = true

        withAnimation(.easeInOut) {
            swapPositions(gem, targetGem)
        }
        Task {
            do {
                try await NetworkManager.shared.swapGems(gem1: gem, gem2: targetGem, playerDataManager: playerDataManager)
                withAnimation(.easeInOut) {
                    initializeGems() // Refresh the board
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
    
    /// Reverts a swap if the server response indicates a failure.
    private func handleSwapFailure(_ gem: Gem, _ targetGem: Gem, statusCode: Int) {
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
                    initializeGems() // Refresh the board
                }
            } catch {
                print("Click gem failed: \(error)")
            }
        }
    }
}

