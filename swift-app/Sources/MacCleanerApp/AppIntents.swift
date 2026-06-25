import AppIntents
import Foundation

// MARK: - Scan intent (Siri: "Scan my Mac with MacCleaner")

struct ScanMacIntent: AppIntent {
    static var title        = LocalizedStringResource("Scan Mac for Junk")
    static var description  = IntentDescription("Scans your Mac for junk files and shows how much space you can free.")
    static var openAppWhenRun = true

    @MainActor
    func perform() async throws -> some IntentResult & ProvidesDialog {
        let result = await ScanEngine.shared.scan()
        guard let data = result?.data else {
            return .result(dialog: "I couldn't reach MacCleaner's engine. Please open the app and try again.")
        }
        let gb = String(format: "%.1f", data.totalSizeGB)
        return .result(dialog: "Found \(gb) GB of junk in \(data.totalCount) files across \(data.results.count) categories. Open MacCleaner to review and clean.")
    }
}

// MARK: - Storage intent (Siri: "How much space do I have on my Mac?")

struct StorageIntent: AppIntent {
    static var title        = LocalizedStringResource("Check Mac Storage")
    static var description  = IntentDescription("Checks how much free disk space your Mac has right now.")
    static var openAppWhenRun = false

    @MainActor
    func perform() async throws -> some IntentResult & ProvidesDialog {
        let result = await ScanEngine.shared.storage()
        guard let st = result?.data else {
            return .result(dialog: "Couldn't read disk usage. Please open MacCleaner.")
        }
        let freeGB = String(format: "%.1f", st.freeGB)
        let pct    = String(format: "%.0f", 100 - st.usedPct)
        return .result(dialog: "You have \(freeGB) GB free — that's \(pct)% of your disk.")
    }
}

// MARK: - Quick clean intent (Siri: "Clean my Mac caches")

struct CleanCachesIntent: AppIntent {
    static var title        = LocalizedStringResource("Clean Mac Caches")
    static var description  = IntentDescription("Scans for cache files and moves them to Trash.")
    static var openAppWhenRun = true

    @MainActor
    func perform() async throws -> some IntentResult & ProvidesDialog {
        let scanResult = await ScanEngine.shared.scan(categories: ["User Caches", "Browser Caches"])
        guard let data = scanResult?.data else {
            return .result(dialog: "Couldn't scan. Please open MacCleaner and try manually.")
        }
        let paths = data.results.flatMap(\.paths)
        guard !paths.isEmpty else {
            return .result(dialog: "Your caches look clean — nothing to remove right now! 🎉")
        }
        let cleanResult = await ScanEngine.shared.clean(paths: paths)
        let count = cleanResult?.data?.movedCount ?? 0
        return .result(dialog: "Moved \(count) cache files to Trash. Open MacCleaner to review before emptying Trash.")
    }
}

// MARK: - App Shortcuts (appear in Spotlight + Shortcuts app automatically)

struct MacCleanerShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: ScanMacIntent(),
            phrases: [
                "Scan my Mac with \(.applicationName)",
                "Find junk on my Mac",
                "Check my Mac for junk files",
            ],
            shortTitle: "Scan for Junk",
            systemImageName: "sparkles.rectangle.stack"
        )
        AppShortcut(
            intent: StorageIntent(),
            phrases: [
                "How much space do I have",
                "Check \(.applicationName) storage",
                "How full is my Mac",
            ],
            shortTitle: "Check Storage",
            systemImageName: "internaldrive"
        )
        AppShortcut(
            intent: CleanCachesIntent(),
            phrases: [
                "Clean my Mac caches with \(.applicationName)",
                "Delete caches on my Mac",
            ],
            shortTitle: "Clean Caches",
            systemImageName: "trash.circle.fill"
        )
    }
}
