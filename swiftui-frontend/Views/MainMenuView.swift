//
//  MainMenuView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI


// MARK: - Main menu view
struct MainMenuView: View {
    @Environment(PlayerDataManager.self) var playerDataManager  // Shared player data manager
    @Environment(NetworkManager.self) var networkManager        // Network action manager
    @Environment(BannerManager.self) var bannerManager          // Error banner manager
    @Environment(\.colorScheme) var colorScheme                 // Current system theme (light/dark mode)

    // States to track which view should be opened
    @State private var isNewGameActive: Bool = false
    @State private var isContinueGameActive: Bool = false
    @State private var isContunueGameActive: Bool = false
    @State private var isSettingsActive: Bool = false
    @State private var isLeaderboardActive: Bool = false
    // States to track which dialog should be opened
    @State private var isShowQuitConfirmation = false
    @State private var isShowDeleteGameConfirmation = false

    var body: some View {
        ZStack {
            VStack {
                playerInfoView
                menuButtonsView
            }
        }
        .navigationTitle("Main Menu")
        .navigationDestination(isPresented: $isNewGameActive) {
            GameBoardView()
        }
        .navigationDestination(isPresented: $isContinueGameActive) {
            GameBoardView()
        }
        .navigationDestination(isPresented: $isLeaderboardActive) {
            LeaderboardView()
        }
        .navigationDestination(isPresented: $isSettingsActive) {
            SettingsView()
        }
        .quitGameAlert(isPresented: $isShowQuitConfirmation) {
            Task { await quitGame() }
        }
        .deleteGameAlert(isPresented: $isShowDeleteGameConfirmation) {
            Task { await deleteLastGame() }
        }
    }
    
    // MARK: - Welcome banner and user info
    private var playerInfoView: some View {
        // Safely unwrap playerData
        let login = playerDataManager.playerData?.login ?? "Unknown"
        let highestScore = playerDataManager.playerData?.highestScore ?? 0
        
        let backgroundColor = (colorScheme == .dark)
            ? Color.gray.opacity(0.3)
            : Color.gray.opacity(0.2)
        
        return VStack {
            Text("Hi, \(login)!")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding(.bottom, 20)
            
            Text("Your highest score: \(highestScore)")
                .font(.title2)
                .fontWeight(.semibold)
        }
        .frame(maxWidth: .infinity, minHeight: 100, idealHeight: 200)
        .background(backgroundColor)
        .cornerRadius(10)
        .padding(.horizontal, 20)
    }

    // MARK: - Buttons of the main menu
    private var menuButtonsView: some View {
        VStack {
            Button("New Game") {
                Task { await newGame() }
            }
            .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
                palette.teal
            }))
            
            HStack {
                Button("                              Continue") { // Adding spaces for better layout
                    Task { await continueGame() }
                }
                .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
                    palette.teal
                }))
                .disabled(playerDataManager.playerData?.lastGame == nil)
                
                Button(action: {
                    isShowDeleteGameConfirmation = true
                }) {
                    Image(systemName: "trash")
                }
                .buttonStyle(SecondaryMenuButtonStyle(customColorProvider: { palette in
                    palette.red
                }))
                .disabled(playerDataManager.playerData?.lastGame == nil)
            }
            .frame(maxWidth: .infinity, alignment: .center)
            .padding(.vertical, 1)
            
            Button("Settings") {
                isSettingsActive = true
            }
            .buttonStyle(MainMenuButtonStyle())
            
            Button("Leader board") {
                isLeaderboardActive = true
            }
            .buttonStyle(MainMenuButtonStyle())
            
            Button("Quit Game") {
                isShowQuitConfirmation = true
            }
            .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
                palette.red
            }))
        }
    }

    // MARK: - networkManage functions
    private func newGame() async {
        do {
            try await networkManager.newGame(playerDataManager: playerDataManager)
            isNewGameActive = true
        } catch {
            bannerManager.showError(message: "Failed to start new game: \(error.localizedDescription)")
        }
    }
    
    private func continueGame() async {
        do {
            try await networkManager.continue_game(playerDataManager: playerDataManager)
            isContinueGameActive = true
        } catch {
            bannerManager.showError(message: "Failed to continue game: \(error.localizedDescription)")
        }
    }
    
    private func quitGame() async {
        do {
            try await networkManager.quitGame()
        } catch {
            bannerManager.showError(message: "Failed: \(error.localizedDescription)")
        }
        await MainActor.run {
            NSApplication.shared.terminate(nil)
        }
    }
    
    private func deleteLastGame() async {
        do {
            try await networkManager.deleteGame(playerDataManager: playerDataManager)
        } catch {
            bannerManager.showError(message: "Failed to delete last game: \(error.localizedDescription)")
        }
    }
}

// MARK: - View for alerts

private extension View {
    func quitGameAlert(isPresented: Binding<Bool>, quitAction: @escaping () -> Void) -> some View {
        self.alert("Quit Game?", isPresented: isPresented) {
            VStack {
                Button("Yes", action: quitAction)
                Button("No", role: .cancel) {}
            }
        } message: {
            Text("Are you sure you want to quit the game?")
        }
    }

    func deleteGameAlert(isPresented: Binding<Bool>, deleteAction: @escaping () -> Void) -> some View {
        self.alert("Delete Last Game?", isPresented: isPresented) {
            VStack {
                Button("Yes", action: deleteAction)
                Button("No", role: .cancel) {}
            }
        } message: {
            Text("Are you sure you want to delete the last game?")
        }
    }

    func errorAlert(errorMessage: Binding<String?>, isShowErrorAlert: Binding<Bool>) -> some View {
        self.alert("Error", isPresented: isShowErrorAlert) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(errorMessage.wrappedValue ?? "Unknown Error")
        }
    }
}
