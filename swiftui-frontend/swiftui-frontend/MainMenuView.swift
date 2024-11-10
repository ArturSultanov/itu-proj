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
    @State private var isContunueGameActive: Bool = false
    @State private var isSettingsActive: Bool = false
    @State private var isLeaderboardActive: Bool = false
    
    var body: some View {
        ZStack{
            VStack{
                if let player = playerDataManager.playerData {
                    Text("Welcome, \(player.login)!")
                        .font(.title)
                    Text("Highest Score: \(player.highestScore)")
                        .font(.subheadline)
                }
                NavigationStack{
                    VStack(spacing: 20){
                        if let player = playerDataManager.playerData {
                            Text("Welcome, \(player.login)!")
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .cornerRadius(20)
                        }
                        
                        Button("New Game") {
                            Task {
                                await newGame()
                            }
                        }
                        .buttonStyle(.bordered)
                        .padding()
                        
                        Button(action: {}) {
                            Text("Continue")
                        }
                        
                        Button(action: {}) {
                            Text("Settings")
                        }
                        Button(action: {}) {
                            Text("Leader board")
                        }
                        Button(action: {}){
                            Text("Quit Game")
                        }
                        .buttonStyle(.bordered)
                        .padding()
                    }
                    .navigationTitle("Navigation")
                    .navigationDestination(isPresented: $isNewGameActive) {
                        GameBoardView()
                    }
                }
                .padding()
            }
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
}

