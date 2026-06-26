// Engine.swift — Pure Swift scanning engine. No Python. No subprocess. No pip.
// FileManager + CryptoKit replace the entire Python engine layer.

import Foundation
import CryptoKit

// MARK: - Helpers

private let fm = FileManager.default

private func urlExists(_ url: URL) -> Bool {
    fm.fileExists(atPath: url.path)
}

private func isDir(_ url: URL) -> Bool {
    var b: ObjCBool = false
    fm.fileExists(atPath: url.path, isDirectory: &b)
    return b.boolValue
}

private func recursiveSize(_ url: URL) -> Int64 {
    var b: ObjCBool = false
    guard fm.fileExists(atPath: url.path, isDirectory: &b) else { return 0 }
    if b.boolValue {
        guard let e = fm.enumerator(at: url, includingPropertiesForKeys: [.fileSizeKey]) else { return 0 }
        var total: Int64 = 0
        for case let f as URL in e {
            total += Int64((try? f.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0)
        }
        return total
    }
    return Int64((try? url.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0)
}

// MARK: - Scanner protocol

private protocol FileScanner {
    var categoryName: String { get }
    func findPaths() -> [URL]
}

// MARK: - NativeEngine

actor NativeEngine {
    static let shared = NativeEngine()
    private let home = fm.homeDirectoryForCurrentUser

    // MARK: Storage

    func storageInfo() -> StorageData {
        guard
            let attrs = try? fm.attributesOfFileSystem(forPath: home.path),
            let total = (attrs[.systemSize] as? NSNumber)?.int64Value,
            let free  = (attrs[.systemFreeSize] as? NSNumber)?.int64Value
        else { return StorageData(totalGB: 0, usedGB: 0, freeGB: 0, usedPct: 0) }

        let used = total - free
        return StorageData(
            totalGB: Double(total) / 1e9,
            usedGB:  Double(used)  / 1e9,
            freeGB:  Double(free)  / 1e9,
            usedPct: total > 0 ? Double(used) / Double(total) * 100 : 0
        )
    }

    // MARK: Large folders

    func largeFolders() -> [FolderNode] {
        let topNames = [
            "Library", "Documents", "Downloads", "Desktop",
            "Movies", "Music", "Pictures", "Developer",
            "Projects", "repos", "code", "workspace", "src",
        ]
        var nodes: [FolderNode] = []
        for name in topNames {
            let dir = home.appendingPathComponent(name)
            guard urlExists(dir), isDir(dir) else { continue }
            let sizeMB = Double(recursiveSize(dir)) / 1_000_000
            guard sizeMB >= 100 else { continue }
            let children = buildFolderChildren(of: dir, depth: 1, maxDepth: 3)
            let rel = "~/" + name
            nodes.append(FolderNode(url: dir, name: name, sizeMB: sizeMB, displayPath: rel, children: children))
        }
        return nodes.sorted { $0.sizeMB > $1.sizeMB }
    }

    private func buildFolderChildren(of dir: URL, depth: Int, maxDepth: Int) -> [FolderNode] {
        guard depth <= maxDepth,
              let entries = try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil)
        else { return [] }
        let homePath = home.path
        var children: [FolderNode] = []
        for entry in entries where isDir(entry) && !entry.lastPathComponent.hasPrefix(".") {
            let sizeMB = Double(recursiveSize(entry)) / 1_000_000
            guard sizeMB >= 50 else { continue }
            let sub = depth < maxDepth ? buildFolderChildren(of: entry, depth: depth + 1, maxDepth: maxDepth) : []
            let rel = entry.path.hasPrefix(homePath + "/")
                ? "~" + String(entry.path.dropFirst(homePath.count))
                : entry.path
            children.append(FolderNode(url: entry, name: entry.lastPathComponent,
                                       sizeMB: sizeMB, displayPath: rel, children: sub))
        }
        return Array(children.sorted { $0.sizeMB > $1.sizeMB }.prefix(8))
    }

    // MARK: Scan

    func runScan(categories: [String]? = nil) -> ScanData {
        let scanners: [any FileScanner] = [
            UserCacheScanner(home: home),
            BrowserCacheScanner(home: home),
            XcodeScanner(home: home),
            LogScanner(home: home),
            TrashScanner(home: home),
            TempScanner(),
            NodeCacheScanner(home: home),
            NodeModulesScanner(home: home),
            BuildCacheScanner(home: home),
            HomebrewScanner(home: home),
            MailScanner(home: home),
            PythonCacheScanner(home: home),
            VenvScanner(home: home),
            DuplicateScanner(home: home),
        ]

        var results: [ScanCategory] = []

        for scanner in scanners {
            if let filter = categories, !filter.contains(scanner.categoryName) { continue }
            let paths = scanner.findPaths()
            let totalBytes = paths.reduce(Int64(0)) { $0 + recursiveSize($1) }
            results.append(ScanCategory(
                category: scanner.categoryName,
                count:    paths.count,
                sizeMB:   Double(totalBytes) / 1_000_000,
                paths:    paths.map(\.path)
            ))
        }

        // Docker: always included even if nothing reclaimable
        if categories == nil || categories?.contains("Docker") == true {
            let docker = DockerScanner().scan() ?? ScanCategory(category: "Docker", count: 0, sizeMB: 0, paths: [])
            results.append(docker)
        }

        let totalGB    = results.reduce(0.0) { $0 + $1.sizeMB } / 1000.0
        let totalCount = results.reduce(0)   { $0 + $1.count }
        return ScanData(totalSizeGB: totalGB, totalCount: totalCount, results: results)
    }

    // MARK: Clean

    func runClean(paths: [String]) -> CleanData {
        var moved = 0
        for path in paths {
            if path == "__docker_prune__" {
                let p = Process()
                p.executableURL = URL(fileURLWithPath: "/usr/bin/env")
                p.arguments = ["docker", "system", "prune", "-f"]
                p.standardOutput = FileHandle.nullDevice
                p.standardError  = FileHandle.nullDevice
                try? p.run(); p.waitUntilExit()
                moved += 1
                continue
            }
            let url = URL(fileURLWithPath: path)
            // Items already in .Trash — permanently delete (they were already "trashed")
            if path.contains("/.Trash/") {
                if (try? fm.removeItem(at: url)) != nil { moved += 1 }
            } else {
                var out: NSURL?
                if (try? fm.trashItem(at: url, resultingItemURL: &out)) != nil { moved += 1 }
            }
        }
        return CleanData(movedCount: moved)
    }
}

// MARK: - Scanners

private struct UserCacheScanner: FileScanner {
    let home: URL
    let categoryName = "User Caches"

    func findPaths() -> [URL] {
        let dir = home.appendingPathComponent("Library/Caches")
        guard let entries = try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil) else { return [] }
        return entries.filter {
            let name = $0.lastPathComponent
            return isDir($0) && name.contains(".") && name != "com.apple.Safari"
        }
    }
}

