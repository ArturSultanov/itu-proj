//
//  MainMenuView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct MainMenuView: View {
    @Environment(PlayerDataManager.self) var playerDataManager
    @Environment(\.colorScheme) var colorScheme // Access current system theme (light/dark mode)

    // State variables to track view navigation and alerts.
    @State private var isNewGameActive: Bool = false
    @State private var isContinueGameActive: Bool = false
    @State private var isContunueGameActive: Bool = false
    @State private var isSettingsActive: Bool = false
    @State private var isLeaderboardActive: Bool = false
    @State private var isShowQuitConfirmation = false
    @State private var isShowErrorAlert = false
    @State private var isShowDeleteGameConfirmation = false
    @State private var isDisableContinue = true
    @State private var errorMessage: String?

    
    var body: some View {
        ZStack{
            VStack{
                if let player = playerDataManager.playerData {
                    VStack {
                        Text("Hi, \(player.login)!")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .padding(.bottom, 20)
                        
                        Text("Your highest score: \(playerDataManager.playerData!.highestScore)")
                            .font(.title2)
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity, minHeight: 100, idealHeight: 200)
                    .background(colorScheme == .dark ? Color.gray.opacity(0.3) : Color.gray.opacity(0.2))
                    .cornerRadius(10)
                    .padding(.horizontal, 20)
                    
                }
                VStack(){
                    Button("New Game") {
                        Task {
                            await newGame()
                        }
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaBlue))
                    
                    HStack {
                        Button("Continue") {
                            Task {
                                await continueGame()
                            }
                        }
                        .buttonStyle(MainMenuButtonStyle(mainColor: playerDataManager.playerData?.lastGame == nil ? .gray : Color.tritanopiaBlue))
                        .disabled(playerDataManager.playerData?.lastGame == nil)

                        // Trash Icon
                        Button(action: {
                            isShowDeleteGameConfirmation = true
                        }) {
                            Image(systemName: "trash")
                        }
                        .buttonStyle(SecondaryMenuButtonStyle(mainColor: playerDataManager.playerData?.lastGame == nil ? .gray : Color.tritanopiaRed))
                        .disabled(playerDataManager.playerData?.lastGame == nil)

                    }
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding(.vertical, 1)

                    Button(action: {
                        isSettingsActive = true
                    }) {
                        Text("Settings")
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaPrimaryButton))
                    
                    Button(action: {
                        isLeaderboardActive = true
                    }) {
                        Text("Leader board")
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaPrimaryButton))
                    
                    Button("Quit Game") {
                        isShowQuitConfirmation = true
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaRed))
                }
            }
            .padding([.leading, .trailing, .bottom], 20)
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
        .alert("Quit Game?", isPresented: $isShowQuitConfirmation) {
            VStack {
                Button("Yes") {
                    Task {
                        await quitGame()
                    }
                }
                Button("No", role: .cancel) {}
            }
        } message: {
            Text("Are you sure you want to quit the game?")
        }
        .alert("Delete Last Game?", isPresented: $isShowDeleteGameConfirmation) {
            VStack {
                Button("Yes") {
                    Task {
                        await deleteLastGame()
                    }
                }
                Button("No", role: .cancel) {}
            }
        } message: {
            Text("Are you sure you want to delete the last game?")
        }
    }
    
    // MARK: - Actions

    /// Starts a new game and navigates to the game board
    func newGame() async {
        do {
            try await NetworkManager.shared.newGame(playerDataManager: playerDataManager)
            isNewGameActive = true
        } catch {
            print("Failed to start new game: \(error)")
        }
    }
    
    /// Continues the last game and navigates to the game board
    func continueGame() async {
        do {
            try await NetworkManager.shared.continue_game(playerDataManager: playerDataManager)
            isContinueGameActive = true
        } catch {
            print("Failed to start new game: \(error)")
        }
    }
    
    /// Quits the game by sending a request to the backend and terminating the app
    func quitGame() async {
        do {
            try await NetworkManager.shared.quitGame()
            await MainActor.run {
                NSApplication.shared.terminate(nil)
            }
        } catch {
            errorMessage = "Failed to quit game: \(error.localizedDescription)"
            isShowErrorAlert = true
        }
    }
    
    /// Deletes the last game session
    func deleteLastGame() async {
        do {
            try await NetworkManager.shared.deleteGame(playerDataManager: playerDataManager)
        } catch {
            errorMessage = "Failed to delete last game: \(error.localizedDescription)"
            isShowErrorAlert = true
        }
    }
}
