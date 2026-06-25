import SwiftUI
import FoundationModels

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

    // AI per-category advice
    @Published var aiAdvice: [String: CategoryAdvice] = [:]
    @Published var isAnalyzing = false

    // Storage large-folder tree
    @Published var largeFolders: [FolderNode] = []
    @Published var isLoadingFolders = false

    func runScan() async {
        isScanning = true
        aiAdvice   = [:]
        defer { isScanning = false }
        let resp = await ScanEngine.shared.scan()
        if let data = resp?.data {
            scanData = data
            Task { await analyzeWithAI(data.results) }
        }
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
        await loadLargeFolders()
    }

    func loadLargeFolders() async {
        isLoadingFolders = true
        defer { isLoadingFolders = false }
        largeFolders = await ScanEngine.shared.largeFolders()
    }

    func deleteFolder(_ node: FolderNode) async {
        _ = await ScanEngine.shared.clean(paths: [node.url.path])
        let resp = await ScanEngine.shared.storage()
        if let data = resp?.data { storageData = data }
        await loadLargeFolders()
    }

    // MARK: AI analysis — runs after every scan

    private func analyzeWithAI(_ categories: [ScanCategory]) async {
        let nonEmpty = categories.filter { !$0.paths.isEmpty }
        guard !nonEmpty.isEmpty else { return }

        isAnalyzing = true
        defer { isAnalyzing = false }

        let useAI: Bool
        if #available(macOS 26, *),
           case .available = SystemLanguageModel.default.availability {
            useAI = true
        } else {
            useAI = false
        }

        if useAI, #available(macOS 26, *) {
            for cat in nonEmpty {
                let safety   = ScanAdvisor.safety(for: cat.category)
                let fallback = ScanAdvisor.fallback(for: cat.category)
                let prompt   = ScanAdvisor.prompt(for: cat)
                do {
                    let session  = LanguageModelSession(instructions: ScanAdvisor.instructions)
                    let response = try await session.respond(to: prompt)
                    let text     = response.content.trimmingCharacters(in: .whitespacesAndNewlines)
                    aiAdvice[cat.category] = CategoryAdvice(safety: safety,
                                                            text: text.isEmpty ? fallback : text)
                } catch {
                    aiAdvice[cat.category] = CategoryAdvice(safety: safety, text: fallback)
                }
            }
        } else {
            for cat in nonEmpty {
                aiAdvice[cat.category] = CategoryAdvice(
                    safety: ScanAdvisor.safety(for: cat.category),
                    text:   ScanAdvisor.fallback(for: cat.category)
                )
            }
        }
    }
}

// MARK: - Root view

struct MainView: View {
    @StateObject var vm: MainViewModel
    @AppStorage("themeKey") private var themeKey = "glass"

    private var accentColor: Color { theme(for: themeKey).accent }

    var body: some View {
        HStack(spacing: 0) {
            sidebar
            Divider()
            content
        }
        .frame(minWidth: 680, minHeight: 460)
        .background(Color(nsColor: .windowBackgroundColor))
        .tint(accentColor)
        .task { await vm.refreshStorage() }
    }

