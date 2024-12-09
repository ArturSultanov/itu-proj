//
//  GemView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 10.11.2024.
//
// GemView.swift

import SwiftUI

struct GemView: View {
    @State var gem: Gem
    var swapAction: (Direction) -> Void
    var clickAction: (Gem) -> Void

    @State private var dragOffset: CGSize = .zero

    var body: some View {
        let icon = IconType.getGemIcon(for: gem.type)
        
        Image(systemName: icon.symbolName)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .foregroundColor(icon.color)
            .frame(width: 50, height: 50)
            .offset(dragOffset)
//            .scaleEffect(dragOffset == .zero ? 1.0 : 1.1)
            .animation(.easeOut, value: dragOffset) // Animate drag offset changes
            .gesture(dragGesture)
            .onTapGesture {
                clickAction(gem)
            }
    }

    private var dragGesture: some Gesture {
        DragGesture()
            .onChanged { value in
                dragOffset = value.translation
            }
            .onEnded { value in
                let direction = getDragDirection(translation: value.translation)
                dragOffset = .zero
                if let direction = direction {
                    swapAction(direction)
                }
            }
    }

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
}

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
