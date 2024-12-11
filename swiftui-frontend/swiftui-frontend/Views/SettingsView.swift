//
//  SettingsView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct SettingsView: View {
    @Environment(PlayerDataManager.self) var playerDataManager // Access shared player data.
    @Environment(\.colorScheme) var colorScheme // Access current system theme (light/dark mode)

    @State private var showChangeLoginSheet = false // Controls the visibility of the change login sheet.
    @State private var newLogin: String = "" // Holds the new login value.
    @State private var showSwitchUserConfirmation = false // Controls the visibility of the switch user confirmation alert.
    @State private var navigateToLogin = false // Triggers navigation to the login view.
    @State private var showDifficultyOptions = false // Controls the visibility of the difficulty selection dialog.
    @State private var currentDifficulty: Int = 1 // Tracks the current difficulty level (default to Easy).
    @State private var isLoading = false // Indicates whether a task is currently loading.
    @State private var errorMessage: String? // Holds error messages for alerts.

    
    var body: some View {
        ZStack{
            VStack() {
                if isLoading {
                    ProgressView("Loading…")
                } else {
//                    Spacer()
                    
                        HStack {
                            Text("Current Difficulty: \(difficultyDescription(for: currentDifficulty))")
                                .font(.title2)
                                .fontWeight(.bold)
                                .padding(.trailing)
                            
                            Text("Current Login: \(playerDataManager.playerData!.login)")
                                .font(.title2)
                                .fontWeight(.bold)
                        }
                        .frame(maxWidth: .infinity, minHeight: 100, idealHeight: 200)
                        .background(colorScheme == .dark ? Color.gray.opacity(0.3) : Color.gray.opacity(0.2))
                        .cornerRadius(10)
                        .padding(.horizontal, 20)
                    
                    Button("Change Login") {
                        newLogin = playerDataManager.playerData?.login ?? ""
                        showChangeLoginSheet = true
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaPrimaryButton))
                    
                    Button("Switch User") {
                        showSwitchUserConfirmation = true
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaPrimaryButton))
                    
                    Button("Change Difficulty") {
                        showDifficultyOptions = true
                    }
                    .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaPrimaryButton))
                }
            }
            .padding([.leading, .trailing, .bottom], 20)
        }
        .alert("Error", isPresented: Binding<Bool>(
            get: { errorMessage != nil },
            set: { _ in errorMessage = nil }
        )) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(errorMessage ?? "")
        }
        .sheet(isPresented: $showChangeLoginSheet) {
            NavigationStack {
                Form {
                    Section(header: Text("Enter a new login:")) {
                        TextField("New Login", text: $newLogin)
                    }
                }
                .navigationTitle("Change Login")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") {
                            showChangeLoginSheet = false
                        }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            Task {
                                await changeLogin()
                            }
                        }
                    }
                }
            }
        }
        .confirmationDialog("Select Difficulty", isPresented: $showDifficultyOptions) {
            Button("Easy") { Task { await changeDifficulty(to: 1) } }
            Button("Normal") { Task { await changeDifficulty(to: 2) } }
            Button("Hard") { Task { await changeDifficulty(to: 3) } }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Choose your difficulty level")
        }
        .alert("Switch User?", isPresented: $showSwitchUserConfirmation) {
            VStack {
                Button("Yes") {
                    navigateToLogin = true
                }
                Button("No", role: .cancel) {
                    navigateToLogin = false
                }
            }
        } message: {
            Text("Are you sure you want to switch user?")
        }
        .navigationDestination(isPresented: $navigateToLogin) {
            LoginView()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .navigationTitle("Settings")
        .task {
            await loadCurrentDifficulty()
        }
    }
    
    // MARK: - Helper Functions

    /// Fetches the current difficulty from the backend
    private func loadCurrentDifficulty() async {
        isLoading = true
        do {
            let difficulty = try await NetworkManager.shared.getDifficulty()
            await MainActor.run {
                currentDifficulty = difficulty
                isLoading = false
            }
        } catch {
            await MainActor.run {
                errorMessage = "Failed to load current difficulty: \(error.localizedDescription)"
                isLoading = false
            }
        }
    }
    
    /// Updates the player's login in the backend
    private func changeLogin() async {
        isLoading = true
        do {
            try await NetworkManager.shared.updateLogin(newLogin: newLogin, playerDataManager: playerDataManager)
            isLoading = false
            showChangeLoginSheet = false
        } catch {
            isLoading = false
            errorMessage = "Failed to change login: \(error.localizedDescription)"
        }
    }
    
    /// Updates the difficulty level in the backend
    /// - Parameter difficulty: The new difficulty level
    private func changeDifficulty(to difficulty: Int) async {
        isLoading = true
        do {
            try await NetworkManager.shared.setDifficulty(difficulty, playerDataManager: playerDataManager)
            currentDifficulty = difficulty
            isLoading = false
        } catch {
            isLoading = false
            errorMessage = "Failed to change difficulty: \(error.localizedDescription)"
        }
    }
    
    /// Returns a human-readable description of the difficulty level
    /// - Parameter difficulty: The difficulty level as an integer
    /// - Returns: A string describing the difficulty level
    private func difficultyDescription(for difficulty: Int) -> String {
        switch difficulty {
        case 1: return "Easy"
        case 2: return "Normal"
        case 3: return "Hard"
        default: return "Unknown"
        }
    }
}
