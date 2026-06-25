import Foundation

// MARK: - Models (same shape as before — UI is unchanged)

struct StorageData {
    let totalGB: Double
    let usedGB:  Double
    let freeGB:  Double
    let usedPct: Double
}

struct ScanCategory: Identifiable {
    var id: String { category }
    let category: String
    let count:    Int
    let sizeMB:   Double
    let paths:    [String]
}

struct ScanData {
    let totalSizeGB: Double
    let totalCount:  Int
    let results:     [ScanCategory]
}

struct CleanData {
    let movedCount: Int
}

struct FolderNode: Identifiable {
    let id = UUID()
    let url: URL
    let name: String
    let sizeMB: Double
    let displayPath: String
    var children: [FolderNode]
}

struct EngineResponse<T> {
    let status:  String
    let data:    T?
    let message: String?
}

// MARK: - ScanEngine actor (thin wrapper over NativeEngine — no subprocess)

actor ScanEngine {
    static let shared = ScanEngine()

    func storage() async -> EngineResponse<StorageData>? {
        let data = await NativeEngine.shared.storageInfo()
        return EngineResponse(status: "ok", data: data, message: nil)
    }

    func scan(categories: [String]? = nil) async -> EngineResponse<ScanData>? {
        let data = await NativeEngine.shared.runScan(categories: categories)
        return EngineResponse(status: "ok", data: data, message: nil)
    }

    func clean(paths: [String]) async -> EngineResponse<CleanData>? {
        let data = await NativeEngine.shared.runClean(paths: paths)
        return EngineResponse(status: "ok", data: data, message: nil)
    }

    func largeFolders() async -> [FolderNode] {
        await NativeEngine.shared.largeFolders()
    }
}