    // MARK: Sidebar
    private var sidebar: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("MacCleaner")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(
                    LinearGradient(colors: [accentColor, accentColor.opacity(0.6)],
                                   startPoint: .leading, endPoint: .trailing)
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
        Button { activeTab = tab } label: {
            HStack(spacing: 10) {
                Image(systemName: icon)
                    .foregroundStyle(isActive ? Color.accentColor : Color.secondary)
                    .frame(width: 20)
                Text(label)
                    .font(.system(size: 13, weight: isActive ? .semibold : .regular))
                    .foregroundStyle(isActive ? Color.primary : Color.secondary)
                Spacer()
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 7)
            .background(isActive ? Color.accentColor.opacity(0.12) : Color.clear)
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
                .tint(usedPct > 0.8 ? .red : .accentColor)
            Text(String(format: "%.0f GB free", freeGB))
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}

// MARK: - Clean tab

struct CleanTabView: View {
    @ObservedObject var vm: MainViewModel

    private var foundCategories: [ScanCategory] {
        vm.scanData?.results.filter { !$0.paths.isEmpty } ?? []
    }
    private var emptyCategories: [ScanCategory] {
        vm.scanData?.results.filter { $0.paths.isEmpty } ?? []
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {

            // ── Header ──────────────────────────────────────────────────────
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text("Junk Files").font(.title2).bold()
                    if vm.isAnalyzing {
                        HStack(spacing: 4) {
                            ProgressView().scaleEffect(0.5)
                            Text("Apple Intelligence is reviewing…")
                                .font(.caption2).foregroundStyle(.secondary)
                        }
                    }
                }
                Spacer()
                if vm.isScanning { ProgressView().scaleEffect(0.7) }
                Button(vm.isScanning ? "Scanning…" : "Scan Now") {
                    Task { await vm.runScan() }
                }
                .buttonStyle(.borderedProminent)
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

            // ── Results ─────────────────────────────────────────────────────
            if let _ = vm.scanData {
                if foundCategories.isEmpty {
                    ContentUnavailableView("Your Mac looks clean!",
                        systemImage: "sparkles",
                        description: Text("Nothing found across all 14 scanner categories."))
                } else {
                    List {
                        // Categories with junk found
                        Section {
                            ForEach(foundCategories) { cat in
                                CategoryRow(cat: cat,
                                            selectedPaths: $vm.selectedPaths,
                                            advice: vm.aiAdvice[cat.category],
                                            isAnalyzing: vm.isAnalyzing && vm.aiAdvice[cat.category] == nil)
                            }
                        }

                        // Empty categories — proof the scan was thorough
                        if !emptyCategories.isEmpty {
                            Section {
                                VStack(alignment: .leading, spacing: 6) {
                                    Text("Also checked — nothing found")
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                    Text(emptyCategories.map(\.category).joined(separator: "  ·  "))
                                        .font(.caption2)
                                        .foregroundStyle(.tertiary)
                                }
                                .padding(.vertical, 4)
                                .listRowBackground(Color.clear)
                            }
                        }
                    }
                }
            } else {
                ContentUnavailableView(
                    "No scan yet",
                    systemImage: "sparkles.rectangle.stack",
                    description: Text("Tap Scan Now — Apple Intelligence will advise on every category.")
                )
            }
        }
    }
}

// MARK: - Category row with AI advice

private struct CategoryRow: View {
    let cat: ScanCategory
    @Binding var selectedPaths: Set<String>
    let advice: CategoryAdvice?
    let isAnalyzing: Bool

    private var isSelected: Bool {
        cat.paths.allSatisfy { selectedPaths.contains($0) }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {

            // Category summary row
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
                    Text("\(cat.count) \(cat.count == 1 ? "item" : "items")")
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                Text(sizeLabel(cat.sizeMB))
                    .font(.system(.body, design: .monospaced))
                    .foregroundStyle(.secondary)
            }

            // AI advice row
            if isAnalyzing {
                HStack(spacing: 5) {
                    ProgressView().scaleEffect(0.55)
                    Text("Analyzing…")
                        .font(.caption2).foregroundStyle(.tertiary)
                }
                .padding(.leading, 28)
            } else if let adv = advice {
                HStack(alignment: .top, spacing: 5) {
                    Image(systemName: adv.safety.icon)
                        .foregroundStyle(adv.safety.color)
                        .font(.caption)
                        .padding(.top, 1)
                    VStack(alignment: .leading, spacing: 1) {
                        Text(adv.safety.label)
                            .font(.caption2).bold()
                            .foregroundStyle(adv.safety.color)
                        Text(adv.text)
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
                .padding(.leading, 28)
            }
        }
        .padding(.vertical, 4)
    }

    private func sizeLabel(_ mb: Double) -> String {
        mb >= 1000
            ? String(format: "%.1f GB", mb / 1000)
            : String(format: "%.1f MB", mb)
    }
}

// MARK: - Storage tab

struct StorageTabView: View {
    @ObservedObject var vm: MainViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text("Storage").font(.title2).bold()
                Spacer()
                if vm.isLoadingFolders { ProgressView().scaleEffect(0.65) }
                Button("Refresh") { Task { await vm.refreshStorage() } }
                    .buttonStyle(.bordered)
            }
            .padding()

