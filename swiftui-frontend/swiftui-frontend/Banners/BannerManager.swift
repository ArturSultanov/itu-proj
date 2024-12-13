//
//  BannerManager.swift
//  swiftui-frontend
//
//  Created by Artur Sultanov on 13.12.2024.
//

import SwiftUI
import Combine

@Observable class BannerManager {
    var bannerMessage: String? = nil
    
    /// Displays an error message in the banner and automatically dismisses it after a delay.
    func showError(message: String) {
        bannerMessage = message
        DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
            self.bannerMessage = nil
        }
    }
}


