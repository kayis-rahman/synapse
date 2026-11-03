import os

enum LoggerStore {
    static let timer = Logger(subsystem: "com.wool", category: "Timer")
    static let session = Logger(subsystem: "com.wool", category: "SessionAPI")
    static let auth = Logger(subsystem: "com.wool", category: "Auth")
    static let general = Logger(subsystem: "com.wool", category: "General")
}
