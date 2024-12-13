//
//  NotificationBanner.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 13.12.2024.
//

import SwiftUI

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

//struct BannerModifier: ViewModifier {
//    @Binding var isPresented: Bool
//    let message: String
//
//    func body(content: Content) -> some View {
//        ZStack {
//            content
//            if isPresented {
//                VStack {
//                    NotificationBanner(message: message)
//                    Spacer()
//                }
//                .transition(.move(edge: .top))
//                .animation(.easeInOut, value: isPresented)
//            }
//        }
//    }
//}
//
//extension View {
//    func banner(isPresented: Binding<Bool>, message: String) -> some View {
//        self.modifier(BannerModifier(isPresented: isPresented, message: message))
//    }
//}



struct BannerViewModifier: ViewModifier {
    @Environment(BannerManager.self) var bannerManager

    func body(content: Content) -> some View {
        ZStack {
            content
            
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


extension View {
    func withBanner() -> some View {
        self.modifier(BannerViewModifier())
    }
}
