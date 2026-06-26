import SwiftUI

struct SplashView: View {
    @State private var visible = true
    @State private var dotPhase = 0
    let onDismiss: () -> Void

    private let version: String = {
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "2.0"
    }()

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .fill(Color(red: 253/255, green: 252/255, blue: 248/255))

            VStack(spacing: 0) {
                Spacer()

                // App icon
                ZStack {
                    RoundedRectangle(cornerRadius: 28, style: .continuous)
                        .fill(Color(red: 15/255, green: 23/255, blue: 42/255))
                        .frame(width: 110, height: 110)
                    Text("🧹")
                        .font(.system(size: 60))
                }
                .padding(.bottom, 28)

                // App name
                Text("MacCleaner")
                    .font(.system(size: 40, weight: .bold, design: .default))
                    .foregroundStyle(Color(red: 15/255, green: 23/255, blue: 42/255))
                    .tracking(-1)

                // Tagline
                Text("Your Mac, cleaned.")
                    .font(.system(size: 17, weight: .regular))
                    .foregroundStyle(Color(red: 100/255, green: 116/255, blue: 139/255))
                    .padding(.top, 10)

                Spacer()

                // Animated loading dots
                HStack(spacing: 9) {
                    ForEach(0..<3) { i in
                        Circle()
                            .fill(Color(red: 148/255, green: 163/255, blue: 184/255))
                            .frame(width: 7, height: 7)
                            .opacity(dotPhase == i ? 1 : 0.25)
                            .scaleEffect(dotPhase == i ? 1.4 : 1)
                            .animation(.easeInOut(duration: 0.3), value: dotPhase)
                    }
                }
                .padding(.bottom, 16)

                Text("v\(version)  ·  Free · Secure · Private")
                    .font(.system(size: 12))
                    .foregroundStyle(Color(red: 148/255, green: 163/255, blue: 184/255))
                    .padding(.bottom, 28)
            }
        }
        .frame(width: 520, height: 400)
        .opacity(visible ? 1 : 0)
        .scaleEffect(visible ? 1 : 0.94)
        .onAppear { startAnimating() }
        .onTapGesture { dismiss() }
    }

    private func startAnimating() {
        animateDots(phase: 0)
        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
            dismiss()
        }
    }

    private func animateDots(phase: Int) {
        dotPhase = phase
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.45) {
            guard visible else { return }
            animateDots(phase: (phase + 1) % 3)
        }
    }

    private func dismiss() {
        guard visible else { return }
        withAnimation(.easeIn(duration: 0.3)) {
            visible = false
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.35) {
            onDismiss()
        }
    }
}
