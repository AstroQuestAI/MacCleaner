import Foundation

// MARK: - Engine models (mirrors engine_cli.py JSON)

struct StorageData: Decodable {
    let totalGB: Double
    let usedGB:  Double
    let freeGB:  Double
    let usedPct: Double

    enum CodingKeys: String, CodingKey {
        case totalGB = "total_gb"
        case usedGB  = "used_gb"
        case freeGB  = "free_gb"
        case usedPct = "used_pct"
    }
}

struct ScanCategory: Decodable, Identifiable {
    var id: String { category }
    let category: String
    let count:    Int
    let sizeMB:   Double
    let paths:    [String]

    enum CodingKeys: String, CodingKey {
        case category, count, paths
        case sizeMB = "size_mb"
    }
}

struct ScanData: Decodable {
    let totalSizeGB: Double
    let totalCount:  Int
    let results:     [ScanCategory]

    enum CodingKeys: String, CodingKey {
        case results, totalCount = "total_count"
        case totalSizeGB = "total_size_gb"
    }
}

struct CleanData: Decodable {
    let movedCount: Int
    enum CodingKeys: String, CodingKey { case movedCount = "moved_count" }
}

// Generic engine response
struct EngineResponse<T: Decodable>: Decodable {
    let status: String
    let data:   T?
    let message: String?
}

// MARK: - ScanEngine actor

actor ScanEngine {
    static let shared = ScanEngine()

    // Path to the embedded engine binary inside the .app bundle
    private var engineURL: URL {
        // During development, look next to the Swift binary
        let devPath = Bundle.main.bundleURL
            .deletingLastPathComponent()
            .appendingPathComponent("maccleaner-engine")
        if FileManager.default.fileExists(atPath: devPath.path) { return devPath }

        // In the shipped .app: Contents/MacOS/maccleaner-engine
        return Bundle.main.bundleURL
            .appendingPathComponent("Contents/MacOS/maccleaner-engine")
    }

    // MARK: Public commands

    func storage() async -> EngineResponse<StorageData>? {
        await send(cmd: ["cmd": "storage"])
    }

    func scan(categories: [String]? = nil) async -> EngineResponse<ScanData>? {
        var cmd: [String: Any] = ["cmd": "scan"]
        if let cats = categories { cmd["categories"] = cats }
        return await send(cmd: cmd)
    }

    func clean(paths: [String]) async -> EngineResponse<CleanData>? {
        await send(cmd: ["cmd": "clean", "paths": paths])
    }

    // MARK: Private transport

    private func send<T: Decodable>(cmd: [String: Any]) async -> EngineResponse<T>? {
        guard FileManager.default.isExecutableFile(atPath: engineURL.path) else {
            print("[ScanEngine] engine not found at \(engineURL.path)")
            return nil
        }

        let proc  = Process()
        let stdin  = Pipe()
        let stdout = Pipe()

        proc.executableURL          = engineURL
        proc.standardInput          = stdin
        proc.standardOutput         = stdout
        proc.standardError          = FileHandle.nullDevice

        do { try proc.run() } catch {
            print("[ScanEngine] launch failed: \(error)")
            return nil
        }

        // Write command JSON + quit
        let quitLine  = try! JSONSerialization.data(withJSONObject: ["cmd": "quit"])
        let cmdLine   = try! JSONSerialization.data(withJSONObject: cmd)
        stdin.fileHandleForWriting.write(cmdLine + "\n".data(using: .utf8)!)
        stdin.fileHandleForWriting.write(quitLine + "\n".data(using: .utf8)!)
        stdin.fileHandleForWriting.closeFile()

        let output = stdout.fileHandleForReading.readDataToEndOfFile()
        proc.waitUntilExit()

        // First line is the response to our command
        guard let firstLine = output.split(separator: UInt8(ascii: "\n")).first else { return nil }
        return try? JSONDecoder().decode(EngineResponse<T>.self, from: Data(firstLine))
    }
}
