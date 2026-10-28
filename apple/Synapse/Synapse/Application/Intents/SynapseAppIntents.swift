#if canImport(AppIntents)
import AppIntents
import SwiftData
import CloudKit

enum SynapseIntentError: LocalizedError {
    case appNeedsSetup
    case cloudKitUnavailable
    case emptyCapture
    case taskNotFound(String)

    var errorDescription: String? {
        switch self {
        case .appNeedsSetup: "Open Synapse first to set up Siri capture."
        case .cloudKitUnavailable: "Synapse needs iCloud to finish setting up. Open Synapse and complete setup, then try again."
        case .emptyCapture: "I didn't hear what to capture. Tell me what you'd like to add to Synapse."
        case .taskNotFound(let title): "I couldn't find an open task matching \"\(title)\"."
        }
    }
}

enum SynapseIntentSupport {
    static func setupError(appSetupCompleted: Bool, accountStatus: CKAccountStatus?) -> SynapseIntentError? {
        guard appSetupCompleted else { return .appNeedsSetup }
        guard accountStatus != .noAccount else { return .cloudKitUnavailable }
        return nil
    }

    static func context() async throws -> ModelContext {
        let accountStatus = !SynapseModelContainer.isTestingProcess
            ? try? await CKContainer(identifier: SynapseModelContainer.cloudKitContainerIdentifier).accountStatus()
            : nil
        if let error = setupError(
            appSetupCompleted: SynapseModelContainer.appSetupCompleted,
            accountStatus: accountStatus
        ) {
            throw error
        }
        do { return ModelContext(try SynapseModelContainer.makeIntentContainer()) }
        catch { throw SynapseIntentError.cloudKitUnavailable }
    }

    static func save(_ context: ModelContext) throws {
        do { try context.save() } catch { throw SynapseIntentError.cloudKitUnavailable }
    }

    static func save(_ item: TaskItem, in context: ModelContext) throws {
        context.insert(item)
        try save(context)
    }

    static func normalized(_ value: String) -> String {
        value.lowercased().folding(options: [.diacriticInsensitive, .caseInsensitive], locale: .current)
            .components(separatedBy: CharacterSet.alphanumerics.inverted).filter { !$0.isEmpty }.joined(separator: " ")
    }

    private static func tokenDistance(_ lhs: String, _ rhs: String) -> Int {
        if lhs == rhs { return 0 }
        let lhsCount = lhs.count, rhsCount = rhs.count
        if abs(lhsCount - rhsCount) > 2 { return Int.max }
        var previous = Array(0...rhsCount)
        var current = Array(repeating: 0, count: rhsCount + 1)
        for (i, l) in lhs.enumerated() {
            current[0] = i + 1
            for (j, r) in rhs.enumerated() {
                let substitutionCost = l == r ? 0 : 1
                current[j + 1] = min(previous[j + 1] + 1, current[j] + 1, previous[j] + substitutionCost)
            }
            swap(&previous, &current)
        }
        return previous[rhsCount]
    }

    private static func isHexToken(_ value: String) -> Bool {
        guard value.count >= 4 else { return false }
        return value.allSatisfy { "0123456789abcdef".contains($0) }
    }

    private static func tokensAreClose(_ lhs: String, _ rhs: String) -> Bool {
        if lhs == rhs { return true }
        guard lhs.count >= 4 && rhs.count >= 4 else { return false }
        return tokenDistance(lhs, rhs) <= 1
    }

    /// Number of query tokens that have a close (exact or single-edit) match in
    /// the task title. Close token matches let a misheard word such as "silk"
    /// still count as overlap against "milk".
    private static func meaningfulTokenOverlap(queryWords: Set<String>, titleWords: Set<String>) -> Int {
        let queries = Array(queryWords)
        let titles = Array(titleWords)
        var matchForTitle = Array(repeating: -1, count: titles.count)

        func tryMatch(_ queryIndex: Int, visited: inout [Bool]) -> Bool {
            for (titleIndex, titleWord) in titles.enumerated() {
                guard !visited[titleIndex], tokensAreClose(queries[queryIndex], titleWord) else { continue }
                visited[titleIndex] = true
                if matchForTitle[titleIndex] == -1 || tryMatch(matchForTitle[titleIndex], visited: &visited) {
                    matchForTitle[titleIndex] = queryIndex
                    return true
                }
            }
            return false
        }

        var total = 0
        for queryIndex in queries.indices {
            var visited = Array(repeating: false, count: titles.count)
            if tryMatch(queryIndex, visited: &visited) { total += 1 }
        }
        return total
    }

