import XCTest
@testable import Synapse

final class TaskAPIIntegrationTests: XCTestCase {
    func testUserTaskRoundTripsItsIdentityAndStatus() throws {
        let taskID = UUID()
        let userID = UUID()
        let task = UserTask(
            id: taskID,
            userId: userID,
            title: "Integration fixture",
            status: .inProgress
        )

        let data = try JSONEncoder().encode(task)
        let decoded = try JSONDecoder().decode(UserTask.self, from: data)

        XCTAssertEqual(decoded.id, taskID)
        XCTAssertEqual(decoded.userId, userID)
        XCTAssertEqual(decoded.status, .inProgress)
        XCTAssertTrue(decoded.isActive)
    }
}