private struct BrowserCacheScanner: FileScanner {
    let home: URL
    let categoryName = "Browser Caches"

    private let rels = [
        "Library/Caches/com.apple.Safari",
        "Library/Caches/Google/Chrome/Default/Cache",
        "Library/Application Support/Google/Chrome/Default/Code Cache",
        "Library/Caches/BraveSoftware/Brave-Browser/Default/Cache",
        "Library/Caches/Firefox",
        "Library/Caches/Microsoft Edge/Default/Cache",
    ]

    func findPaths() -> [URL] {
        rels.compactMap {
            let u = home.appendingPathComponent($0)
            return urlExists(u) ? u : nil
        }
    }
}

private struct XcodeScanner: FileScanner {
    let home: URL
    let categoryName = "Xcode Artifacts"

    func findPaths() -> [URL] {
        var paths: [URL] = []

        for rel in ["Library/Developer/Xcode/DerivedData",
                    "Library/Developer/Xcode/Archives",
                    "Library/Developer/Xcode/iOS Device Logs"] {
            let u = home.appendingPathComponent(rel)
            if urlExists(u) { paths.append(u) }
        }

        // Each simulator device is its own directory
        let sims = home.appendingPathComponent("Library/Developer/CoreSimulator/Devices")
        if let entries = try? fm.contentsOfDirectory(at: sims, includingPropertiesForKeys: nil) {
            paths.append(contentsOf: entries.filter { isDir($0) })
        }

        // Each iPhone backup is its own directory
        let backups = home.appendingPathComponent("Library/Application Support/MobileSync/Backup")
        if let entries = try? fm.contentsOfDirectory(at: backups, includingPropertiesForKeys: nil) {
            paths.append(contentsOf: entries.filter { isDir($0) })
        }

        return paths
    }
}

private struct LogScanner: FileScanner {
    let home: URL
    let categoryName = "System Logs"

