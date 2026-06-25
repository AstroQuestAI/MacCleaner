import SwiftUI
import FoundationModels

// MARK: - AI Assistant (Apple Intelligence · on-device · private)
// Uses FoundationModels.framework — available macOS 26+ with Apple Intelligence enabled.

struct AIAssistantView: View {
    @State private var messages: [ChatMessage] = [
        ChatMessage(role: .assistant, text:
            "Hi! I'm your on-device AI assistant. Ask me anything about your Mac's storage — " +
            "\"What's safe to delete?\", \"Why is Xcode using 18 GB?\", \"How do I free space fast?\"")
    ]
    @State private var input      = ""
    @State private var isThinking = false

    // Persistent session retains conversation context
    @State private var session: LanguageModelSession? = nil

    var body: some View {
        VStack(spacing: 0) {
            header
            Divider()
            messageList
            Divider()
            inputBar
        }
    }

    // MARK: Header

    private var header: some View {
        HStack(spacing: 10) {
            Image(systemName: "sparkles")
                .foregroundStyle(
                    LinearGradient(colors: [.purple, .pink], startPoint: .top, endPoint: .bottom)
                )
                .font(.title3)
            VStack(alignment: .leading, spacing: 1) {
                Text("Ask AI").font(.headline)
                Text("On-device · Private · No internet")
                    .font(.caption2).foregroundStyle(.secondary)
            }
            Spacer()
            availabilityBadge
        }
        .padding()
    }

    @ViewBuilder
    private var availabilityBadge: some View {
        let model = SystemLanguageModel.default
        if case .available = model.availability {
            Label("Apple Intelligence", systemImage: "brain.filled.head.profile")
                .font(.caption).foregroundStyle(.purple)
        } else {
            Label("Enable Apple Intelligence", systemImage: "exclamationmark.circle")
                .font(.caption).foregroundStyle(.orange)
        }
    }

    // MARK: Messages

    private var messageList: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 12) {
                    ForEach(messages) { msg in
                        MessageBubble(message: msg).id(msg.id)
                    }
                    if isThinking {
                        ThinkingIndicator()
                    }
                }
                .padding()
            }
            .onChange(of: messages.count) { _, _ in
                if let last = messages.last {
                    withAnimation { proxy.scrollTo(last.id, anchor: .bottom) }
                }
            }
        }
    }

    // MARK: Input bar

    private var inputBar: some View {
        HStack(spacing: 10) {
            TextField("Ask about your storage…", text: $input, axis: .vertical)
                .textFieldStyle(.roundedBorder)
                .lineLimit(1...4)
                .onSubmit { send() }

            Button { send() } label: {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.title2)
                    .foregroundStyle(input.isEmpty ? Color.secondary : Color.purple)
            }
            .buttonStyle(.plain)
            .disabled(input.isEmpty || isThinking)
        }
        .padding()
    }

    // MARK: Send

    private func send() {
        let text = input.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty else { return }
        input = ""
        messages.append(ChatMessage(role: .user, text: text))
        isThinking = true

        Task {
            await generate(prompt: text)
            isThinking = false
        }
    }

    // MARK: Foundation Models — Apple Intelligence on-device

    private func generate(prompt: String) async {
        let model = SystemLanguageModel.default
        guard case .available = model.availability else {
            messages.append(ChatMessage(role: .assistant, text:
                "Apple Intelligence isn't available on this device. " +
                "Enable it in System Settings → Apple Intelligence & Siri."))
            return
        }

        if session == nil {
            session = LanguageModelSession(model: .default, instructions: macCleanerInstructions)
        }
        guard let session else { return }

        do {
            let response = try await session.respond(to: prompt)
            messages.append(ChatMessage(role: .assistant,
                text: response.content.trimmingCharacters(in: .whitespacesAndNewlines)))
        } catch {
            messages.append(ChatMessage(role: .assistant,
                text: "Sorry, something went wrong: \(error.localizedDescription)"))
        }
    }

}

// MARK: - System instructions

private let macCleanerInstructions = """
You are MacCleaner's built-in AI assistant. You help users understand and safely manage their Mac's disk storage.

Key facts you know:
- User Caches (~/Library/Caches): always safe to delete; apps rebuild them automatically
- System Logs (/var/log, ~/Library/Logs): safe to delete
- Xcode DerivedData (~/Library/Developer/Xcode/DerivedData): very safe, often huge (10–30 GB), Xcode rebuilds on next open
- Docker (~/Library/Containers/com.docker): safe if not actively using Docker
- Node.js Cache (~/.npm, ~/.yarn/cache): safe; packages re-download when needed
- Browser Caches: safe to delete
- Python Cache (.pyc, __pycache__): safe to delete
- MacCleaner always moves to Trash first — nothing is permanently deleted until Trash is emptied

Be helpful, reassuring, and concise. Users may be nervous about deleting files. Keep responses under 3 sentences unless more detail is needed.
"""

// MARK: - Chat models

struct ChatMessage: Identifiable {
    enum Role { case user, assistant }
    let id   = UUID()
    let role: Role
    let text: String
}

// MARK: - Sub-views

private struct MessageBubble: View {
    let message: ChatMessage
    var isUser: Bool { message.role == .user }

    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            if isUser { Spacer(minLength: 60) }
            if !isUser {
                Image(systemName: "sparkles").foregroundStyle(.purple).padding(.top, 2)
            }
            Text(message.text)
                .textSelection(.enabled)
                .padding(.horizontal, 14).padding(.vertical, 10)
                .background(isUser ? Color.purple.opacity(0.15) : Color(nsColor: .controlBackgroundColor))
                .clipShape(RoundedRectangle(cornerRadius: 14))
                .font(.system(size: 13))
            if !isUser { Spacer(minLength: 60) }
        }
    }
}

private struct ThinkingIndicator: View {
    @State private var count = 1
    let timer = Timer.publish(every: 0.4, on: .main, in: .common).autoconnect()

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "sparkles").foregroundStyle(.purple)
            Text(String(repeating: "●", count: count))
                .foregroundStyle(.secondary).font(.caption)
                .onReceive(timer) { _ in count = count % 3 + 1 }
        }
        .padding(.horizontal, 14).padding(.vertical, 10)
        .background(Color(nsColor: .controlBackgroundColor))
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }
}
