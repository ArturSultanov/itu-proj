//
//  MainMenuView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct MainMenuView: View {
    @Environment(PlayerDataManager.self) var playerDataManager
    
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
                    .background(Color.tritanopiaTeal)
                    .cornerRadius(10)
                    .padding(.horizontal, 20)
                    
                    
                }
                VStack{
                    Button("New Game") {
                        Task {
                            await newGame()
                        }
                    }
                    .buttonStyle(MainMenuButtonStyle(secondColor: Color.tritanopiaPrimaryButton))
                    
//                    Button("Continue") {
//                        Task {
//                            await continueGame()
//                        }
//                    }
//                    .buttonStyle(MainMenuButtonStyle(secondColor: Color.tritanopiaPrimaryButton))
//                    
                    // Continue + Delete Button
                    HStack {
                        // Continue Button
                        Button("Continue") {
                            Task {
                                await continueGame()
                            }
                        }
                        .buttonStyle(MainMenuButtonStyle(secondColor: playerDataManager.playerData?.lastGame == nil ? .gray : Color.tritanopiaPrimaryButton))
                        .disabled(playerDataManager.playerData?.lastGame == nil)

                        // Trash Icon
                        Button(action: {
                            isShowDeleteGameConfirmation = true
                        }) {
                            Image(systemName: "trash")
                                .padding(.leading, 10)
                        }
                        .buttonStyle(PlainButtonStyle())
                        .disabled(playerDataManager.playerData?.lastGame == nil)
                        .foregroundColor(playerDataManager.playerData?.lastGame == nil ? .gray : .red)
                    }

                    
                    Button(action: {
                        isSettingsActive = true
                    }) {
                        Text("Settings")
                    }
                    .buttonStyle(MainMenuButtonStyle(secondColor: Color.tritanopiaPrimaryButton))
                    
                    Button(action: {
                        isLeaderboardActive = true
                    }) {
                        Text("Leader board")
                    }
                    .buttonStyle(MainMenuButtonStyle(secondColor: Color.tritanopiaPrimaryButton))
                    
                    
                    Button("Quit Game") {
                        isShowQuitConfirmation = true
                    }
                    .buttonStyle(MainMenuButtonStyle(secondColor: Color.tritanopiaRed))
                }
            }
            .aspectRatio(1, contentMode: .fit)
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
    
    func newGame() async {
        
        do {
            try await NetworkManager.shared.newGame(playerDataManager: playerDataManager)
            isNewGameActive = true
        } catch {
            print("Failed to start new game: \(error)")
        }
    }
    
    func continueGame() async {
        
        do {
            try await NetworkManager.shared.continue_game(playerDataManager: playerDataManager)
            isContinueGameActive = true
        } catch {
            print("Failed to start new game: \(error)")
        }
    }
    
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
    
    func deleteLastGame() async {
        do {
            try await NetworkManager.shared.deleteGame(playerDataManager: playerDataManager)
        } catch {
            errorMessage = "Failed to delete last game: \(error.localizedDescription)"
            isShowErrorAlert = true
        }
    }


}

struct MainMenuButtonStyle: ButtonStyle {
    var secondColor : Color
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity, minHeight: 50)
//            .background(
//                LinearGradient(
//                    gradient: Gradient(colors: [secondColor, Color.purple]),
//                    startPoint: .leading,
//                    endPoint: .trailing
//                )
//            )
            .background(secondColor)
            .foregroundColor(.white)
            .font(.headline)
            .cornerRadius(10)
            .shadow(radius: configuration.isPressed ? 2 : 5, x: 0, y: configuration.isPressed ? 1 : 3)
            .padding(.horizontal, 20)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}
