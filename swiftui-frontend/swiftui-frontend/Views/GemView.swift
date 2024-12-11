//
//  GemView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 10.11.2024.
//

import SwiftUI

/// Represents a single gem on the game board.
struct GemView: View {
    @State var gem: Gem // Includes type and position
    @State private var dragOffset: CGSize = .zero // Tracks the drag offset

    var swapAction: (Direction) -> Void // Closure to handle swapping the gem
    var clickAction: (Gem) -> Void // Closure to handle clicking the gem

    var body: some View {
        let icon = IconType.getGemIcon(for: gem.type)
        // Modify the gem icon
        Image(systemName: icon.symbolName)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .foregroundColor(icon.color)
            .frame(width: 50, height: 50)
            .offset(dragOffset)
            .animation(.easeOut, value: dragOffset) // Animate drag offset changes
            .gesture(dragGesture)
            .onTapGesture {
                clickAction(gem)
            }
    }

    /// Drag gesture for swapping gems by direction.
    private var dragGesture: some Gesture {
        DragGesture()
            .onChanged { value in
                dragOffset = value.translation
            }
            .onEnded { value in
                let direction = getDragDirection(translation: value.translation) // Determine drag direction
                dragOffset = .zero // Reset the drag offset after the gesture ends
                if let direction = direction {
                    swapAction(direction)
                }
            }
    }
    
    /// Determines the drag direction based on the translation.
    /// - Parameter translation: The drag translation vector.
    /// - Returns: The detected direction (`up`, `down`, `left`, `right`), or `nil` if no direction detected.
    private func getDragDirection(translation: CGSize) -> Direction? {
        let threshold: CGFloat = 20 // Minimum drag distance to detect a direction.
        
        // Horizontal drag
        if abs(translation.width) > abs(translation.height) {
            if translation.width > threshold { return .right }
            else if translation.width < -threshold { return .left }
        // Vertical drag
        } else {
            if translation.height > threshold { return .down }
            else if translation.height < -threshold { return .up }
        }
        // No drag
        return nil
    }
}

/// Represents the  gem types
enum IconType: CaseIterable, Equatable {
    case triangle, circle, square, diamond, heart

    var color: Color {
        switch self {
        case .triangle: return .tritanopiaPurple
        case .circle: return .tritanopiaTeal
        case .square: return .tritanopiaPink
        case .diamond: return .tritanopiaBlue
        case .heart: return .tritanopiaRed
        }
    }

    var symbolName: String {
        switch self {
        case .triangle: return "triangle.fill"
        case .circle: return "circle.fill"
        case .square: return "square.fill"
        case .diamond: return "diamond.fill"
        case .heart: return "heart.fill"
        }
    }

    static func getGemIcon(for typeIndex: Int) -> IconType {
        let allCases = Array(Self.allCases)
        return allCases[typeIndex % allCases.count]
    }
}
