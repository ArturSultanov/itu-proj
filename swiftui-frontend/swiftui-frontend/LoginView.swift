//
//  LoginView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.11.2024.
//

import SwiftUI

import SwiftUI

struct LoginView: View {
    @State private var loginText = ""
    @State private var isLoading = false
    @State private var showError = false
    @State private var navigateToMenu = false
    private var networkManager = NetworkManager.shared
    @State private var user: User?

    var body: some View {
        VStack {
            Text("Welcome to Gem Match!")
                .font(.largeTitle)
                .padding()

            TextField("Enter your login", text: $loginText)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            if isLoading {
                ProgressView()
            } else {
                Button(action: login) {
                    Text("Login")
                        .font(.headline)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.accentColor)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()
                .disabled(loginText.isEmpty)
            }

            if showError {
                Text("Login failed. Please try again.")
                    .foregroundColor(.red)
            }
            
            if navigateToMenu {
                Text("Success")
                    .foregroundColor(.red)
            }

        }
        .padding()
    }

    func login() {
        Task {
            isLoading = true
            do {
                print("Hello")
                user = try await networkManager.login(with: loginText)
                isLoading = false
                navigateToMenu = true
            } catch {
                isLoading = false
                showError = true
            }
        }
    }
}


#Preview {
    LoginView()
}
