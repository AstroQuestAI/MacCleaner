/// maccleaner-ai — thin Foundation Models bridge for MacCleaner.
/// Compiled with swiftc (no Xcode needed). No SwiftUI, no macros.
///
/// Protocol (stdin → stdout, one JSON object per line):
///   {"cmd":"available"}
///   {"cmd":"summarize","context":"...scan text..."}
///   {"cmd":"explain","category":"Xcode Artifacts","size_mb":18432,"count":1234}
///   {"cmd":"advise","categories":["User Caches","Xcode Artifacts"],"total_gb":19.2}
///   {"cmd":"notify","total_gb":4.2,"top_category":"Xcode Artifacts","top_gb":18.0}
///
/// Response always:
///   {"status":"ok","text":"..."}   or   {"status":"unavailable","reason":"..."}

import Foundation
import FoundationModels

// ── JSON helpers ──────────────────────────────────────────────────────────

func jsonLine(_ dict: [String: Any]) -> String {
    let data = try! JSONSerialization.data(withJSONObject: dict)
    return String(data: data, encoding: .utf8)!
}
func ok(_ text: String)     { print(jsonLine(["status": "ok",          "text": text])) }
func err(_ msg: String)     { print(jsonLine(["status": "error",       "message": msg])) }
func unavail(_ reason: String) { print(jsonLine(["status": "unavailable", "reason": reason])) }

// ── Availability check ────────────────────────────────────────────────────

func checkAvailability() -> String? {
    if #available(macOS 26.0, *) {
        switch SystemLanguageModel.default.availability {
        case .available:
            return nil     // nil = available, no error
        case .unavailable(let reason):
            switch reason {
            case .deviceNotEligible:
                return "deviceNotEligible"
            case .appleIntelligenceNotEnabled:
                return "appleIntelligenceNotEnabled"
            default:
                return "unavailable"
            }
        }
    } else {
        return "requiresMacOS26"
    }
}

// ── Single-turn AI call ───────────────────────────────────────────────────

@available(macOS 26.0, *)
func respond(instructions: String, prompt: String) async -> String {
    do {
        let session  = LanguageModelSession(model: .default, instructions: instructions)
        let response = try await session.respond(to: prompt)   // non-streaming
        return response.content.trimmingCharacters(in: .whitespacesAndNewlines)
    } catch {
        return "Error: \(error.localizedDescription)"
    }
}

// ── Prompts ───────────────────────────────────────────────────────────────

let BASE_INSTRUCTIONS = """
You are the built-in AI assistant for MacCleaner, a Mac storage cleaner.
Be helpful, concise, and reassuring. Users may worry about deleting files.
MacCleaner always moves files to Trash first — nothing is permanently deleted until the user empties Trash.
Keep responses short (1–3 sentences) unless asked for detail.
"""

func promptSummarize(context: String) -> String {
    "Summarize this disk scan result in 2 sentences for a non-technical user. Be specific about the biggest win.\n\nScan result:\n\(context)"
}

func promptExplain(category: String, sizeMB: Double, count: Int) -> String {
    let sizeStr = sizeMB > 1024 ? String(format: "%.1f GB", sizeMB / 1024) : String(format: "%.0f MB", sizeMB)
    return "In one sentence: what is '\(category)' (\(count) files, \(sizeStr)) and is it safe to delete? Start with the category name."
}

func promptAdvise(categories: [String], totalGB: Double) -> String {
    let list = categories.joined(separator: ", ")
    return "The user is about to delete: \(list) (total \(String(format: "%.1f", totalGB)) GB). In 1–2 sentences: confirm it's safe OR warn about anything risky."
}

func promptNotify(totalGB: Double, topCategory: String, topGB: Double) -> String {
    return "Write a friendly macOS notification body (max 15 words) telling the user they can free \(String(format: "%.1f", totalGB)) GB, mentioning \(topCategory) (\(String(format: "%.1f", topGB)) GB) as the biggest item."
}

// ── Main event loop ───────────────────────────────────────────────────────

func run() async {
    while let line = readLine(), !line.isEmpty {
        guard let data = line.data(using: .utf8),
              let req  = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let cmd  = req["cmd"] as? String
        else {
            err("invalid JSON")
            continue
        }

        // Availability is always checked first
        if let reason = checkAvailability() {
            unavail(reason)
            continue
        }

        if #available(macOS 26.0, *) {
            switch cmd {

            case "available":
                ok("Apple Intelligence is available")

            case "summarize":
                guard let ctx = req["context"] as? String else { err("missing context"); continue }
                let text = await respond(instructions: BASE_INSTRUCTIONS, prompt: promptSummarize(context: ctx))
                ok(text)

            case "explain":
                guard let cat   = req["category"]  as? String,
                      let sizeMB = req["size_mb"] as? Double,
                      let count  = req["count"]    as? Int    else { err("missing fields"); continue }
                let text = await respond(instructions: BASE_INSTRUCTIONS, prompt: promptExplain(category: cat, sizeMB: sizeMB, count: count))
                ok(text)

            case "advise":
                guard let cats    = req["categories"] as? [String],
                      let totalGB = req["total_gb"]   as? Double   else { err("missing fields"); continue }
                let text = await respond(instructions: BASE_INSTRUCTIONS, prompt: promptAdvise(categories: cats, totalGB: totalGB))
                ok(text)

            case "notify":
                guard let totalGB = req["total_gb"]    as? Double,
                      let topCat  = req["top_category"] as? String,
                      let topGB   = req["top_gb"]       as? Double  else { err("missing fields"); continue }
                let text = await respond(instructions: BASE_INSTRUCTIONS, prompt: promptNotify(totalGB: totalGB, topCategory: topCat, topGB: topGB))
                ok(text)

            default:
                err("unknown command: \(cmd)")
            }
        }
    }
}

// ── Entry point ───────────────────────────────────────────────────────────

let semaphore = DispatchSemaphore(value: 0)
Task {
    await run()
    semaphore.signal()
}
semaphore.wait()
