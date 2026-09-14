import XCTest
@testable import Synapse

final class TaskServiceUnitTests: XCTestCase {
    func testTaskValidationRejectsWhitespaceOnlyTitle() {
        let task = UserTask(userId: UUID(), title: "   ")
        XCTAssertThrowsError(try task.validate()) { error in
            XCTAssertEqual(error as? TaskValidationError, .emptyTitle)
        }
    }

    func testTaskStatusHelpersDistinguishActiveAndCompleted() {
        let active = UserTask(userId: UUID(), title: "Active", status: .inProgress)
        let completed = active.withStatus(.completed)

        XCTAssertTrue(active.isActive)
        XCTAssertFalse(active.isCompleted)
        XCTAssertFalse(completed.isActive)
        XCTAssertTrue(completed.isCompleted)
    }
}
