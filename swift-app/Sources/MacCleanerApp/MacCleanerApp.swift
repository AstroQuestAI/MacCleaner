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
    private var splashWindow: NSWindow?

    func applicationDidFinishLaunching(_ notification: Notification) {
        // Hide from Dock
        NSApp.setActivationPolicy(.accessory)

        // Request notification permission once
        NotificationService.shared.requestPermission()

        // Boot the menu bar
        menuBar = MenuBarController()

        // Kick off first storage check
        Task { await menuBar?.refreshStorage() }

        // Show splash screen on launch
        showSplash()
    }

    private func showSplash() {
        let w = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 380, height: 300),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        w.backgroundColor = .clear
        w.isOpaque = false
        w.hasShadow = true
        w.level = .floating
        w.isMovableByWindowBackground = true
        w.center()

        let view = SplashView {
            self.splashWindow?.orderOut(nil)
            self.splashWindow = nil
        }
        w.contentViewController = NSHostingController(rootView: view)
        w.makeKeyAndOrderFront(nil)
        splashWindow = w
    }
}
