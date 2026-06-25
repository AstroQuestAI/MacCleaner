import SwiftUI

enum AppTab { case clean, storage, ai, settings }

// MARK: - ViewModel

@MainActor
final class MainViewModel: ObservableObject {
    @Published var activeTab: AppTab   = .clean
    @Published var scanData: ScanData? = nil
    @Published var storageData: StorageData? = nil
    @Published var isScanning  = false
    @Published var isCleaning  = false
    @Published var selectedPaths: Set<String> = []

    func runScan() async {
        isScanning = true
        defer { isScanning = false }
        let resp = await ScanEngine.shared.scan()
        if let data = resp?.data { scanData = data }
    }

    func runClean() async {
        isCleaning = true
        defer { isCleaning = false }
        let paths = Array(selectedPaths)
        _ = await ScanEngine.shared.clean(paths: paths)
        selectedPaths = []
        await runScan()
        await refreshStorage()
    }

    func refreshStorage() async {
        let resp = await ScanEngine.shared.storage()
        if let data = resp?.data { storageData = data }
    }
}

// MARK: - Root view

struct MainView: View {
    @StateObject var vm: MainViewModel

    var body: some View {
        HStack(spacing: 0) {
            sidebar
            Divider()
            content
        }
        .frame(minWidth: 680, minHeight: 460)
        .background(Color(nsColor: .windowBackgroundColor))
        .task { await vm.refreshStorage() }
    }

    // MARK: Sidebar
    private var sidebar: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("MacCleaner")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(
                    LinearGradient(colors: [.purple, .pink], startPoint: .leading, endPoint: .trailing)
                )
                .padding(.horizontal, 16)
                .padding(.top, 20)
                .padding(.bottom, 8)

            SidebarRow(icon: "trash.circle.fill",  label: "Clean",    tab: .clean,    activeTab: $vm.activeTab)
            SidebarRow(icon: "internaldrive.fill",  label: "Storage",  tab: .storage,  activeTab: $vm.activeTab)
            SidebarRow(icon: "sparkles",            label: "Ask AI",   tab: .ai,       activeTab: $vm.activeTab)
            SidebarRow(icon: "gearshape.fill",      label: "Settings", tab: .settings, activeTab: $vm.activeTab)

            Spacer()

            if let st = vm.storageData {
                StorageMiniBar(usedPct: st.usedPct / 100, freeGB: st.freeGB)
                    .padding(12)
            }
        }
        .frame(width: 180)
        .background(Color(nsColor: .controlBackgroundColor))
    }

    // MARK: Content
    @ViewBuilder
    private var content: some View {
        switch vm.activeTab {
        case .clean:    CleanTabView(vm: vm)
        case .storage:  StorageTabView(vm: vm)
        case .ai:       AIAssistantView()
        case .settings: SettingsTabView()
        }
    }
}

// MARK: - Sidebar row

private struct SidebarRow: View {
    let icon:  String
    let label: String
    let tab:   AppTab
    @Binding var activeTab: AppTab

    var isActive: Bool { activeTab == tab }

    var body: some View {
        Button {
            activeTab = tab
        } label: {
            HStack(spacing: 10) {
                Image(systemName: icon)
                    .foregroundStyle(isActive ? Color.purple : Color.secondary)
                    .frame(width: 20)
                Text(label)
                    .font(.system(size: 13, weight: isActive ? .semibold : .regular))
                    .foregroundStyle(isActive ? Color.primary : Color.secondary)
                Spacer()
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 7)
            .background(isActive ? Color.purple.opacity(0.12) : Color.clear)
            .cornerRadius(8)
        }
        .buttonStyle(.plain)
        .padding(.horizontal, 8)
    }
}

// MARK: - Storage mini bar

private struct StorageMiniBar: View {
    let usedPct: Double
    let freeGB:  Double

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            ProgressView(value: usedPct)
                .tint(usedPct > 0.8 ? .red : .purple)
            Text(String(format: "%.0f GB free", freeGB))
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}

// MARK: - Clean tab

struct CleanTabView: View {
    @ObservedObject var vm: MainViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text("Junk Files")
                    .font(.title2).bold()
                Spacer()
                if vm.isScanning {
                    ProgressView().scaleEffect(0.7)
                }
                Button(vm.isScanning ? "Scanning…" : "Scan Now") {
                    Task { await vm.runScan() }
                }
                .buttonStyle(.borderedProminent)
                .tint(.purple)
                .disabled(vm.isScanning)

                if !vm.selectedPaths.isEmpty {
                    Button("Clean Selected (\(vm.selectedPaths.count))") {
                        Task { await vm.runClean() }
                    }
                    .buttonStyle(.bordered)
                    .disabled(vm.isCleaning)
                }
            }
            .padding()

            Divider()

            if let data = vm.scanData {
                List(data.results) { cat in
                    CategoryRow(cat: cat, selectedPaths: $vm.selectedPaths)
                }
            } else {
                ContentUnavailableView(
                    "No scan yet",
                    systemImage: "sparkles.rectangle.stack",
                    description: Text("Tap Scan Now to find junk")
                )
            }
        }
    }
}

private struct CategoryRow: View {
    let cat: ScanCategory
    @Binding var selectedPaths: Set<String>

    private var isSelected: Bool {
        cat.paths.allSatisfy { selectedPaths.contains($0) }
    }

    var body: some View {
        HStack {
            Toggle("", isOn: Binding(
                get: { isSelected },
                set: { sel in
                    if sel { cat.paths.forEach { selectedPaths.insert($0) } }
                    else   { cat.paths.forEach { selectedPaths.remove($0) } }
                }
            ))
            .labelsHidden()

            VStack(alignment: .leading, spacing: 2) {
                Text(cat.category).font(.headline)
                Text("\(cat.count) files").font(.caption).foregroundStyle(.secondary)
            }
            Spacer()
            Text(String(format: "%.1f MB", cat.sizeMB))
                .font(.system(.body, design: .monospaced))
                .foregroundStyle(.secondary)
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Storage tab

struct StorageTabView: View {
    @ObservedObject var vm: MainViewModel

    var body: some View {
        VStack {
            if let st = vm.storageData {
                VStack(spacing: 16) {
                    Text("Disk Usage").font(.title2).bold()
                    ProgressView(value: st.usedPct / 100)
                        .tint(st.usedPct > 80 ? .red : .purple)
                        .scaleEffect(x: 1, y: 2, anchor: .center)

                    HStack {
                        Label(String(format: "%.1f GB used", st.usedGB), systemImage: "internaldrive")
                        Spacer()
                        Label(String(format: "%.1f GB free", st.freeGB), systemImage: "checkmark.circle")
                            .foregroundStyle(.green)
                    }
                    .font(.callout)
                }
                .padding(32)
            } else {
                ContentUnavailableView("Loading…", systemImage: "internaldrive")
                    .task { await vm.refreshStorage() }
            }
        }
    }
}

// MARK: - Settings tab (stub)

struct SettingsTabView: View {
    var body: some View {
        Text("Settings coming soon")
            .foregroundStyle(.secondary)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
