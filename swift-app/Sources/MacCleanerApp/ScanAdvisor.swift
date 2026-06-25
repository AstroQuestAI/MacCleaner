import SwiftUI
import FoundationModels

// MARK: - CategoryAdvice

struct CategoryAdvice: Sendable {
    let safety: Safety
    let text: String

    enum Safety: Sendable {
        case safe, review

        var label: String {
            switch self {
            case .safe:   return "Safe to delete"
            case .review: return "Review first"
            }
        }
        var icon: String {
            switch self {
            case .safe:   return "checkmark.circle.fill"
            case .review: return "exclamationmark.triangle.fill"
            }
        }
        var color: Color {
            switch self {
            case .safe:   return .green
            case .review: return .orange
            }
        }
    }
}

// MARK: - Static lookups

enum ScanAdvisor {

    static func safety(for category: String) -> CategoryAdvice.Safety {
        safetyMap[category] ?? .review
    }

    static func fallback(for category: String) -> String {
        fallbackText[category] ?? "Review these files before deleting."
    }

    static func prompt(for cat: ScanCategory) -> String {
        let sizeStr = cat.sizeMB >= 1000
            ? String(format: "%.1f GB", cat.sizeMB / 1000)
            : String(format: "%.0f MB", cat.sizeMB)
        return """
        Category: "\(cat.category)"
        Size: \(sizeStr) in \(cat.count) item\(cat.count == 1 ? "" : "s")

        In 1–2 sentences, explain what these files are and why it's safe (or not) to delete them.
        Mention what regenerates them. No markdown. No bullet points.
        """
    }

    static let instructions = """
    You are MacCleaner's on-device AI advisor. You explain Mac storage categories clearly.
    Key facts: User Caches, Browser Caches, Temp Files, System Logs, Node.js Cache, \
    Python Cache, Homebrew Cache, Build Cache, and Xcode DerivedData are all safe to delete — \
    they are rebuilt automatically. \
    Duplicate Files, Unused node_modules, Mail Downloads, Docker, and Unused Venvs need a quick review first. \
    Keep every response to 1–2 sentences. No markdown. No bullet points.
    """
}

// MARK: - Safety map

private let safetyMap: [String: CategoryAdvice.Safety] = [
    "User Caches":         .safe,
    "Browser Caches":      .safe,
    "System Logs":         .safe,
    "Temp Files":          .safe,
    "Node.js Cache":       .safe,
    "Homebrew Cache":      .safe,
    "Python Cache":        .safe,
    "Build Cache":         .safe,
    "Xcode Artifacts":     .safe,
    "Trash":               .safe,
    "Unused node_modules": .review,
    "Docker":              .review,
    "Mail Downloads":      .review,
    "Duplicate Files":     .review,
    "Unused Venvs":        .review,
]

// MARK: - Fallback advice (shown when Apple Intelligence is unavailable)

private let fallbackText: [String: String] = [
    "User Caches":
        "Per-app caches in ~/Library/Caches. Rebuilt automatically the next time each app runs.",
    "Browser Caches":
        "Safari and Chrome page caches. Rebuilt on the next site visit — bookmarks and passwords are unaffected.",
    "System Logs":
        "Diagnostic logs macOS writes continuously. No user data here; new logs are generated as needed.",
    "Temp Files":
        "System temp files in $TMPDIR and /private/tmp. macOS writes fresh ones as needed.",
    "Node.js Cache":
        "npm, yarn, pnpm download cache in ~/.npm and ~/.cache. Your installed packages in node_modules are untouched.",
    "Homebrew Cache":
        "Old Homebrew package downloads. brew redownloads them on demand if you reinstall a package.",
    "Python Cache":
        "pip, poetry, uv download cache. Your installed packages and virtualenvs are untouched.",
    "Build Cache":
        "Gradle, Maven, Cargo, Go, CocoaPods build output. Source code is untouched — rebuilt on next compile.",
    "Xcode Artifacts":
        "Xcode DerivedData build cache, simulator devices, and archives. DerivedData regenerates on next build.",
    "Trash":
        "Files already in your Trash. This permanently deletes them.",
    "Unused node_modules":
        "node_modules in projects not touched in 30+ days. Restored with `npm install` if you reopen a project.",
    "Docker":
        "Stopped containers, dangling images, and build cache. Verify no containers are actively needed before pruning.",
    "Mail Downloads":
        "Attachments downloaded through Mail. Check if you've already saved what you need.",
    "Duplicate Files":
        "Files with identical content found in multiple locations. One copy is kept — review which location matters.",
    "Unused Venvs":
        "Python virtual environments for projects inactive 60+ days. Recreate with `pip install` if you reopen them.",
]
