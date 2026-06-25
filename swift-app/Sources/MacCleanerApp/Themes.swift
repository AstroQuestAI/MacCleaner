import SwiftUI

// MARK: - Theme model

struct AppTheme: Identifiable {
    let key:    String
    let name:   String
    let accent: Color

    var id: String { key }
}

// MARK: - Catalogue (matches website data/themes.ts)

let appThemes: [AppTheme] = [
    AppTheme(key: "glass",     name: "Midnight Indigo", accent: Color(hex: "5E5CE6")),
    AppTheme(key: "rose",      name: "Infrared",        accent: Color(hex: "FF375F")),
    AppTheme(key: "sky",       name: "Pacific Blue",    accent: Color(hex: "0A84FF")),
    AppTheme(key: "mint",      name: "Midnight Green",  accent: Color(hex: "30D158")),
    AppTheme(key: "peach",     name: "Desert Sunset",   accent: Color(hex: "FF9F0A")),
    AppTheme(key: "lavender",  name: "Deep Purple",     accent: Color(hex: "BF5AF2")),
    AppTheme(key: "sage",      name: "Olive Night",     accent: Color(hex: "FFD60A")),
    AppTheme(key: "arctic",    name: "Titanium",        accent: Color(hex: "98989D")),
    AppTheme(key: "champagne", name: "Rose Gold",       accent: Color(hex: "FFBC3C")),
    AppTheme(key: "neon",      name: "Eclipse",         accent: Color(hex: "30D0E0")),
]

func theme(for key: String) -> AppTheme {
    appThemes.first { $0.key == key } ?? appThemes[0]
}

// MARK: - Hex colour init

extension Color {
    init(hex: String) {
        let h = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: h).scanHexInt64(&int)
        let r = Double((int >> 16) & 0xFF) / 255
        let g = Double((int >> 8)  & 0xFF) / 255
        let b = Double(int         & 0xFF) / 255
        self.init(red: r, green: g, blue: b)
    }
}
