//
//  LeaderBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.12.2024.
//

import SwiftUI


// MARK: - Leaderboard view
struct LeaderboardView: View {
    @Environment(NetworkManager.self) var networkManager    // Network action manager
    @Environment(BannerManager.self) var bannerManager      // Error banner manager

    @State private var topPlayers: [LeaderboardEntry] = []  // Holds the list of top players.
    @State private var isLoading = true                     // State for loading animation while fetching data
    
    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading…")
            } else {
                List {
                    ForEach(Array(topPlayers.enumerated()), id: \.element.id) { index, player in
                        HStack(spacing: 10) {
                            if index < 3 {
                                Image(systemName: "medal")
                                    .foregroundColor(.yellow)
                            }
                            else{
                                Image(systemName: "medal")
                            }
                            VStack(alignment: .leading, spacing: 2) {
                                Text(player.login)
                                    .font(.headline)
                                    .fontWeight(.bold)
                                Text("Score: \(player.highest_score)")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            .padding(5)
                        }
                    }
                }
                .listStyle(InsetListStyle())
            }
        }
        .navigationTitle("Leaderboard")
        .task {
            await loadLeaderboard() // Load the leaderboard data when the view appears
        }
    }
    
    /// Fetches the leaderboard data asynchronously and updates the UI
    private func loadLeaderboard() async {
        do {
            let players = try await networkManager.fetchLeaderboard(with: 15)
            await MainActor.run {
                topPlayers = players
                isLoading = false
            }
        } catch {
            bannerManager.showError(message: "Failed to load leaderboard: \(error.localizedDescription)")
            isLoading = false
        }
    }
}
