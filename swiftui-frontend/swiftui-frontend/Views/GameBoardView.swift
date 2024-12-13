//
//  GameBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

// MARK: - GameBoardView
struct GameBoardView: View {
    @Environment(PlayerDataManager.self) var playerDataManager  // Shared player data manager
    @Environment(NetworkManager.self) var networkManager        // Network action manager
    @Environment(BannerManager.self) var bannerManager          // Error banner manager
    @Environment(\.colorScheme) var colorScheme                 // Current system theme (light/dark mode)

    @State private var gems: [Gem] = []                         // Array of gems displayed on the board
    @State private var swapInProgress = false                   // Prevent multiple swaps at once.
    @State private var showPauseMenu = false                    // Controls pause menu display
    @State private var isLoading = false                        // State for loading animation while fetching data
    @State private var isSettingsActive = false                 // State to open Settings View
    @State private var isShowQuitConfirmation = false           // State to open Quit Game dialog

    private let gemSize: CGFloat = 50                           // Size of each gem.
    private let gridSpacing: CGFloat = 2                        // Spacing between gems.

    var body: some View {
        ZStack {
            VStack(spacing: 20) {
                Spacer()

                // MARK: - Player metrics
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
                
                // MARK: - top buttons: Shuffle and Pause
                HStack {
                    Button("Shuffle") {Task {await shuffleBoard()}}
                    .buttonStyle(MainMenuButtonStyle())

                    Button("Pause") {showPauseMenu = true}
                    .buttonStyle(MainMenuButtonStyle())
                }
                .padding(.horizontal, 20)

                // MARK: - Game board with gems
                GeometryReader { geometry in
                    ZStack {
                        // Display gems on the board
                        ForEach(gems) { gem in
                            GemView(
                                gem: gem,
                                iconType: IconType.getGemIcon(for: gem.type),   // Set the icon for gem
                                swapAction: { direction in handleSwapAction(gem: gem, direction: direction) },
                                clickAction: { gem in handleClickAction(gem: gem) }
                            )
                            .frame(width: gemSize, height: gemSize)
                            .position(position(for: gem, in: geometry.size))    // Calculate gem position
                            .animation(.easeInOut, value: gems)                 // Animate board changes
                        }
                    }
                    .onAppear {
                        initializeGems() // Initialize the board with gems
                    }
                }
                .padding(.bottom, 20)
            }
            .padding([.leading, .trailing], 20)
            if isLoading {ProgressView("Loading…")} // Show loading indicator
        }
        .navigationTitle("Game Board")
        .navigationDestination(isPresented: $isSettingsActive) {
            SettingsView() // Navigate to Settings View
        }
        .confirmationDialog("Pause Menu", isPresented: $showPauseMenu) {
            Button("Resume", role: .cancel) {} // Close the dialog
            Button("Settings") {
                isSettingsActive = true
            }
            Button("Quit Game", role: .destructive) {
                isShowQuitConfirmation = true
            }
        } message: {
            Text("Game is paused.") // Display a message in the pause dialog
        }
        .alert("Quit Game?", isPresented: $isShowQuitConfirmation) {
            VStack {
                Button("Yes") {
                    Task {
                        await quitGame() // Quit the game if the user confirms
                    }
                }
                Button("No", role: .cancel) {}
            }
        } message: {
            Text("Are you sure you want to quit the game?")
        }
        
    }

    // MARK: - Network Actions

    /// Sends request to shuffle the board and updates local state.
    private func shuffleBoard() async {
        isLoading = true
        do {
            let newBoardStatus = try await networkManager.shuffleBoard()
            await MainActor.run {
                // Update player lastGame boardStatus
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
            isLoading = false
            bannerManager.showError(message: "Failed to shuffle board: \(error.localizedDescription)")
        }
    }
    
    // MARK: - Quit game
    /// Terminates the application
    private func quitGame() async {
        await MainActor.run {
            NSApplication.shared.terminate(nil)
        }
    }

    // MARK: - Positioning
    /// Calculates the position of a gem based on its row and column
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
    /// Initializes the gems on the board based on the current board status
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
    /// Handles swapping a gem with its adjacent gem in the specified direction
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
                bannerManager.showError(message: "Swap failed: \(error)")
                swapInProgress = false
            }
        }
    }
    
    /// Reverts the gem positions if the server reports a failed swap
    private func handleSwapFailure(_ gem: Gem, _ targetGem: Gem, statusCode: Int) {
        if statusCode == 406 {
            withAnimation(.easeInOut) {
                swapPositions(gem, targetGem)
            }
        } else {
            bannerManager.showError(message: "Swap failed with status code: \(statusCode)")
        }
        swapInProgress = false
    }

    /// Swaps the positions of two gems in the array
    private func swapPositions(_ gem1: Gem, _ gem2: Gem) {
        let tempX = gem1.x
        let tempY = gem1.y
        gem1.x = gem2.x
        gem1.y = gem2.y
        gem2.x = tempX
        gem2.y = tempY
    }

    /// Finds the adjacent gem in the specified direction
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

    /// Handles the click action for a gem, particularly for hearts
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