    func findPaths() -> [URL] {
        var paths: [URL] = []

        // Per-app logs in ~/Library/Logs
        let userLogs = home.appendingPathComponent("Library/Logs")
        if let entries = try? fm.contentsOfDirectory(at: userLogs, includingPropertiesForKeys: nil) {
            paths.append(contentsOf: entries)
        }

        // /private/var/log — only .log files owned by the current user
        let sysLogs = URL(fileURLWithPath: "/private/var/log")
        let uid = getuid()
        if let entries = try? fm.contentsOfDirectory(at: sysLogs, includingPropertiesForKeys: nil) {
            for u in entries where u.pathExtension == "log" {
                if let owner = (try? fm.attributesOfItem(atPath: u.path))?[.ownerAccountID] as? Int,
                   UInt32(owner) == uid {
                    paths.append(u)
                }
            }
        }

        return paths
    }
}

private struct TrashScanner: FileScanner {
    let home: URL
    let categoryName = "Trash"

    func findPaths() -> [URL] {
        // Try the standard path first
        let trash = home.appendingPathComponent(".Trash")
        if let entries = try? fm.contentsOfDirectory(at: trash, includingPropertiesForKeys: [.fileSizeKey, .isDirectoryKey]) {
            return entries.filter { $0.lastPathComponent != ".DS_Store" }
        }
        // Fall back to FileManager API (works with Full Disk Access)
        if let trashURL = try? fm.url(for: .trashDirectory, in: .userDomainMask, appropriateFor: nil, create: false),
           let entries = try? fm.contentsOfDirectory(at: trashURL, includingPropertiesForKeys: [.fileSizeKey, .isDirectoryKey]) {
            return entries.filter { $0.lastPathComponent != ".DS_Store" }
        }
        return []
    }
}

private struct TempScanner: FileScanner {
    let categoryName = "Temp Files"

    func findPaths() -> [URL] {
        var paths: [URL] = []

        let tmpPath = ProcessInfo.processInfo.environment["TMPDIR"] ?? "/private/var/folders"
        let tmpDir  = URL(fileURLWithPath: tmpPath)
        if let e = fm.enumerator(at: tmpDir, includingPropertiesForKeys: [.fileSizeKey]) {
            for case let u as URL in e {
                guard !isDir(u) else { continue }
                let size = (try? u.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0
                if size > 1024 { paths.append(u) }
                if paths.count >= 500 { break }
            }
        }

        let pTmp = URL(fileURLWithPath: "/private/tmp")
        if let entries = try? fm.contentsOfDirectory(at: pTmp, includingPropertiesForKeys: nil) {
            paths.append(contentsOf: entries.filter { !isDir($0) })
        }

        return paths
    }
}

private struct NodeCacheScanner: FileScanner {
    let home: URL
    let categoryName = "Node.js Cache"

    private let rels = [
        ".npm", ".yarn/cache", ".cache/yarn", ".pnpm-store",
        ".local/share/pnpm/store", ".bun/install/cache",
        ".cache/node-gyp", "Library/Caches/node-gyp",
    ]

    func findPaths() -> [URL] {
        rels.compactMap {
            let u = home.appendingPathComponent($0)
            return urlExists(u) ? u : nil
        }
    }
}

private struct NodeModulesScanner: FileScanner {
    let home: URL
    let categoryName = "Unused node_modules"
    private let unusedDays: Double = 30
    private let skipDirs: Set<String> = ["Library", "Applications"]

    func findPaths() -> [URL] {
        guard let topDirs = try? fm.contentsOfDirectory(at: home, includingPropertiesForKeys: nil)
        else { return [] }
        var found: [URL] = []
        for dir in topDirs where isDir(dir)
                               && !dir.lastPathComponent.hasPrefix(".")
                               && !skipDirs.contains(dir.lastPathComponent) {
            found.append(contentsOf: findNM(in: dir, depth: 5))
        }
        return found
    }

    private func findNM(in dir: URL, depth: Int) -> [URL] {
        guard depth > 0,
              let children = try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: [.contentModificationDateKey])
        else { return [] }
        var results: [URL] = []
        for child in children where isDir(child) {
            if child.lastPathComponent == "node_modules" {
                guard fm.fileExists(atPath: dir.appendingPathComponent("package.json").path) else { continue }
                let mtime = (try? dir.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? Date()
                if Date().timeIntervalSince(mtime) / 86400 >= unusedDays { results.append(child) }
            } else {
                results.append(contentsOf: findNM(in: child, depth: depth - 1))
            }
        }
        return results
    }
}

private struct BuildCacheScanner: FileScanner {
    let home: URL
    let categoryName = "Build Cache"

