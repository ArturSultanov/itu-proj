//
//  SettingsView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

// MARK: - Settings view
struct SettingsView: View {
    @Environment(PlayerDataManager.self) var playerDataManager  // Shared player data manager
    @Environment(NetworkManager.self) var networkManager        // Network action manager
    @Environment(BannerManager.self) var bannerManager          // Error banner manager
    @Environment(PaletteManager.self) var paletteManager        // Color palette manager
    @Environment(\.colorScheme) var colorScheme                 // Current system theme (light/dark mode)
    
    @State private var showChangeLoginSheet = false             // State to show the change login for current user dialog
    @State private var newLogin: String = ""                    // String to keep a new login

    @State private var showSwitchUserConfirmation = false       // State to show the switch user dialog
    @State private var navigateToLogin = false                  // State to navigate to to Login View

    @State private var showDifficultyOptions = false            // State to open the change difficulty dialog
    @State private var currentDifficulty: Int = 1               // State to display the current difficulty level
    @State private var isLoading = false                        // State for loading animation while fetching data

    var body: some View {
        ZStack {
            mainContent
        }
        .applyChangeLoginSheet(
            isPresented: $showChangeLoginSheet,
            newLogin: $newLogin,
            changeLoginAction: { await changeLogin() }
        )
        .applyDifficultyConfirmationDialog(
            isPresented: $showDifficultyOptions,
            changeDifficultyAction: { difficulty in Task { await changeDifficulty(to: difficulty) } }
        )
        .applySwitchUserAlert(
            isPresented: $showSwitchUserConfirmation,
            navigateToLogin: $navigateToLogin
        )
        .navigationDestination(isPresented: $navigateToLogin) {
            LoginView()
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .navigationTitle("Settings")
        .task {
            await loadCurrentDifficulty()
        }
    }

    // Extracted main content into a computed property to reduce complexity.
    var mainContent: some View {
        VStack {
            if isLoading {
                ProgressView("Loading…")
            } else {
                topInfoView
                switchColorPaletteButton
                changeLoginButton
                changeDifficultyButton
                switchUserButton
            }
        }
    }

    var topInfoView: some View {
        let backgroundColor = (colorScheme == .dark)
            ? Color.gray.opacity(0.3)
            : Color.gray.opacity(0.2)

        let currentLogin = playerDataManager.playerData!.login

        return HStack {
            Text("Current Difficulty: \(difficultyDescription(for: currentDifficulty))")
                .font(.title2)
                .fontWeight(.bold)
                .padding(.trailing)

            Text("Current Login: \(currentLogin)")
                .font(.title2)
                .fontWeight(.bold)
        }
        .frame(maxWidth: .infinity, minHeight: 100, idealHeight: 200)
        .background(backgroundColor)
        .cornerRadius(10)
        .padding(.horizontal, 20)
    }
    
    var switchColorPaletteButton: some View {
        Button("Switch Color Palette") {
            paletteManager.currentStyle = (paletteManager.currentStyle == .tritanopia) ? .normal : .tritanopia
        }
        .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
            palette.teal
        }))
    }

    var changeLoginButton: some View {
        Button("Change Login") {
            newLogin = playerDataManager.playerData?.login ?? ""
            showChangeLoginSheet = true
        }
        .buttonStyle(MainMenuButtonStyle())
    }

    var changeDifficultyButton: some View {
        Button("Change Difficulty") {
            showDifficultyOptions = true
        }
        .buttonStyle(MainMenuButtonStyle())
    }
    
    var switchUserButton: some View {
        Button("Switch User") {
            showSwitchUserConfirmation = true
        }
        .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
            palette.red
        }))
    }
    
    // MARK: - Helper Functions

    func loadCurrentDifficulty() async {
        isLoading = true
        do {
            let difficulty = try await networkManager.getDifficulty()
            await MainActor.run {
                currentDifficulty = difficulty
                isLoading = false
            }
        } catch {
            bannerManager.showError(message: "Failed to load current difficulty: \(error.localizedDescription)")
            isLoading = false
        }
    }

    func changeLogin() async {
        isLoading = true
        do {
            try await networkManager.updateLogin(newLogin: newLogin, playerDataManager: playerDataManager)
            isLoading = false
            showChangeLoginSheet = false
        } catch {
            isLoading = false
            bannerManager.showError(message: "Failed to change login: \(error.localizedDescription)")
        }
    }

    func changeDifficulty(to difficulty: Int) async {
        isLoading = true
        do {
            try await networkManager.setDifficulty(difficulty, playerDataManager: playerDataManager)
            currentDifficulty = difficulty
            isLoading = false
        } catch {
            bannerManager.showError(message: "Failed to change difficulty: \(error.localizedDescription)")
            isLoading = false
        }
    }

    func difficultyDescription(for difficulty: Int) -> String {
        switch difficulty {
        case 1: return "Easy"
        case 2: return "Normal"
        case 3: return "Hard"
        default: return "Unknown"
        }
    }
}

// MARK: - View Modifiers for Alerts and Sheets

extension View {
    func applyErrorAlert(errorMessage: Binding<String?>) -> some View {
        self.alert("Error", isPresented: Binding<Bool>(
            get: { errorMessage.wrappedValue != nil },
            set: { _ in errorMessage.wrappedValue = nil }
        )) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(errorMessage.wrappedValue ?? "")
        }
    }
    

    func applyChangeLoginSheet(isPresented: Binding<Bool>, newLogin: Binding<String>, changeLoginAction: @escaping () async -> Void) -> some View {
        self.sheet(isPresented: isPresented) {
            NavigationStack {
                Form {
                    TextField("New Login:", text: newLogin)
                        .padding()
                }
                .navigationTitle("Change Login")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") {
                            isPresented.wrappedValue = false
                        }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            Task {
                                await changeLoginAction()
                            }
                        }
                    }
                }
            }
        }
    }

    func applyDifficultyConfirmationDialog(isPresented: Binding<Bool>, changeDifficultyAction: @escaping (Int) -> Void) -> some View {
        self.confirmationDialog("Select Difficulty", isPresented: isPresented) {
            Button("Easy") { changeDifficultyAction(1) }
            Button("Normal") { changeDifficultyAction(2) }
            Button("Hard") { changeDifficultyAction(3) }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Choose your difficulty level")
        }
    }

    func applySwitchUserAlert(isPresented: Binding<Bool>, navigateToLogin: Binding<Bool>) -> some View {
        self.alert("Switch User?", isPresented: isPresented) {
            VStack {
                Button("Yes") {
                    navigateToLogin.wrappedValue = true
                }
                Button("No", role: .cancel) {
                    navigateToLogin.wrappedValue = false
                }
            }
        } message: {
            Text("Are you sure you want to switch user?")
        }
    }
}
