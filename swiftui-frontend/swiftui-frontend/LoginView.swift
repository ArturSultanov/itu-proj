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
    
    var body: some View {
        ZStack {
            VStack {
                NavigationStack {
                    Text("Enter your name")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.blue)
                        .padding(.bottom, 20)
                    
                    TextField("Your login", text: $loginInput)
                        .padding()
                        .background(Color.white)
                        .foregroundColor(.black)
                        .cornerRadius(10)
                        .shadow(radius: 5, x: 0, y: 3)
                        .padding(.horizontal, 40)
                    
                    Button("Confirm") {
                        Task {
                            await login()
                        }
                    }
                    .buttonStyle(LoginButtonStyle())
                    .padding(.top, 10)
                    .navigationTitle("Welcome")
                    .navigationDestination(isPresented: $isLoggedIn) {
                        MainMenuView()}
                }
            }
            .aspectRatio(1, contentMode: .fit)
            .padding([.leading, .trailing, .bottom], 20)
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
}

struct LoginButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity, minHeight: 50)
            .background(
                LinearGradient(
                    gradient: Gradient(colors: [Color.tritanopiaRed, Color.tritanopiaTeal]),
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .foregroundColor(.white)
            .font(.headline)
            .cornerRadius(10)
            .shadow(radius: configuration.isPressed ? 2 : 5, x: 0, y: configuration.isPressed ? 1 : 3)
            .padding(.horizontal, 40)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}

#Preview {
    LoginView()
        .environment(PlayerDataManager())
}
