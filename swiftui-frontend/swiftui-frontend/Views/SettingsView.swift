//
//  SettingsView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct SettingsView: View {
    @Environment(PlayerDataManager.self) var playerDataManager
    @Environment(PaletteManager.self) var paletteManager
    @Environment(NetworkManager.self) var networkManager
//    @Environment(BannerManager.self) var bannerManager
    @Environment(\.colorScheme) var colorScheme

    @State private var showChangeLoginSheet = false
    @State private var newLogin: String = ""
    @State private var showSwitchUserConfirmation = false
    @State private var navigateToLogin = false
    @State private var showDifficultyOptions = false
    @State private var currentDifficulty: Int = 1
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        ZStack {
            mainContent
        }
        .applyErrorAlert(errorMessage: $errorMessage)
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
    private var mainContent: some View {
        VStack {
            if isLoading {
                Color.black.opacity(0.3)
                    .edgesIgnoringSafeArea(.all)
                ProgressView("Loading…")
                    .padding(40)
                    .background(Color.white)
                    .cornerRadius(10)
            } else {
                topInfoView
                switchColorPaletteButton
                changeLoginButton
                changeDifficultyButton
                switchUserButton
            }
        }
        .padding([.leading, .trailing, .bottom], 20)
    }

    // Extracted the top info HStack
    private var topInfoView: some View {
        // Precompute the background color
        let backgroundColor = (colorScheme == .dark)
            ? Color.gray.opacity(0.3)
            : Color.gray.opacity(0.2)

        // Safely unwrap login
        let currentLogin = playerDataManager.playerData?.login ?? "Unknown"

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
    
    private var switchColorPaletteButton: some View {
        Button("Switch Color Palette") {
            paletteManager.currentStyle = (paletteManager.currentStyle == .tritanopia) ? .normal : .tritanopia
        }
        .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
            palette.teal
        }))
    }

    private var changeLoginButton: some View {
        Button("Change Login") {
            newLogin = playerDataManager.playerData?.login ?? ""
            showChangeLoginSheet = true
        }
        .buttonStyle(MainMenuButtonStyle())
    }

    private var changeDifficultyButton: some View {
        Button("Change Difficulty") {
            showDifficultyOptions = true
        }
        .buttonStyle(MainMenuButtonStyle())
    }
    
    private var switchUserButton: some View {
        Button("Switch User") {
            showSwitchUserConfirmation = true
        }
        .buttonStyle(MainMenuButtonStyle(customColorProvider: { palette in
            palette.red
        }))
    }
    
    // MARK: - Helper Functions

    private func loadCurrentDifficulty() async {
        isLoading = true
        do {
            let difficulty = try await networkManager.getDifficulty()
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

    private func changeLogin() async {
        isLoading = true
        do {
            try await networkManager.updateLogin(newLogin: newLogin, playerDataManager: playerDataManager)
            isLoading = false
            showChangeLoginSheet = false
        } catch {
            isLoading = false
//            errorMessage = "Failed to change login: \(error.localizedDescription)"
//            bannerManager.showBanner(message: "Failed to change login: \(error.localizedDescription)")

        }
    }

    private func changeDifficulty(to difficulty: Int) async {
        isLoading = true
        do {
            try await networkManager.setDifficulty(difficulty, playerDataManager: playerDataManager)
            currentDifficulty = difficulty
            isLoading = false
        } catch {
            isLoading = false
            errorMessage = "Failed to change difficulty: \(error.localizedDescription)"
        }
    }

    private func difficultyDescription(for difficulty: Int) -> String {
        switch difficulty {
        case 1: return "Easy"
        case 2: return "Normal"
        case 3: return "Hard"
        default: return "Unknown"
        }
    }
}

// MARK: - View Modifiers for Alerts and Sheets

private extension View {
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