    private let rels = [
        ".gradle/caches", ".gradle/wrapper/dists", ".m2/repository",
        ".cargo/registry/cache", ".cargo/registry/src", ".cargo/git/db",
        ".cache/go-build", "go/pkg/mod/cache",
        "Library/Caches/CocoaPods",
        ".gem/cache", ".bundle/cache", ".composer/cache",
        ".nuget/packages", ".sonar/cache", ".pub-cache/hosted", ".swiftpm",
    ]

    func findPaths() -> [URL] {
        rels.compactMap {
            let u = home.appendingPathComponent($0)
            return urlExists(u) ? u : nil
        }
    }
}

private struct HomebrewScanner: FileScanner {
    let home: URL
    let categoryName = "Homebrew Cache"

    func findPaths() -> [URL] {
        var paths: [URL] = []
        let user = home.appendingPathComponent("Library/Caches/Homebrew")
        if urlExists(user) { paths.append(user) }
        for p in ["/opt/homebrew/Caches", "/usr/local/Homebrew/Cache"] {
            let u = URL(fileURLWithPath: p)
            if urlExists(u) { paths.append(u) }
        }
        return paths
    }
}

private struct MailScanner: FileScanner {
    let home: URL
    let categoryName = "Mail Downloads"

    private let rels = [
        "Library/Mail Downloads",
        "Library/Containers/com.apple.mail/Data/Library/Mail Downloads",
    ]

    func findPaths() -> [URL] {
        var results: [URL] = []
        for rel in rels {
            let dir = home.appendingPathComponent(rel)
            guard urlExists(dir),
                  let e = fm.enumerator(at: dir, includingPropertiesForKeys: nil) else { continue }
            for case let u as URL in e where !isDir(u) { results.append(u) }
        }
        return results
    }
}

private struct PythonCacheScanner: FileScanner {
    let home: URL
    let categoryName = "Python Cache"

    private let namedRels = [
        ".cache/pip", ".cache/pypoetry/cache", ".cache/uv",
        "Library/Caches/pip", ".cache/hatch", ".cache/pdm",
    ]
    private let searchRoots = [
        "Projects", "Developer", "code", "repos", "workspace",
        "Documents", "Desktop", "Sites",
    ]

    func findPaths() -> [URL] {
        var paths: [URL] = []

        for rel in namedRels {
            let u = home.appendingPathComponent(rel)
            if urlExists(u) { paths.append(u) }
        }

        // __pycache__ inside project directories (2 levels deep)
        for rootName in searchRoots {
            let root = home.appendingPathComponent(rootName)
            guard urlExists(root),
                  let projects = try? fm.contentsOfDirectory(at: root, includingPropertiesForKeys: nil) else { continue }
            for project in projects where isDir(project) {
                let pc1 = project.appendingPathComponent("__pycache__")
                if urlExists(pc1) { paths.append(pc1) }
                if let subs = try? fm.contentsOfDirectory(at: project, includingPropertiesForKeys: nil) {
                    for sub in subs where isDir(sub) {
                        let pc2 = sub.appendingPathComponent("__pycache__")
                        if urlExists(pc2) { paths.append(pc2) }
                    }
                }
            }
        }
        return paths
    }
}

private struct VenvScanner: FileScanner {
    let home: URL
    let categoryName = "Unused Venvs"
    private let unusedDays: Double = 60
    private let venvNames: Set<String> = [".venv", "venv", "env", ".env", "virtualenv"]
    private let skipDirs: Set<String> = ["Library", "Applications"]

    func findPaths() -> [URL] {
        guard let topDirs = try? fm.contentsOfDirectory(at: home, includingPropertiesForKeys: nil)
        else { return [] }
        var found: [URL] = []
        for dir in topDirs where isDir(dir)
                               && !dir.lastPathComponent.hasPrefix(".")
                               && !skipDirs.contains(dir.lastPathComponent) {
            found.append(contentsOf: findVenvs(in: dir, depth: 5))
        }
        return found
    }

    private func findVenvs(in dir: URL, depth: Int) -> [URL] {
        guard depth > 0,
              let children = try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: [.contentModificationDateKey])
        else { return [] }
        var results: [URL] = []
        for child in children where isDir(child) {
            if venvNames.contains(child.lastPathComponent) {
                let hasPy = fm.fileExists(atPath: child.appendingPathComponent("bin/python").path) ||
                            fm.fileExists(atPath: child.appendingPathComponent("bin/python3").path)
                guard hasPy else { continue }
                let mtime = (try? dir.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? Date()
                if Date().timeIntervalSince(mtime) / 86400 >= unusedDays { results.append(child) }
            } else {
                results.append(contentsOf: findVenvs(in: child, depth: depth - 1))
            }
        }
        return results
    }
}

private struct DuplicateScanner: FileScanner {
    let home: URL
    let categoryName = "Duplicate Files"

