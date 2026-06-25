import UserNotifications
import Foundation

// Smart scheduling: auto-scan every N hours, notify if junk found > threshold
@MainActor
final class NotificationService {
    static let shared = NotificationService()

    private let center = UNUserNotificationCenter.current()

    // MARK: Permission

    func requestPermission() {
        center.requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if let error { print("[Notifications] permission error: \(error)") }
        }
    }

    // MARK: Scan result notification

    func notifyJunkFound(gb: Double, count: Int) {
        guard gb > 0.2 else { return }   // skip trivial amounts

        let content       = UNMutableNotificationContent()
        content.title     = "MacCleaner"
        content.body      = String(format: "%.1f GB of junk found (%d files). Tap to review.", gb, count)
        content.sound     = .default
        content.categoryIdentifier = "JUNK_FOUND"

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(identifier: "junk-found", content: content, trigger: trigger)
        center.add(request)
    }

    // MARK: Disk pressure notification

    func notifyLowDisk(freeGB: Double, usedPct: Double) {
        guard usedPct > 85 else { return }

        let content   = UNMutableNotificationContent()
        content.title = "⚠️ Low Disk Space"
        content.body  = String(format: "Only %.0f GB remaining. Open MacCleaner to free space.", freeGB)
        content.sound = .defaultCritical

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(identifier: "disk-pressure", content: content, trigger: trigger)
        center.add(request)
    }

    // MARK: Scheduled weekly scan

    func scheduleWeeklyScan() {
        center.removePendingNotificationRequests(withIdentifiers: ["weekly-scan"])

        var comps        = DateComponents()
        comps.weekday    = 2    // Monday
        comps.hour       = 10   // 10 AM

        let content      = UNMutableNotificationContent()
        content.title    = "MacCleaner Weekly Scan"
        content.body     = "Time for your weekly cleanup. Tap to scan now."
        content.sound    = .default

        let trigger = UNCalendarNotificationTrigger(dateMatching: comps, repeats: true)
        let request = UNNotificationRequest(identifier: "weekly-scan", content: content, trigger: trigger)
        center.add(request)
    }

    // MARK: Background auto-scan (runs every N hours via DispatchSource)

    private var scanTimer: DispatchSourceTimer?

    func startAutoScanTimer(intervalHours: Int = 2) {
        scanTimer?.cancel()
        let source = DispatchSource.makeTimerSource(queue: .global(qos: .background))
        source.schedule(deadline: .now() + .hours(intervalHours),
                        repeating: .hours(intervalHours))
        source.setEventHandler { [weak self] in
            Task { @MainActor in
                await self?.performBackgroundScan()
            }
        }
        source.resume()
        scanTimer = source
    }

    private func performBackgroundScan() async {
        let scanResp    = await ScanEngine.shared.scan()
        let storageResp = await ScanEngine.shared.storage()

        if let data = scanResp?.data, data.totalSizeGB > 0.2 {
            notifyJunkFound(gb: data.totalSizeGB, count: data.totalCount)
        }
        if let st = storageResp?.data {
            notifyLowDisk(freeGB: st.freeGB, usedPct: st.usedPct)
        }
    }
}

// MARK: - DispatchTimeInterval convenience

private extension DispatchTimeInterval {
    static func hours(_ h: Int) -> DispatchTimeInterval { .seconds(h * 3600) }
}
