//
//  swiftui_frontendApp.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 07.11.2024.
//

import SwiftUI

@main
struct GemMatchApp: App {
    @State private var playerDataManager = PlayerDataManager()
    @State private var paletteManager = PaletteManager()
    @State private var bannerManager = BannerManager()
    @State private var networkManager = NetworkManager()

    var body: some Scene {
        WindowGroup {
            LoginView()
                .environment(playerDataManager)
                .environment(paletteManager)
                .environment(bannerManager)
                .environment(networkManager)
        }
    }
}