    static func bestTaskMatch(for query: String, in tasks: [TaskItem]) -> TaskItem? {
        let normalizedQuery = normalized(query)
        guard !normalizedQuery.isEmpty else { return nil }
        let queryWords = Set(normalizedQuery.split(separator: " ").map(String.init).filter { !isHexToken($0) })
        guard !queryWords.isEmpty else { return nil }
        return tasks.filter { $0.status != .completed && $0.status != .cancelled }.compactMap { task -> (TaskItem, Int)? in
            let title = normalized(task.title)
            let titleWords = Set(title.split(separator: " ").map(String.init).filter { !isHexToken($0) })
            guard !titleWords.isEmpty else { return nil }
            let overlap = queryWords.intersection(titleWords).count
            let contains = title.contains(normalizedQuery) || normalizedQuery.contains(title)
            let fuzzyOverlap = meaningfulTokenOverlap(queryWords: queryWords, titleWords: titleWords)
            // Refuse matches that rest on a single shared word (or a substring
            // occurrence) without enough token-level alignment to be meaningful.
            let requiredOverlap = queryWords.count <= 1 ? 1 : max(2, queryWords.count / 2 + 1)
            guard fuzzyOverlap >= requiredOverlap else { return nil }
            return (task, (contains ? 100 : 0) + max(overlap, fuzzyOverlap) * 10 - abs(titleWords.count - queryWords.count))
        }.sorted { $0.1 > $1.1 }.first?.0
    }
}

struct AddCaptureIntent: AppIntent {
    static var title: LocalizedStringResource { "Capture an item" }
    static var description = IntentDescription("Save a thought to the Synapse Inbox.")
    static var openAppWhenRun: Bool { false }

    @Parameter(title: "Capture")
    var title: String

    func perform() async throws -> some IntentResult {
        guard !title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { throw SynapseIntentError.emptyCapture }
        let context = try await SynapseIntentSupport.context()
        let item = await CaptureService.shared.processInboxCapture(text: title)
        try SynapseIntentSupport.save(item, in: context)
        return .result()
    }

    static var parameterSummary: some ParameterSummary {
        Summary("Capture \(\.$title)")
    }
}

struct AddNextActionIntent: AppIntent {
    static var title: LocalizedStringResource { "Add a next action" }
    static var description = IntentDescription("Add an actionable task directly to Next Actions.")
    static var openAppWhenRun: Bool { false }

    @Parameter(title: "Action")
    var title: String

    func perform() async throws -> some IntentResult {
        guard !title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { throw SynapseIntentError.emptyCapture }
        let context = try await SynapseIntentSupport.context()
        let item = await CaptureService.shared.processCapture(text: title)
        item.status = .nextAction
        try SynapseIntentSupport.save(item, in: context)
        TaskDueNotificationService.shared.sync(task: item)
        return .result()
    }

    static var parameterSummary: some ParameterSummary {
        Summary("Add next action \(\.$title)")
    }
}

struct StartWeeklyReviewIntent: AppIntent {
    static var title: LocalizedStringResource { "Start weekly review" }
    static var description = IntentDescription("Start a structured Synapse weekly review.")
    static var openAppWhenRun: Bool { true }

    func perform() async throws -> some IntentResult {
        let context = try await SynapseIntentSupport.context()
        let reviews = try context.fetch(FetchDescriptor<WeeklyReview>())
        let service = await WeeklyReviewService.shared
        if await service.resumeReview(from: reviews) == nil,
           await service.review(forWeekContaining: .now, from: reviews) == nil {
            context.insert(await service.makeWeeklyReview())
            try SynapseIntentSupport.save(context)
        }
        UserDefaults.standard.set("weekly-review", forKey: SynapseModelContainer.pendingDestinationKey)
        return .result()
    }
}

struct StartFocusIntent: AppIntent {
    static var title: LocalizedStringResource { "Start focus" }
    static var description = IntentDescription("Open Synapse Focus and start a work session.")
    static var openAppWhenRun: Bool { true }

