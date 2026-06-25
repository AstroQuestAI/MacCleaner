import AppKit
import SwiftUI

@MainActor
final class MenuBarController {
    private let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    private var mainWindowController: MainWindowController?
    private var currentFreeGB: Double = 0

    init() {
        updateLabel("⟳")
        buildMenu()
    }

    // MARK: - Label

    func refreshStorage() async {
        let result = await ScanEngine.shared.storage()
        if let data = result?.data {
            currentFreeGB = data.freeGB
            updateLabel(String(format: "%.0f GB", data.freeGB))
        }
    }

    private func updateLabel(_ text: String) {
        if let btn = statusItem.button {
            btn.title = text
            btn.font  = .monospacedSystemFont(ofSize: 12, weight: .medium)
        }
    }

    // MARK: - Menu

    private func buildMenu() {
        let menu = NSMenu()

        menu.addItem(withTitle: "Open MacCleaner", action: #selector(openMain), keyEquivalent: "")
            .target = self

        menu.addItem(withTitle: "Scan for Junk",   action: #selector(runScan),  keyEquivalent: "s")
            .target = self

        menu.addItem(.separator())

        let aiItem = NSMenuItem(title: "Ask AI…", action: #selector(openAI), keyEquivalent: "a")
        aiItem.target = self
        menu.addItem(aiItem)

        menu.addItem(.separator())

        menu.addItem(withTitle: "Quit MacCleaner", action: #selector(NSApplication.terminate(_:)),
                     keyEquivalent: "q")

        statusItem.menu = menu
    }

    @objc private func openMain() {
        if mainWindowController == nil {
            mainWindowController = MainWindowController()
        }
        mainWindowController?.showWindow(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    @objc private func runScan() {
        openMain()
        mainWindowController?.startScan()
    }

    @objc private func openAI() {
        openMain()
        mainWindowController?.showAIPanel()
    }
}
