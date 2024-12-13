//
//  NotificationBanner.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 13.12.2024.
//

import SwiftUI


/// The notification banner structure
struct NotificationBanner: View {
    let message: String

    var body: some View {
        Text(message)
            .foregroundColor(.white)
            .padding()
            .background(Color.red)
            .cornerRadius(8)
            .shadow(radius: 10)
            .padding()
    }
}


/// View to inject banner into other views
struct BannerViewModifier: ViewModifier {
    @Environment(BannerManager.self) var bannerManager

    func body(content: Content) -> some View {
        ZStack {
            content
            // Get the current banner message
            if let message = bannerManager.bannerMessage {
                VStack {
                    NotificationBanner(message: message)
                    Spacer()
                }
                .transition(.move(edge: .top))
                .animation(.easeInOut, value: bannerManager.bannerMessage)
            }
        }
    }
}

/// Function to apply modifier easily
extension View {
    func withBanner() -> some View {
        self.modifier(BannerViewModifier())
    }
}