    func perform() async throws -> some IntentResult {
        guard SynapseModelContainer.appSetupCompleted else { throw SynapseIntentError.appNeedsSetup }
        UserDefaults.standard.set("focus", forKey: SynapseModelContainer.pendingDestinationKey)
        UserDefaults.standard.set(true, forKey: "synapse.pendingStartFocus")
        return .result()
    }
}

struct DailyBriefingIntent: AppIntent {
    static var title: LocalizedStringResource { "What's my Synapse briefing?" }
    static var description = IntentDescription("Read today's focus, overdue work, and Waiting For follow-ups.")
    static var openAppWhenRun: Bool { false }

    func perform() async throws -> some IntentResult {
        let context = try await SynapseIntentSupport.context()
        let tasks = try context.fetch(FetchDescriptor<TaskItem>())
        let result = await DailyBriefingService.shared.makeBriefing(
            tasks: tasks,
            isFirstRun: tasks.isEmpty && !UserDefaults.standard.bool(forKey: "synapse.hasGeneratedBriefing")
        )
        return .result(dialog: IntentDialog(stringLiteral: result.narrative ?? result.plainText))
    }
}

struct CompleteTaskIntent: AppIntent {
    static var title: LocalizedStringResource { "Complete a task" }
    static var description = IntentDescription("Mark an existing Synapse task as complete.")
    static var openAppWhenRun: Bool { false }

    @Parameter(title: "Task") var title: String

    func perform() async throws -> some IntentResult {
        let context = try await SynapseIntentSupport.context()
        let tasks = try context.fetch(FetchDescriptor<TaskItem>())
        guard let task = SynapseIntentSupport.bestTaskMatch(for: title, in: tasks) else {
            throw SynapseIntentError.taskNotFound(title)
        }
        task.status = .completed
        try SynapseIntentSupport.save(context)
        TaskDueNotificationService.shared.sync(task: task)
        return .result(dialog: IntentDialog(stringLiteral: "Marked \(task.title) complete."))
    }

    static var parameterSummary: some ParameterSummary { Summary("Complete \(\.$title)") }
}

struct ShowNextActionsIntent: AppIntent {
    static var title: LocalizedStringResource { "Show next actions" }
    static var description = IntentDescription("Read today's open Next Actions from Synapse.")
    static var openAppWhenRun: Bool { false }

    func perform() async throws -> some IntentResult {
        let context = try await SynapseIntentSupport.context()
        let tasks = try context.fetch(FetchDescriptor<TaskItem>())
        let actions = tasks.filter { $0.status == .nextAction && ($0.dueDate == nil || Calendar.current.isDateInToday($0.dueDate!)) }
            .sorted { $0.createdAt < $1.createdAt }
        let message = actions.isEmpty ? "You have no open Next Actions for today." : "Today's Next Actions: " + actions.map(\.title).joined(separator: ", ")
        return .result(dialog: IntentDialog(stringLiteral: message))
    }
}

struct SynapseShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(intent: AddCaptureIntent(), phrases: ["Capture an item in \(.applicationName)"], shortTitle: "Capture item", systemImageName: "tray.and.arrow.down")
        AppShortcut(intent: AddNextActionIntent(), phrases: ["Add a next action in \(.applicationName)"], shortTitle: "Add next action", systemImageName: "checkmark.circle")
        AppShortcut(intent: StartWeeklyReviewIntent(), phrases: ["Start my weekly review in \(.applicationName)"], shortTitle: "Start review", systemImageName: "arrow.triangle.2.circlepath")
        AppShortcut(intent: StartFocusIntent(), phrases: ["Start focus in \(.applicationName)"], shortTitle: "Start focus", systemImageName: "timer")
        AppShortcut(intent: CompleteTaskIntent(), phrases: ["Mark a task complete in \(.applicationName)"], shortTitle: "Complete task", systemImageName: "checkmark.circle")
        AppShortcut(intent: ShowNextActionsIntent(), phrases: ["What's next in \(.applicationName)", "Show my next actions in \(.applicationName)"], shortTitle: "Next actions", systemImageName: "list.bullet")
        AppShortcut(intent: DailyBriefingIntent(), phrases: ["What's my briefing in \(.applicationName)", "Give me my daily briefing in \(.applicationName)"], shortTitle: "Daily briefing", systemImageName: "sparkles")
    }
}
#endif
