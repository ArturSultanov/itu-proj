//
//  PaletteManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 12.12.2024.
//

import SwiftUI
import Observation

@Observable class PaletteManager {
    enum PaletteStyle {
        case tritanopia
        case normal
    }
    
    var currentStyle: PaletteStyle = .tritanopia // Default to tritanopia
}

extension PaletteManager {
    var currentPalette: ColorPalette {
        switch currentStyle {
        case .tritanopia:
            return .tritanopia
        case .normal:
            return .normal
        }
    }
}
