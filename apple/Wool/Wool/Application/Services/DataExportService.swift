import Foundation
import SwiftData

@MainActor
enum DataExportService {
    struct AreaDTO: Codable, Equatable {
        var id: UUID
        var name: String
        var notes: String
        var createdAt: Date
    }

    struct ProjectDTO: Codable, Equatable {
        var id: UUID
        var title: String
        var desiredOutcome: String
        var notes: String
        var createdAt: Date
        var updatedAt: Date
        var completedAt: Date?
        var statusRawValue: String
        var isArchived: Bool
        var statusBeforeArchiveRawValue: String?
    }

    struct TaskDTO: Codable, Equatable {
        var id: UUID
        var title: String
        var notes: String
        var createdAt: Date
        var updatedAt: Date
        var dueDate: Date?
        var completedAt: Date?
        var statusRawValue: String
        var contextTags: [String]
        var sortOrder: Double
        var projectId: UUID?
        var areaIds: [UUID]
    }

    struct WeeklyReviewItemDTO: Codable, Equatable {
        var id: UUID
        var title: String
        var instructions: String
        var kindRawValue: String
        var sortOrder: Int
        var isComplete: Bool
        var completedAt: Date?
        var isSkipped: Bool
        var staleDecisionRawValue: String?
        var reviewId: UUID
    }

    struct WeeklyReviewDTO: Codable, Equatable {
        var id: UUID
        var weekStart: Date
        var weekEnd: Date
        var startedAt: Date?
        var completedAt: Date?
        var statusRawValue: String
        var currentStep: Int
        var completedStepCount: Int
        var skippedStepCount: Int
        var isPartial: Bool
        var streakAtCompletion: Int
        var lastSavedAt: Date
        var staleTaskIDs: [String]
        var staleItemsPreparedAt: Date?
    }

    struct Payload: Codable, Equatable {
        var schemaVersion: Int
        var exportedAt: Date
        var areas: [AreaDTO]
        var projects: [ProjectDTO]
        var tasks: [TaskDTO]
        var weeklyReviews: [WeeklyReviewDTO]
        var weeklyReviewItems: [WeeklyReviewItemDTO]
    }

    static let currentSchemaVersion = 1

    static func makePayload(in context: ModelContext) throws -> Payload {
        let areas = try context.fetch(FetchDescriptor<Area>())
        let projects = try context.fetch(FetchDescriptor<Project>())
        let tasks = try context.fetch(FetchDescriptor<TaskItem>())
        let reviews = try context.fetch(FetchDescriptor<WeeklyReview>())
        let items = try context.fetch(FetchDescriptor<WeeklyReviewItem>())

        return Payload(
            schemaVersion: currentSchemaVersion,
            exportedAt: Date(),
            areas: areas.map { AreaDTO(id: $0.id, name: $0.name, notes: $0.notes, createdAt: $0.createdAt) },
            projects: projects.map {
                ProjectDTO(
                    id: $0.id,
                    title: $0.title,
                    desiredOutcome: $0.desiredOutcome,
                    notes: $0.notes,
                    createdAt: $0.createdAt,
                    updatedAt: $0.updatedAt,
                    completedAt: $0.completedAt,
                    statusRawValue: $0.statusRawValue,
                    isArchived: $0.isArchived,
                    statusBeforeArchiveRawValue: $0.statusBeforeArchiveRawValue
                )
            },
            tasks: tasks.map {
                TaskDTO(
                    id: $0.id,
                    title: $0.title,
                    notes: $0.notes,
                    createdAt: $0.createdAt,
                    updatedAt: $0.updatedAt,
                    dueDate: $0.dueDate,
                    completedAt: $0.completedAt,
                    statusRawValue: $0.statusRawValue,
                    contextTags: $0.contextTags,
                    sortOrder: $0.sortOrder,
                    projectId: $0.project?.id,
                    areaIds: ($0.areas ?? []).map(\.id)
                )
            },
            weeklyReviews: reviews.map {
                WeeklyReviewDTO(
                    id: $0.id,
                    weekStart: $0.weekStart,
                    weekEnd: $0.weekEnd,
                    startedAt: $0.startedAt,
                    completedAt: $0.completedAt,
                    statusRawValue: $0.statusRawValue,
                    currentStep: $0.currentStep,
                    completedStepCount: $0.completedStepCount,
                    skippedStepCount: $0.skippedStepCount,
                    isPartial: $0.isPartial,
                    streakAtCompletion: $0.streakAtCompletion,
                    lastSavedAt: $0.lastSavedAt,
                    staleTaskIDs: $0.staleTaskIDs,
                    staleItemsPreparedAt: $0.staleItemsPreparedAt
                )
            },
            weeklyReviewItems: items.map {
                WeeklyReviewItemDTO(
                    id: $0.id,
                    title: $0.title,
                    instructions: $0.instructions,
                    kindRawValue: $0.kindRawValue,
                    sortOrder: $0.sortOrder,
                    isComplete: $0.isComplete,
                    completedAt: $0.completedAt,
                    isSkipped: $0.isSkipped,
                    staleDecisionRawValue: $0.staleDecisionRawValue,
                    reviewId: $0.review?.id ?? UUID()
                )
            }
        )
    }

    static func jsonEncoder() -> JSONEncoder {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        encoder.dateEncodingStrategy = .iso8601
        return encoder
    }

    static func jsonDecoder() -> JSONDecoder {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return decoder
    }

    static func exportJSON(in context: ModelContext) throws -> Data {
        let payload = try makePayload(in: context)
        return try jsonEncoder().encode(payload)
    }

