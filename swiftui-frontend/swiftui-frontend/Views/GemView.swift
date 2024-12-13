//
//  GemView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 10.11.2024.
//

import SwiftUI


// MARK: - Gem view
struct GemView: View {
    @Environment(PaletteManager.self) var paletteManager    // Color palette manager
    @State private var dragOffset: CGSize = .zero           // Offset how much gem is moved

    var gem: Gem
    var iconType: IconType
    var swapAction: (Direction) -> Void                     // Closure for swap gems action
    var clickAction: (Gem) -> Void                          // Closure for click action
    
    var body: some View {
        let symbolName = symbolName(for: iconType)          // Get the SF symbol name for the gem icon type
        let color = colorForIcon(iconType, in: paletteManager.currentPalette) // Get the gem color from the palette
        
        Image(systemName: symbolName)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .foregroundColor(color)
            .frame(width: 50, height: 50)
            .offset(dragOffset)
            .animation(.easeOut, value: dragOffset) // Animate drag offset changes
            .gesture(dragGesture)
            .onTapGesture {
                clickAction(gem)
            }
    }

    // MARK: - Drag Gesture
    /// Drag gesture to handle the movement of the gem and trigger swaps.
    private var dragGesture: some Gesture {
        DragGesture()
            .onChanged { value in
                dragOffset = value.translation // Update the drag offset while dragging
            }
            .onEnded { value in
                let direction = getDragDirection(translation: value.translation) // Determine the drag direction
                dragOffset = .zero // Reset the drag offset after release
                if let direction = direction {
                    swapAction(direction)
                }
            }
    }

    // MARK: - Drag Direction Detection
    /// Determines the drag direction based on the drag translation.
    /// - Parameter translation: The size of the drag translation.
    /// - Returns: The direction of the drag or `nil` if the drag does not meet the threshold.
    private func getDragDirection(translation: CGSize) -> Direction? {
        let threshold: CGFloat = 20
        if abs(translation.width) > abs(translation.height) {
            if translation.width > threshold { return .right }
            else if translation.width < -threshold { return .left }
        } else {
            if translation.height > threshold { return .down }
            else if translation.height < -threshold { return .up }
        }
        return nil
    }
    
    // MARK: - Icon Symbol Mapping
    /// Maps an `IconType` to its corresponding SF Symbol name.
    /// - Parameter icon: The type of icon.
    /// - Returns: The SF Symbol name for the icon.
    private func symbolName(for icon: IconType) -> String {
        switch icon {
        case .triangle: return "triangle.fill"
        case .circle: return "circle.fill"
        case .square: return "square.fill"
        case .diamond: return "diamond.fill"
        case .heart: return "heart.fill"
        }
    }

    // MARK: - Icon Color Mapping
    /// Maps an `IconType` to its corresponding color in the current palette.
    /// - Parameters:
    ///   - icon: The type of icon.
    ///   - palette: The current color palette.
    /// - Returns: The color for the icon.
    private func colorForIcon(_ icon: IconType, in palette: ColorPalette) -> Color {
        switch icon {
        case .triangle: return palette.purple
        case .circle: return palette.teal
        case .square: return palette.pink
        case .diamond: return palette.blue
        case .heart: return palette.red
        }
    }
}

// MARK: - Different icon types of gems
/// Represents the different icon types for gems.
enum IconType: CaseIterable, Equatable {
    case triangle
    case circle
    case square
    case diamond
    case heart

    static func getGemIcon(for typeIndex: Int) -> IconType {
        let allCases = Array(Self.allCases)
        return allCases[typeIndex % allCases.count]
    }
}

