import SwiftUI

// MARK: - AppStorage keys (mirrors Python Settings dataclass)

private enum Key {
    static let trayLabel        = "trayLabel"          // "free" | "pct"
    static let autoScan         = "autoScan"
    static let scanIntervalH    = "scanIntervalH"      // 1/2/6/12/24
    static let notifyAbovePct   = "notifyAbovePct"     // 50-90
    static let junkMinMB        = "junkMinMB"          // 50-500
    static let warnPct          = "warnPct"            // 60-85
    static let critPct          = "critPct"            // 80-95
    static let scanNodeModules  = "scanNodeModules"
    static let startupDelayS    = "startupDelayS"      // 5/15/30/60
}

// MARK: - Settings tab

struct SettingsTabView: View {

    @AppStorage("themeKey")          private var themeKey       = "glass"
    @AppStorage(Key.trayLabel)       private var trayLabel      = "free"
    @AppStorage(Key.autoScan)        private var autoScan       = true
    @AppStorage(Key.scanIntervalH)   private var scanIntervalH  = 2
    @AppStorage(Key.notifyAbovePct)  private var notifyAbovePct = 70
    @AppStorage(Key.junkMinMB)       private var junkMinMB      = 200
    @AppStorage(Key.warnPct)         private var warnPct        = 70
    @AppStorage(Key.critPct)         private var critPct        = 85
    @AppStorage(Key.scanNodeModules) private var scanNodeModules = true
    @AppStorage(Key.startupDelayS)   private var startupDelayS  = 15

    @State private var savedFlash = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {

                // ── Appearance ─────────────────────────────────────────────
                SettingsSection(title: "Appearance") {
                    ThemePickerRow(themeKey: $themeKey)
                    PickerRow(label: "Menu bar shows",
                              selection: $trayLabel,
                              options: [("free", "Free space GB"), ("pct", "Used %")])
                }

                // ── Scheduler ──────────────────────────────────────────────
                SettingsSection(title: "Scheduler") {
                    ToggleRow(label: "Auto-scan in background", value: $autoScan)

                    PickerRow(label: "Scan interval",
                              selection: Binding(
                                  get: { String(scanIntervalH) },
                                  set: { scanIntervalH = Int($0) ?? 2 }
                              ),
                              options: [("1","1 hour"),("2","2 hours"),("6","6 hours"),
                                        ("12","12 hours"),("24","24 hours")])
                    .disabled(!autoScan)

                    PickerRow(label: "Notify when disk ≥",
                              selection: Binding(
                                  get: { String(notifyAbovePct) },
                                  set: { notifyAbovePct = Int($0) ?? 70 }
                              ),
                              options: [("50","50%"),("60","60%"),("70","70%"),
                                        ("80","80%"),("90","90%")])

                    PickerRow(label: "Min junk to notify",
                              selection: Binding(
                                  get: { String(junkMinMB) },
                                  set: { junkMinMB = Int($0) ?? 200 }
                              ),
                              options: [("50","50 MB"),("100","100 MB"),
                                        ("200","200 MB"),("500","500 MB")])

                    PickerRow(label: "Warn colour at",
                              selection: Binding(
                                  get: { String(warnPct) },
                                  set: { warnPct = Int($0) ?? 70 }
                              ),
                              options: [("60","60%"),("70","70%"),("75","75%"),
                                        ("80","80%"),("85","85%")])

                    PickerRow(label: "Critical colour at",
                              selection: Binding(
                                  get: { String(critPct) },
                                  set: { critPct = Int($0) ?? 85 }
                              ),
                              options: [("80","80%"),("85","85%"),
                                        ("90","90%"),("95","95%")])
                }

                // ── Scan ───────────────────────────────────────────────────
                SettingsSection(title: "Scan") {
                    ToggleRow(label: "Scan node_modules folders",
                              value: $scanNodeModules)

                    PickerRow(label: "Startup scan delay",
                              selection: Binding(
                                  get: { String(startupDelayS) },
                                  set: { startupDelayS = Int($0) ?? 15 }
                              ),
                              options: [("5","5 s"),("15","15 s"),
                                        ("30","30 s"),("60","60 s")])
                }

                // ── Footer ─────────────────────────────────────────────────
                HStack {
                    if savedFlash {
                        Label("Saved", systemImage: "checkmark.circle.fill")
                            .foregroundStyle(.green)
                            .font(.callout)
                            .transition(.opacity)
                    }
                    Spacer()
                    Button {
                        applyToNotificationService()
                        withAnimation { savedFlash = true }
                        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                            withAnimation { savedFlash = false }
                        }
                    } label: {
                        Label("Save Settings", systemImage: "square.and.arrow.down")
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding(.top, 4)
            }
            .padding(24)
        }
    }

    private func applyToNotificationService() {
        Task { @MainActor in
            let svc = NotificationService.shared
            if autoScan {
                svc.startAutoScanTimer(intervalHours: scanIntervalH)
            } else {
                svc.stopAutoScanTimer()
            }
        }
    }
}

// MARK: - Sub-views

private struct SettingsSection<Content: View>: View {
    let title: String
    @ViewBuilder let content: () -> Content

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text(title.uppercased())
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(.secondary)
                .padding(.horizontal, 14)
                .padding(.bottom, 6)

            VStack(spacing: 0) {
                content()
            }
            .background(Color(nsColor: .controlBackgroundColor))
            .clipShape(RoundedRectangle(cornerRadius: 10))
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(Color(nsColor: .separatorColor).opacity(0.5), lineWidth: 0.5)
            )
        }
    }
}

private struct ToggleRow: View {
    let label: String
    @Binding var value: Bool

    var body: some View {
        HStack {
            Text(label).font(.callout)
            Spacer()
            Toggle("", isOn: $value).labelsHidden()
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 10)
        Divider().padding(.leading, 14)
    }
}

private struct ThemePickerRow: View {
    @Binding var themeKey: String

    var body: some View {
        HStack {
            Text("Theme").font(.callout)
            Spacer()
            Picker("", selection: $themeKey) {
                ForEach(appThemes) { t in
                    HStack(spacing: 6) {
                        Circle()
                            .fill(t.accent)
                            .frame(width: 10, height: 10)
                        Text(t.name)
                    }
                    .tag(t.key)
                }
            }
            .pickerStyle(.menu)
            .fixedSize()
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
        Divider().padding(.leading, 14)
    }
}

private struct PickerRow: View {
    let label: String
    @Binding var selection: String
    let options: [(String, String)]

    var body: some View {
        HStack {
            Text(label).font(.callout)
            Spacer()
            Picker("", selection: $selection) {
                ForEach(options, id: \.0) { value, display in
                    Text(display).tag(value)
                }
            }
            .pickerStyle(.menu)
            .fixedSize()
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
        Divider().padding(.leading, 14)
    }
}
