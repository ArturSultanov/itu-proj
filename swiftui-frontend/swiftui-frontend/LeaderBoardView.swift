//
//  LeaderBoardView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.12.2024.
//

import SwiftUI

struct LeaderboardView: View {
    @State private var topPlayers: [LeaderboardEntry] = []
    @State private var isLoading = true
    @State private var errorMessage: String?
    
    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Loading Leaderboard…")
            } else if let errorMessage = errorMessage {
                Text(errorMessage)
                    .foregroundColor(.red)
                    .multilineTextAlignment(.center)
                    .padding()
            } else {
                List(topPlayers) { player in
                    HStack {
                        Text(player.login)
                            .fontWeight(.bold)
                        Spacer()
                        Text("\(player.highest_score)")
                    }
                }
                .listStyle(PlainListStyle())
            }
        }
        .navigationTitle("Leaderboard")
        .task {
            await loadLeaderboard()
        }
    }
    
    private func loadLeaderboard() async {
        do {
            let players = try await NetworkManager.shared.fetchLeaderboard()
            await MainActor.run {
                topPlayers = players
                isLoading = false
            }
        } catch {
            await MainActor.run {
                errorMessage = "Failed to load leaderboard: \(error.localizedDescription)"
                isLoading = false
            }
        }
    }
}

