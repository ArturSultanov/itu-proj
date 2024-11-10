//
//  GemView.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 10.11.2024.
//

import SwiftUI


// GemView.swift
import SwiftUI

import SwiftUI

struct GemView: View {
    @State var gem: Gem
    var swapAction: (Direction) -> Void

    @State private var dragOffset: CGSize = .zero

    var body: some View {
        let icon = IconType.getGemIcon(for: gem.type)

        Image(systemName: icon.symbolName)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .foregroundColor(icon.color)
            .frame(width: 50, height: 50)
            .offset(dragOffset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        self.dragOffset = value.translation
                    }
                    .onEnded { value in
                        let direction = getDragDirection(translation: value.translation)
                        self.dragOffset = .zero
                        if let direction = direction {
                            swapAction(direction)
                        }
                    }
            )
    }

    func getDragDirection(translation: CGSize) -> Direction? {
        let threshold: CGFloat = 20
        if abs(translation.width) > abs(translation.height) {
            if translation.width > threshold {
                return .right
            } else if translation.width < -threshold {
                return .left
            }
        } else {
            if translation.height > threshold {
                return .down
            } else if translation.height < -threshold {
                return .up
            }
        }
        return nil
    }
}

enum IconType: CaseIterable, Equatable {
    case triangle
    case circle
    case square
    case diamond
    case heart

    var color: Color {
        switch self {
        case .triangle: return .purple
        case .circle: return .pink
        case .square: return .orange
        case .diamond: return .yellow
        case .heart: return .red
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