            Divider()

            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    if let st = vm.storageData {
                        DiskUsageCard(st: st)
                    }

                    if !vm.largeFolders.isEmpty {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Large Folders")
                                .font(.headline)
                            FolderTable(folders: vm.largeFolders, vm: vm)
                        }
                    } else if vm.isLoadingFolders {
                        HStack { Spacer(); ProgressView("Scanning folders…"); Spacer() }
                            .padding(.top, 40)
                    } else if vm.storageData != nil {
                        ContentUnavailableView("No large folders found",
                            systemImage: "folder",
                            description: Text("No folders over 100 MB in common locations."))
                    }
                }
                .padding()
            }
        }
    }
}

// MARK: - Disk usage card

private struct DiskUsageCard: View {
    let st: StorageData

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Disk Usage").font(.headline)
            ProgressView(value: st.usedPct / 100)
                .tint(st.usedPct > 80 ? .red : .accentColor)
                .scaleEffect(x: 1, y: 2, anchor: .center)
            HStack {
                Label(String(format: "%.1f GB used", st.usedGB), systemImage: "internaldrive")
                Spacer()
                Label(String(format: "%.1f GB free", st.freeGB), systemImage: "checkmark.circle")
                    .foregroundStyle(.green)
            }
            .font(.callout)
            Text(String(format: "%.0f%%  of  %.0f GB total", st.usedPct, st.totalGB))
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding(16)
        .background(Color(nsColor: .controlBackgroundColor), in: RoundedRectangle(cornerRadius: 10))
    }
}

// MARK: - Folder table (flat list, rows collapse/expand inline)

private let sizeColWidth: CGFloat = 74
private let actionColWidth: CGFloat = 32

private func folderSizeLabel(_ mb: Double) -> String {
    mb >= 1000 ? String(format: "%.1f GB", mb / 1000) : String(format: "%.0f MB", mb)
}

private struct FolderTable: View {
    let folders: [FolderNode]
    @ObservedObject var vm: MainViewModel

    var body: some View {
        VStack(spacing: 0) {
            // Single header row
            HStack {
                Text("FOLDER")
                    .font(.system(size: 10, weight: .semibold))
                    .foregroundStyle(.secondary)
                    .tracking(0.4)
                Spacer()
                Text("SIZE")
                    .font(.system(size: 10, weight: .semibold))
                    .foregroundStyle(.secondary)
                    .tracking(0.4)
                    .frame(width: sizeColWidth, alignment: .trailing)
                Spacer().frame(width: actionColWidth)
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 7)

            Divider()

            ForEach(Array(folders.enumerated()), id: \.element.id) { idx, node in
                FolderSection(node: node, vm: vm)
                if idx < folders.count - 1 { Divider() }
            }
        }
        .background(Color(nsColor: .controlBackgroundColor))
        .clipShape(RoundedRectangle(cornerRadius: 10))
        .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color(nsColor: .separatorColor), lineWidth: 0.5))
    }
}

// Top-level folder — collapsed by default, expands child rows inline
private struct FolderSection: View {
    let node: FolderNode
    @ObservedObject var vm: MainViewModel
    @State private var expanded = false
    @State private var confirmDelete = false

