//
//  LoginView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct LoginView: View {
    @Environment(PlayerDataManager.self) var playerDataManager
    @State private var loginInput: String = ""
    @State private var isLoggedIn: Bool = false
    @State private var isShowQuitConfirmation = false
    @Environment(\.colorScheme) var colorScheme // Access current system theme

    
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
//                        .background(loginInput.isEmpty ? Color.red : Color.gray)
//                        .foregroundColor(.black)
                        .background(
                            loginInput.isEmpty
                            ? (colorScheme == .dark ? Color.red.opacity(0.5) : Color.red.opacity(0.2))
                            : (colorScheme == .dark ? Color.gray.opacity(0.3) : Color.gray.opacity(0.2))
                        )
                        .cornerRadius(10)
                        .shadow(radius: 5, x: 0, y: 3)
                        .padding(.horizontal, 20)
                    
                    Button("Confirm") {
                        Task {
                            await login()
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
            .aspectRatio(1, contentMode: .fit)
            .padding([.leading, .trailing, .bottom], 20)
        }
        .alert("Quit Game?", isPresented: $isShowQuitConfirmation) {
            VStack {
                Button("Yes") {
                    Task {
                        await quitGame()
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
