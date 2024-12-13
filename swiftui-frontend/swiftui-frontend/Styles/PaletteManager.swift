//
//  PaletteManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 12.12.2024.
//

import SwiftUI
import Observation


// Manager to switch color palette
@Observable class PaletteManager {

    enum PaletteStyle {
        case tritanopia
        case normal
    }
    
    var currentStyle: PaletteStyle = .tritanopia
    
    var currentPalette: ColorPalette {
        switch currentStyle {
        case .tritanopia:
            return .tritanopia
        case .normal:
            return .normal
        }
    }
}
