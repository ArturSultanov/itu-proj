//
//  ButtonStyle.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 09.12.2024.
//

import SwiftUI


struct MainMenuButtonStyle: ButtonStyle {
    @Environment(PaletteManager.self) var paletteManager
    @Environment(\.isEnabled) private var isEnabled: Bool

    var customColorProvider: ((ColorPalette) -> Color)? = nil
    
    func makeBody(configuration: Configuration) -> some View {
        // Use the custom color if provided, otherwise fall back to the palette.
        let activeColor = customColorProvider?(paletteManager.currentPalette)
            ?? paletteManager.currentPalette.primaryButton
        
        let backgroundColor = isEnabled ? activeColor : .gray

        return configuration.label
            .frame(maxWidth: .infinity, minHeight: 50)
            .background(backgroundColor)
            .foregroundColor(.white)
            .font(.headline)
            .cornerRadius(10)
            .shadow(radius: configuration.isPressed ? 2 : 5,
                    x: 0, y: configuration.isPressed ? 1 : 3)
            .padding(.horizontal, 20)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}


struct SecondaryMenuButtonStyle: ButtonStyle {
    @Environment(PaletteManager.self) var paletteManager
    @Environment(\.isEnabled) private var isEnabled: Bool

    var customColorProvider: ((ColorPalette) -> Color)? = nil
    
    func makeBody(configuration: Configuration) -> some View {
        // Use the custom color if provided, otherwise fall back to the palette.
        let activeColor = customColorProvider?(paletteManager.currentPalette)
            ?? paletteManager.currentPalette.primaryButton
        
        let backgroundColor = isEnabled ? activeColor : .gray

        return configuration.label
            .frame(maxWidth: 50, minHeight: 50)
            .background(backgroundColor)
            .foregroundColor(.white)
            .font(.headline)
            .cornerRadius(10)
            .shadow(radius: configuration.isPressed ? 2 : 5,
                    x: 0, y: configuration.isPressed ? 1 : 3)
            .padding(.horizontal, 20)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}
