// swift-tools-version: 5.10
import PackageDescription

let package = Package(
    name: "MacCleanerApp",
    platforms: [.macOS(.v14)],
    targets: [
        .executableTarget(
            name: "MacCleanerApp",
            path: "Sources/MacCleanerApp",
            swiftSettings: [
                .enableExperimentalFeature("StrictConcurrency"),
            ]
        ),
    ]
)
