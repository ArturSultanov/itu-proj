//
//  LoginView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct LoginView: View {
    @State private var player = Player()
    var body: some View {
        ZStack{
            VStack {
                Text("Welcome \(player.login)!")
                    .font(.largeTitle)
                    .fontWeight(.semibold)
                    .padding(.bottom, 42)
                LoginInputView()
                Button(action: {}) {
                    Text("Login")
                        .font(.title3)
                        .fontWeight(.semibold)
                        .frame(width: 100, height: 50)
                }
                .buttonStyle(.bordered)
                .cornerRadius(20)
            }
            
        }
        .environment(player)
    }
}


struct LoginInputView: View {
    
    @Environment(Player.self) var player
    
    @State private var loginInput: String = ""
    
    var body: some View {
        TextField("You login", text: $loginInput)
            .padding(.horizontal, 40)
            .frame(height: 40)
            .padding()
            .onChange(of: loginInput) {
                player.login = loginInput
            }
        
    }
}

#Preview {
    LoginView()
}

