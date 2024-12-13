//
//  LoginView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

// MARK: - Login view
struct LoginView: View {
    @Environment(PlayerDataManager.self) var playerDataManager  // Shared player data manager
    @Environment(NetworkManager.self) var networkManager        // Network action manager
    @Environment(BannerManager.self) var bannerManager          // Error banner manager
    @Environment(\.colorScheme) var colorScheme                 // Current system theme (light/dark mode)

    @State private var loginInput: String = ""                  // User input for the login
    @State private var isLoggedIn: Bool = false                 // Tracks if user is logged in
    @State private var isShowQuitConfirmation = false           // Tracks if quit confirmation alert to show
    
    var body: some View {
        ZStack {
            VStack {
                NavigationStack {
                    // MARK: Welcome header
                    Text("Enter your name")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(Color.tritanopiaPrimaryButton)
                        .padding(.bottom, 20)
                    
                    // MARK: Login text filed
                    TextField("Your login", text: $loginInput)
                        .padding()
                        .background(
                            (colorScheme == .dark ? Color.gray.opacity(0.3) : Color.gray.opacity(0.2))
                        )
                        .cornerRadius(10)
                        .shadow(radius: 5, x: 0, y: 3)
                        .padding(.horizontal, 20)
                    
                    // MARK: Confirm button
                    Button("Confirm") {
                        Task {
                            await login() // Trigger the login asynchronously
                        }
                    }
                    .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
                        palette.teal
                    }))
                    .disabled(loginInput.isEmpty)
                    
                    // MARK: Quit Game button
                    Button("Quit Game") {
                        isShowQuitConfirmation = true
                    }
                    .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
                        palette.red
                    }))
                    
                    .navigationTitle("Welcome")
                    .navigationDestination(isPresented: $isLoggedIn) {
                        MainMenuView()}
                }
            }
        }
        .alert("Quit Game?", isPresented: $isShowQuitConfirmation) {
            VStack {
                Button("Yes") {Task {await quitGame()}}
                Button("No", role: .cancel) {}
            }
        } message: {
            Text("Are you sure you want to quit the game?")
        }
    }
    
    // MARK: - Helper functions
    private func login() async {
        do {
            try await networkManager.login(with: loginInput, playerDataManager: playerDataManager)
            isLoggedIn = true
        } catch {
            bannerManager.showError(message: "Login failed: \(error)")
        }
    }
    
    private func quitGame() async {
        await MainActor.run {
            NSApplication.shared.terminate(nil)
        }
    }
    
}
