import SwiftUI

struct SettingsView: View {
    @Environment(PlayerDataManager.self) var playerDataManager
    
    @State private var showChangeLoginSheet = false
    @State private var newLogin: String = ""
    
    @State private var showDifficultyOptions = false
    @State private var currentDifficulty: Int = 1 // Default to 1 (Easy) until fetched
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Settings")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            if isLoading {
                ProgressView("Loading…")
            } else {
                // Show current difficulty at top
                HStack{
                    Text("Current Difficulty: \(difficultyDescription(for: currentDifficulty))")
                        .font(.headline)
                        .padding(.bottom, 20)
                    Text("Current Login: \(playerDataManager.playerData!.login)")
                        .font(.headline)
                        .padding(.bottom, 20)
                }
                
                
                Button("Change Login") {
                    newLogin = playerDataManager.playerData?.login ?? ""
                    showChangeLoginSheet = true
                }
                .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaTeal))
                
                Button("Change Difficulty") {
                    showDifficultyOptions = true
                }
                .buttonStyle(MainMenuButtonStyle(mainColor: Color.tritanopiaPink))
            }
        }
        .padding()
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
        .task {
            await loadCurrentDifficulty()
        }
    }
    
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
    
    private func difficultyDescription(for difficulty: Int) -> String {
        switch difficulty {
        case 1: return "Easy"
        case 2: return "Normal"
        case 3: return "Hard"
        default: return "Unknown"
        }
    }
}
