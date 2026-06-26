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
        // Request notification permission once
        NotificationService.shared.requestPermission()

        // Boot the menu bar
        menuBar = MenuBarController()

        // Kick off first storage check
        Task { await menuBar?.refreshStorage() }

        // Show splash as a regular (non-UIElement) app so it can come to front.
        // setActivationPolicy(.accessory) is deferred until the splash closes.
        NSApp.activate(ignoringOtherApps: true)
        showSplash()
    }

    private func showSplash() {
        let w = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 520, height: 400),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        w.backgroundColor = .clear
        w.isOpaque = false
        w.hasShadow = true
        w.level = .floating
        w.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        w.isMovableByWindowBackground = true
        w.center()

        let view = SplashView {
            self.splashWindow?.orderOut(nil)
            self.splashWindow = nil
            // Now that splash is gone, retreat to menu-bar-only mode
            NSApp.setActivationPolicy(.accessory)
        }
        let hosting = NSHostingController(rootView: view)
        hosting.view.frame = NSRect(x: 0, y: 0, width: 520, height: 400)
        w.contentViewController = hosting
        w.setContentSize(NSSize(width: 520, height: 400))
        w.center()
        w.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        splashWindow = w
    }
}
