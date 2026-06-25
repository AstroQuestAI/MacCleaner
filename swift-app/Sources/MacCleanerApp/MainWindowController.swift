import AppKit
import SwiftUI

@MainActor
final class MainWindowController: NSWindowController {

    private let mainVM: MainViewModel

    init() {
        let vm = MainViewModel()
        self.mainVM = vm

        let contentView = MainView(vm: vm)
        let hosting     = NSHostingController(rootView: contentView)
        let window      = NSWindow(contentViewController: hosting)

        window.title          = "MacCleaner"
        window.styleMask      = [.titled, .closable, .miniaturizable, .resizable]
        window.setContentSize(NSSize(width: 700, height: 520))
        window.center()
        window.isReleasedWhenClosed = false

        super.init(window: window)
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) not implemented") }

    func startScan() {
        Task { await mainVM.runScan() }
    }

    func showAIPanel() {
        mainVM.activeTab = .ai
    }
}