    static func exportCSV(in context: ModelContext) throws -> String {
        let payload = try makePayload(in: context)
        let projectById = Dictionary(uniqueKeysWithValues: payload.projects.map { ($0.id, $0.title) })
        let areaById = Dictionary(uniqueKeysWithValues: payload.areas.map { ($0.id, $0.name) })

        var lines: [String] = []
        let header = ["id", "title", "notes", "status", "createdAt", "updatedAt", "dueDate", "completedAt", "contextTags", "project", "areas"]
        lines.append(header.map(csvEscape).joined(separator: ","))
        for task in payload.tasks {
            let projectTitle = task.projectId.flatMap { projectById[$0] } ?? ""
            let areaNames = task.areaIds.compactMap { areaById[$0] }.joined(separator: ";")
            let row = [
                task.id.uuidString,
                task.title,
                task.notes,
                task.statusRawValue,
                isoString(task.createdAt),
                isoString(task.updatedAt),
                task.dueDate.map(isoString) ?? "",
                task.completedAt.map(isoString) ?? "",
                task.contextTags.joined(separator: ";"),
                projectTitle,
                areaNames
            ]
            lines.append(row.map(csvEscape).joined(separator: ","))
        }
        return lines.joined(separator: "\n") + "\n"
    }

    static func restore(from data: Data, in context: ModelContext) throws {
        let payload = try jsonDecoder().decode(Payload.self, from: data)
        guard payload.schemaVersion == currentSchemaVersion else {
            throw ExportRestoreError.unsupportedSchemaVersion(payload.schemaVersion)
        }

        // Wipe existing data.
        try context.delete(model: WeeklyReviewItem.self)
        try context.delete(model: WeeklyReview.self)
        try context.delete(model: TaskItem.self)
        try context.delete(model: Project.self)
        try context.delete(model: Area.self)

        // Insert areas.
        let areasById: [UUID: Area] = Dictionary(uniqueKeysWithValues: payload.areas.map { dto in
            let area = Area(name: dto.name, notes: dto.notes)
            area.id = dto.id
            // adjust createdAt not in init; set property
            area.createdAt = dto.createdAt
            context.insert(area)
            return (dto.id, area)
        })
        _ = areasById

        let projectsById: [UUID: Project] = Dictionary(uniqueKeysWithValues: payload.projects.map { dto in
            let project = Project(title: dto.title, desiredOutcome: dto.desiredOutcome, notes: dto.notes)
            project.id = dto.id
            project.createdAt = dto.createdAt
            project.updatedAt = dto.updatedAt
            project.completedAt = dto.completedAt
            project.statusRawValue = dto.statusRawValue
            project.isArchived = dto.isArchived
            project.statusBeforeArchiveRawValue = dto.statusBeforeArchiveRawValue
            context.insert(project)
            return (dto.id, project)
        })

        for task in payload.tasks {
            let item = TaskItem(title: task.title, notes: task.notes, status: Status(rawValue: task.statusRawValue) ?? .inbox, dueDate: task.dueDate, contextTags: task.contextTags)
            item.id = task.id
            item.createdAt = task.createdAt
            item.updatedAt = task.updatedAt
            item.completedAt = task.completedAt
            item.statusRawValue = task.statusRawValue
            item.sortOrder = task.sortOrder
            item.project = task.projectId.flatMap { projectsById[$0] }
            item.areas = task.areaIds.compactMap { areasById[$0] }
            context.insert(item)
        }

        let reviewsById: [UUID: WeeklyReview] = [:].merging(payload.weeklyReviews.map { dto in
            let review = WeeklyReview(weekStart: dto.weekStart, weekEnd: dto.weekEnd)
            review.id = dto.id
            review.startedAt = dto.startedAt
            review.completedAt = dto.completedAt
            review.statusRawValue = dto.statusRawValue
            review.currentStep = dto.currentStep
            review.completedStepCount = dto.completedStepCount
            review.skippedStepCount = dto.skippedStepCount
            review.isPartial = dto.isPartial
            review.streakAtCompletion = dto.streakAtCompletion
            review.lastSavedAt = dto.lastSavedAt
            review.staleTaskIDs = dto.staleTaskIDs
            review.staleItemsPreparedAt = dto.staleItemsPreparedAt
            context.insert(review)
            return (dto.id, review)
        }, uniquingKeysWith: { a, _ in a })

        for itemDto in payload.weeklyReviewItems {
            let item = WeeklyReviewItem(title: itemDto.title, instructions: itemDto.instructions, kind: WeeklyReviewStepKind(rawValue: itemDto.kindRawValue) ?? .collect, sortOrder: itemDto.sortOrder)
            item.id = itemDto.id
            item.isComplete = itemDto.isComplete
            item.completedAt = itemDto.completedAt
            item.isSkipped = itemDto.isSkipped
            item.staleDecisionRawValue = itemDto.staleDecisionRawValue
            item.review = reviewsById[itemDto.reviewId]
            context.insert(item)
        }

        try context.save()
    }

    private static func isoString(_ date: Date) -> String {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        return formatter.string(from: date)
    }

    private static func csvEscape(_ value: String) -> String {
        if value.contains(",") || value.contains("\"") || value.contains("\n") {
            return "\"" + value.replacingOccurrences(of: "\"", with: "\"\"") + "\""
        }
        return value
    }
}

enum ExportRestoreError: LocalizedError {
    case unsupportedSchemaVersion(Int)
    var errorDescription: String? {
        switch self { case .unsupportedSchemaVersion(let v): return "Unsupported export schema version: \(v)." }
    }
}
