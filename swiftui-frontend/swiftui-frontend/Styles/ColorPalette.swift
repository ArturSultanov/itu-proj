//
//  TritanopiaColors.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 08.12.2024.
//

import SwiftUI


struct ColorPalette {
    let red: Color
    let blue: Color
    let pink: Color
    let teal: Color
    let purple: Color
    let primaryButton: Color
    let primaryBanner: Color
}

// Tritanopia Palette
extension ColorPalette {
    static let tritanopia = ColorPalette(
        red: Color(red: 1.0, green: 0, blue: 0.4),
        blue: Color(red: 0, green: 0.9, blue: 0.9),
        pink: Color(red: 1.0, green: 0.6, blue: 0.65),
        teal: Color(red: 0.0, green: 0.6, blue: 0.6),
        purple: Color(red: 0.76, green: 0.5, blue: 1.0),
        primaryButton: Color(red: 0.13, green: 0.55, blue: 0.7),
        primaryBanner: Color(red: 0.13, green: 0.55, blue: 0.7)
    )
    
    // Normal Palette (customize as desired)
    static let normal = ColorPalette(
        red: .red,
        blue: .blue,
        pink: .pink,
        teal: .green,
        purple: .purple,
        primaryButton: .blue,
        primaryBanner: .blue
    )
}

extension Color {
    
    public static let tritanopiaRed: Color = Color(red: 1.0, green: 0, blue: 0.4) // #ff0066
    public static let tritanopiaBlue: Color = Color(red: 0, green: 0.9, blue: 0.9) // #00e6e6
    public static let tritanopiaPink: Color = Color(red: 1.0, green: 0.6, blue: 0.65) // #ffb9bd
    public static let tritanopiaTeal: Color = Color(red: 0.0, green: 0.6, blue: 0.6) // #009999
    public static let tritanopiaPurple: Color = Color(red: 0.76, green: 0.5, blue: 1.0) // #C280FF
    
    public static let tritanopiaPrimaryButton: Color = Color(red: 0.13, green: 0.55, blue: 0.7) // #218ab2
    public static let tritanopiaPrimaryBanner: Color = Color(red: 0.13, green: 0.55, blue: 0.7) // #218ab2
}
