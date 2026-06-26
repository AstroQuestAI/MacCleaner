import SwiftUI

struct SplashView: View {
    @State private var visible = false
    @State private var dotPhase = 0
    let onDismiss: () -> Void

    private let version: String = {
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "2.0"
    }()

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(Color(red: 253/255, green: 252/255, blue: 248/255))

            VStack(spacing: 0) {
                Spacer()

                // App icon
                ZStack {
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .fill(Color(red: 15/255, green: 23/255, blue: 42/255))
                        .frame(width: 80, height: 80)
                    Text("🧹")
                        .font(.system(size: 44))
                }
                .padding(.bottom, 22)

                // App name
                Text("MacCleaner")
                    .font(.system(size: 30, weight: .bold, design: .default))
                    .foregroundStyle(Color(red: 15/255, green: 23/255, blue: 42/255))
                    .tracking(-0.5)

                // Tagline
                Text("Your Mac, cleaned.")
                    .font(.system(size: 14, weight: .regular))
                    .foregroundStyle(Color(red: 100/255, green: 116/255, blue: 139/255))
                    .padding(.top, 8)

                Spacer()

                // Animated loading dots
                HStack(spacing: 7) {
                    ForEach(0..<3) { i in
                        Circle()
                            .fill(Color(red: 148/255, green: 163/255, blue: 184/255))
                            .frame(width: 5, height: 5)
                            .opacity(dotPhase == i ? 1 : 0.25)
                            .scaleEffect(dotPhase == i ? 1.4 : 1)
                            .animation(.easeInOut(duration: 0.3), value: dotPhase)
                    }
                }
                .padding(.bottom, 14)

                Text("v\(version)  ·  Free · Secure · Private")
                    .font(.system(size: 10.5))
                    .foregroundStyle(Color(red: 148/255, green: 163/255, blue: 184/255))
                    .padding(.bottom, 22)
            }
        }
        .opacity(visible ? 1 : 0)
        .scaleEffect(visible ? 1 : 0.92)
        .onAppear { startAnimating() }
        .onTapGesture { dismiss() }
    }

    private func startAnimating() {
        withAnimation(.spring(response: 0.4, dampingFraction: 0.75)) {
            visible = true
        }
        animateDots(phase: 0)
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.4) {
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
