//
//  LoginView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct LoginView: View {
    @Environment(PlayerDataManager.self) var playerDataManager // Access shared player data manager
    @Environment(\.colorScheme) var colorScheme // Access current system theme (light/dark mode)

    @State private var loginInput: String = "" // Holds the user's input for the login
    @State private var isLoggedIn: Bool = false // Tracks whether the user has logged in
    @State private var isShowQuitConfirmation = false // Tracks whether the quit confirmation alert is shown
    
    var body: some View {
        ZStack {
            VStack {
                NavigationStack {
                    Text("Enter your name")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(Color.tritanopiaPrimaryButton)
                        .padding(.bottom, 20)
                    
                    TextField("Your login", text: $loginInput)
                        .padding()
                        .background(
                            (colorScheme == .dark ? Color.gray.opacity(0.3) : Color.gray.opacity(0.2))
                        )
                        .cornerRadius(10)
                        .shadow(radius: 5, x: 0, y: 3)
                        .padding(.horizontal, 20)
                    
                    Button("Confirm") {
                        Task {
                            await login() // Trigger the login asynchronously
                        }
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: loginInput == "" ? .gray : Color.tritanopiaBlue))
                    .disabled(loginInput == "")
                    
                    .navigationTitle("Welcome")
                    .navigationDestination(isPresented: $isLoggedIn) {
                        MainMenuView()}
                    
                    Button("Quit Game") {
                        isShowQuitConfirmation = true
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaRed))
                }
            }
            .padding([.leading, .trailing, .bottom], 20)
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
    
    func login() async {
        do {
            try await NetworkManager.shared.login(with: loginInput, playerDataManager: playerDataManager)
            isLoggedIn = true
        } catch {
            print("Login failed: \(error)")
        }
    }
    
    func quitGame() async {
        await MainActor.run {
            NSApplication.shared.terminate(nil)
        }
    }
}
