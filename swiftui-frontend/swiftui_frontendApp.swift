//
//  swiftui_frontendApp.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 07.11.2024.
//

import SwiftUI



// MARK: The main entry point
@main
struct GemMatchApp: App {
    // Setup the managers as states
    @State private var playerDataManager = PlayerDataManager()  // Shared player data manager
    @State private var paletteManager = PaletteManager()        // Color palette manager
    @State private var bannerManager = BannerManager()          // Error banner manager
    @State private var networkManager = NetworkManager()        // Network action manager

    var body: some Scene {
        WindowGroup {
            LoginView() // The login view is entry point to app
                .padding([.leading, .trailing, .bottom], 20)
                .withBanner() // Setup notifications banners for the whole app
                .environment(playerDataManager)
                .environment(paletteManager)
                .environment(bannerManager)
                .environment(networkManager)
        }
        
    }
}
