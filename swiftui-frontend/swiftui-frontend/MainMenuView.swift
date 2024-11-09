//
//  MainMenuView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.11.2024.
//

import SwiftUI

struct MainMenuView: View {
    
    
    var body: some View {
        ZStack{
            VStack(spacing: 20){
                HStack{
                    Text ("Hello, ")
                }
                .padding()
                .font(.title2)
                
                Button(action: {}) {
                    Text("New Game")
                }
                
                Button(action: {}) {
                    Text("Continue")
                }
                
                Button(action: {}) {
                    Text("Settings")
                }
                Button(action: {}) {
                    Text("Leader board")
                }
                Button(action: {}){
                    Text("Quit Game")
                }
                .buttonStyle(.bordered)
                .padding()
            }
            
        }
    }
}


#Preview {
    MainMenuView()
}
