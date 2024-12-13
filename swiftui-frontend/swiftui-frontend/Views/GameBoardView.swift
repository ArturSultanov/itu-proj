//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

// MARK: - GameBoardView
struct GameBoardView: View {
    @Environment(PlayerDataManager.self) var playerDataManager // Access shared player data.
    @Environment(NetworkManager.self) var networkManager
    @Environment(\.colorScheme) var colorScheme // Access current system theme (light/dark mode)
    @Environment(\.dismiss) var dismiss // For navigation actions if needed

    @State private var gems: [Gem] = [] // Array of gems displayed on the board.
    @State private var swapInProgress = false // Prevent multiple swaps at once.
    @State private var showPauseMenu = false // Controls pause menu display
    @State private var isLoading = false // Loading state for shuffle or other actions
    @State private var errorMessage: String?
    @State private var isSettingsActive = false 

    private let gemSize: CGFloat = 50 // Size of each gem.
    private let gridSpacing: CGFloat = 2 // Spacing between gems.

    var body: some View {
        ZStack {
            VStack(spacing: 20) {
                Spacer()

                // Player metrics
                if let player = playerDataManager.playerData, let lastGame = player.lastGame {
                    HStack {
                        Text("Current Score: \(lastGame.currentScore)")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.trailing)

                        Text("Moves Left: \(lastGame.movesLeft)")
                            .font(.title2)
                            .fontWeight(.bold)
                    }
                    .frame(maxWidth: .infinity, minHeight: 100, idealHeight: 200)
                    .background(colorScheme == .dark ? Color.gray.opacity(0.3) : Color.gray.opacity(0.2))
                    .cornerRadius(10)
                    .padding(.horizontal, 20)
                }
                
                // Top Buttons: Shuffle & Pause
                HStack {
                    Button("Shuffle") {
                        Task {
                            await shuffleBoard()
                        }
                    }
                    .buttonStyle(MainMenuButtonStyle()) // or custom color if needed

                    Button("Pause") {
                        showPauseMenu = true
                    }
                    .buttonStyle(MainMenuButtonStyle())
                }
                .padding(.horizontal, 20)

                // Game board
                GeometryReader { geometry in
                    ZStack {
                        ForEach(gems) { gem in
                            GemView(
                                gem: gem,
                                iconType: IconType.getGemIcon(for: gem.type),
                                swapAction: { direction in handleSwapAction(gem: gem, direction: direction) },
                                clickAction: { gem in handleClickAction(gem: gem) }
                            )
                            .frame(width: gemSize, height: gemSize)
                            .position(position(for: gem, in: geometry.size))
                            .animation(.easeInOut, value: gems)
                        }
                    }
                    .onAppear {
                        initializeGems()
                    }
                }
                .padding(.bottom, 20)
            }
            .padding([.leading, .trailing], 20)

            if isLoading {
                Color.black.opacity(0.3)
                    .edgesIgnoringSafeArea(.all)
                ProgressView("Loading…")
                    .padding(40)
                    .background(Color.white)
                    .cornerRadius(10)
            }
        }
        .navigationTitle("Game Board")
        .alert("Error", isPresented: Binding<Bool>(
            get: { errorMessage != nil },
            set: { _ in errorMessage = nil }
        )) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(errorMessage ?? "")
        }
        .navigationDestination(isPresented: $isSettingsActive) {
            SettingsView() // Navigate to SettingsView
        }
        .confirmationDialog("Pause Menu", isPresented: $showPauseMenu) {
            Button("Resume", role: .cancel) {
                
            }
            Button("Settings") {
                isSettingsActive = true
            }
            Button("Quit Game", role: .destructive) {
                Task {
                    await quitGame()
                }
            }
        } message: {
            Text("Game is paused. What do you want to do?")
        }
    }

    // MARK: - Network Actions

    /// Sends request to shuffle the board and updates local state.
    private func shuffleBoard() async {
        isLoading = true
        do {
            let newBoardStatus = try await networkManager.shuffleBoard()
            await MainActor.run {
                // Update player's lastGame boardStatus
                if let player = playerDataManager.playerData, let lastGame = player.lastGame {
                    lastGame.boardStatus = newBoardStatus
                    player.lastGame = lastGame
                    playerDataManager.playerData = player
                }
                withAnimation(.easeInOut) {
                    initializeGems()
                }
                isLoading = false
            }
        } catch {
            await MainActor.run {
                errorMessage = "Failed to shuffle board: \(error.localizedDescription)"
                isLoading = false
            }
        }
    }

    /// Quits the game by calling network quit request and then dismissing.
    private func quitGame() async {
        do {
            try await networkManager.quitGame()
            await MainActor.run {
                // Dismiss current view and possibly go to login or main menu
                dismiss()
            }
        } catch {
            await MainActor.run {
                errorMessage = "Failed to quit game: \(error.localizedDescription)"
            }
        }
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
        gems = updatedGems
    }

    // MARK: - Actions
    private func handleSwapAction(gem: Gem, direction: Direction) {
        guard !swapInProgress,
              let targetGem = getAdjacentGem(for: gem, in: direction) else { return }
        
        swapInProgress = true
        
        withAnimation(.easeInOut) {
            swapPositions(gem, targetGem)
        }

        Task {
            do {
                try await networkManager.swapGems(gem1: gem, gem2: targetGem, playerDataManager: playerDataManager)
                initializeGems()
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
                try await networkManager.clickGem(gem: gem, playerDataManager: playerDataManager)
                initializeGems()
            } catch {
                print("Click gem failed: \(error)")
            }
        }
    }
}
