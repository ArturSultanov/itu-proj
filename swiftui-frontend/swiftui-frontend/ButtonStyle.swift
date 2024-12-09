//
//  MainMenuButtonStyle.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.12.2024.
//

import SwiftUI

struct MainMenuButtonStyle: ButtonStyle {
    var mainColor : Color
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity, minHeight: 50)
            .background(mainColor)
            .foregroundColor(.white)
            .font(.headline)
            .cornerRadius(10)
            .shadow(radius: configuration.isPressed ? 2 : 5, x: 0, y: configuration.isPressed ? 1 : 3)
            .padding(.horizontal, 20)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}

struct SecondaryMenuButtonStyle: ButtonStyle {
    var mainColor : Color
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: 50, minHeight: 50)
            .background(mainColor)
            .foregroundColor(.white)
            .font(.headline)
            .cornerRadius(10)
            .shadow(radius: configuration.isPressed ? 2 : 5, x: 0, y: configuration.isPressed ? 1 : 3)
            .padding(.horizontal, 20)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}