    private let scanRoots = ["Downloads", "Desktop", "Documents", "Pictures", "Movies"]
    private let scanExts: Set<String> = [
        "jpg", "jpeg", "png", "heic", "heif", "gif", "bmp", "tiff", "webp",
        "mp4", "mov", "m4v", "avi", "mkv",
        "pdf", "docx", "xlsx", "pptx", "zip", "dmg", "pkg",
    ]
    private let minSize = 512 * 1024  // 512 KB

    func findPaths() -> [URL] {
        var bySize: [Int: [URL]] = [:]

        for rootName in scanRoots {
            let root = home.appendingPathComponent(rootName)
            guard urlExists(root),
                  let e = fm.enumerator(at: root, includingPropertiesForKeys: [.fileSizeKey]) else { continue }
            for case let u as URL in e {
                guard !isDir(u), scanExts.contains(u.pathExtension.lowercased()) else { continue }
                let size = (try? u.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0
                if size >= minSize { bySize[size, default: []].append(u) }
            }
        }

        var duplicates: [URL] = []
        for (_, urls) in bySize where urls.count >= 2 {
            var byHash: [String: [URL]] = [:]
            for u in urls {
                if let h = sha256(u) { byHash[h, default: []].append(u) }
            }
            for group in byHash.values where group.count >= 2 {
                duplicates.append(contentsOf: group.sorted { $0.path < $1.path }.dropFirst())
            }
        }
        return duplicates
    }

    private func sha256(_ url: URL) -> String? {
        guard let handle = try? FileHandle(forReadingFrom: url) else { return nil }
        defer { try? handle.close() }
        var hasher = SHA256()
        while true {
            let chunk = handle.readData(ofLength: 131_072)
            if chunk.isEmpty { break }
            hasher.update(data: chunk)
        }
        return hasher.finalize().map { String(format: "%02x", $0) }.joined()
    }
}

// MARK: - Docker (special — runs CLI, not file paths)

private struct DockerScanner {
    func scan() -> ScanCategory? {
        guard commandExists("docker"), dockerRunning() else { return nil }
        let bytes = reclaimableBytes()
        guard bytes > 0 else { return nil }
        return ScanCategory(
            category: "Docker",
            count:    1,
            sizeMB:   Double(bytes) / 1_000_000,
            paths:    ["__docker_prune__"]
        )
    }

    private func commandExists(_ cmd: String) -> Bool {
        let p = Process()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/which")
        p.arguments = [cmd]
        p.standardOutput = FileHandle.nullDevice
        p.standardError  = FileHandle.nullDevice
        try? p.run(); p.waitUntilExit()
        return p.terminationStatus == 0
    }

    private func dockerRunning() -> Bool {
        let p = Process()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        p.arguments = ["docker", "info"]
        p.standardOutput = FileHandle.nullDevice
        p.standardError  = FileHandle.nullDevice
        guard (try? p.run()) != nil else { return false }
        p.waitUntilExit()
        return p.terminationStatus == 0
    }

    private func reclaimableBytes() -> Int64 {
        let p    = Process()
        let pipe = Pipe()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        p.arguments = ["docker", "system", "df"]
        p.standardOutput = pipe
        p.standardError  = FileHandle.nullDevice
        guard (try? p.run()) != nil else { return 0 }
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        p.waitUntilExit()
        guard let text = String(data: data, encoding: .utf8) else { return 0 }

        var total: Int64 = 0
        for line in text.components(separatedBy: "\n").dropFirst() {
            let parts = line.split(separator: " ", omittingEmptySubsequences: true)
            if parts.count >= 5 { total += parseSize(String(parts[4])) }
        }
        return total
    }

    private func parseSize(_ s: String) -> Int64 {
        let raw = s.components(separatedBy: " ").first ?? s
        let units: [(String, Int64)] = [
            ("TB", 1_000_000_000_000), ("GB", 1_000_000_000),
            ("MB", 1_000_000), ("KB", 1_000), ("B", 1),
        ]
        for (suffix, mul) in units {
            if let r = raw.range(of: suffix, options: .caseInsensitive) {
                if let v = Double(raw[..<r.lowerBound]) { return Int64(v * Double(mul)) }
            }
        }
        return 0
    }
}