    var body: some View {
        VStack(spacing: 0) {
            FolderRowCell(name: node.name, displayPath: node.displayPath,
                          sizeMB: node.sizeMB, indent: 0, isTopLevel: true,
                          hasChildren: !node.children.isEmpty,
                          expanded: $expanded) { confirmDelete = true }

            if expanded, !node.children.isEmpty {
                ForEach(Array(node.children.enumerated()), id: \.element.id) { idx, child in
                    Divider().padding(.leading, 40)
                    ChildSection(node: child, vm: vm, indent: 1)
                }
            }
        }
        .confirmationDialog("Move \"\(node.name)\" to Trash?",
                            isPresented: $confirmDelete, titleVisibility: .visible) {
            Button("Move to Trash", role: .destructive) { Task { await vm.deleteFolder(node) } }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Frees \(folderSizeLabel(node.sizeMB)). Can be restored from Trash.")
        }
    }
}

// Child row — also collapsed by default, can expand one more level
private struct ChildSection: View {
    let node: FolderNode
    @ObservedObject var vm: MainViewModel
    let indent: Int
    @State private var expanded = false
    @State private var confirmDelete = false

    var body: some View {
        VStack(spacing: 0) {
            FolderRowCell(name: node.name, displayPath: node.displayPath,
                          sizeMB: node.sizeMB, indent: indent, isTopLevel: false,
                          hasChildren: !node.children.isEmpty && indent < 3,
                          expanded: $expanded) { confirmDelete = true }
            .background(Color(nsColor: .windowBackgroundColor).opacity(Double(indent) * 0.3))

            if expanded, !node.children.isEmpty, indent < 3 {
                ForEach(Array(node.children.enumerated()), id: \.element.id) { idx, grandchild in
                    Divider().padding(.leading, CGFloat(indent + 1) * 24 + 16)
                    ChildSection(node: grandchild, vm: vm, indent: indent + 1)
                }
            }
        }
        .confirmationDialog("Move \"\(node.name)\" to Trash?",
                            isPresented: $confirmDelete, titleVisibility: .visible) {
            Button("Move to Trash", role: .destructive) { Task { await vm.deleteFolder(node) } }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Frees \(folderSizeLabel(node.sizeMB)). Can be restored from Trash.")
        }
    }
}

// Shared row cell — same column layout at every level
private struct FolderRowCell: View {
    let name: String
    let displayPath: String
    let sizeMB: Double
    let indent: Int
    let isTopLevel: Bool
    let hasChildren: Bool
    @Binding var expanded: Bool
    let onDelete: () -> Void

    var body: some View {
        HStack(spacing: 8) {
            if indent > 0 { Spacer().frame(width: CGFloat(indent) * 24) }

            Button {
                withAnimation(.easeInOut(duration: 0.15)) { expanded.toggle() }
            } label: {
                Image(systemName: expanded ? "chevron.down" : "chevron.right")
                    .font(isTopLevel ? .caption2 : .system(size: 9))
                    .foregroundStyle(.secondary)
                    .frame(width: 12)
            }
            .buttonStyle(.plain)
            .opacity(hasChildren ? 1 : 0)

            Image(systemName: isTopLevel ? "folder.fill" : "folder")
                .foregroundStyle(isTopLevel ? Color.accentColor : Color.secondary)
                .font(isTopLevel ? .body : .callout)

            Text(name)
                .font(isTopLevel ? .headline : .callout)
                .lineLimit(1)
                .help(displayPath)

            Spacer()

            Text(folderSizeLabel(sizeMB))
                .font(.system(isTopLevel ? .callout : .caption, design: .monospaced))
                .foregroundStyle(isTopLevel ? .primary : .secondary)
                .frame(width: sizeColWidth, alignment: .trailing)

            Button { onDelete() } label: {
                Image(systemName: "trash")
                    .font(.system(size: isTopLevel ? 12 : 10))
                    .foregroundStyle(.red.opacity(isTopLevel ? 0.7 : 0.55))
            }
            .buttonStyle(.plain)
            .help("Move \"\(name)\" to Trash")
            .frame(width: actionColWidth)
        }
        .padding(.horizontal, 14)
        .padding(.vertical, isTopLevel ? 10 : 7)
    }
}
