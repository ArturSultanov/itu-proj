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
                    
                    Button("Continue") {
                        Task {
                            await continueGame()
                        }
                    }
                    .buttonStyle(MainMenuButtonStyle(secondColor: Color.tritanopiaPrimaryButton))
                    
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
                    
                    
                    Button(action: {}){
                        Text("Quit Game")
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
    
    
//    func leaderBoard() async{
//        do {
//            // TODO: create a function to show a leader board
//        }
//    }
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
