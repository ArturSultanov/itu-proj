//
//  LoginView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct LoginView: View {
    
    @State private var loginInput: String = ""
    @State private var isLoggedIn: Bool = false
    @Environment(PlayerDataManager.self) var playerDataManager
    
    var body: some View {
        ZStack{
            NavigationStack{
                VStack(spacing: 20){
                    TextField("Your login", text: $loginInput)
                        .padding()
                    Button("Login"){
                        Task{
                            await login()
                        }
                    }
                    .buttonStyle(.bordered)
                    .padding()
                    
                    
                }
                .navigationTitle("Navigation")
                .navigationDestination(isPresented: $isLoggedIn) {
                    MainMenuView()
                }
            }
            .padding()
            
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

#Preview {
    LoginView()
}

