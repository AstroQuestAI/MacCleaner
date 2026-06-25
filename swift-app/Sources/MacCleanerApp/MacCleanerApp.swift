import AppKit
import SwiftUI

// Entry point — LSUIElement = true in Info.plist hides Dock icon
@main
struct MacCleanerApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var delegate

    var body: some Scene {
        // No main window scene — everything lives in the menu bar
        Settings { EmptyView() }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var menuBar: MenuBarController?

    func applicationDidFinishLaunching(_ notification: Notification) {
        // Hide from Dock
        NSApp.setActivationPolicy(.accessory)

        // Request notification permission once
        NotificationService.shared.requestPermission()

        // Boot the menu bar
        menuBar = MenuBarController()

        // Kick off first storage check
        Task { await menuBar?.refreshStorage() }
    }
}
