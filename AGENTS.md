# Synapse Development Instructions

## iOS validation

Use an iOS Simulator for fast build and UI-test iteration when practical.
Use the configured physical iPhone 15 Pro for device-specific validation,
signing checks, CloudKit, Siri/Shortcuts, notification delivery, and final
release confidence. The physical-device workflow remains available through
`scripts/run-on-iphone15pro.sh` and the commands documented in
`docs/ios-ui-tests-on-iphone-15-pro.md`.

## UI changes

For every user-interface change—including SwiftUI layout, styling, interaction,
motion, navigation, accessibility, and UI tests—use the `emilkowalski/skills`
guidance before implementation. In this workspace, the installed Emil
Kowalski skill is `emil-design-eng` at:

`/Users/kayisrahman/.agents/skills/anthropic-skills/skills/emil-design-eng/SKILL.md`

Read the skill instructions before making the UI change, apply its principles
to the implementation, and mention any material design decisions in the final
handoff. This requirement applies to iOS, macOS, watchOS, and shared UI code.

Continue to use the Swift-specific `write-swift` skill for Swift implementation
and concurrency work when the task involves Swift code.

## Capture test requirements

Changes to Quick Capture, Inbox persistence, triage, or capture intents must
include all three test layers:

1. Unit/service tests for classification, validation, normalization, and edge
   cases.
2. SwiftData/integration tests for local persistence, duplicates, offline
   behavior, and CloudKit synchronization where applicable.
3. UI tests for the user-visible capture flow on a representative iOS
   destination. Use the physical iPhone 15 Pro when validating device-specific
   behavior or release readiness.

Use deterministic fixtures and unique UUID markers for persisted test data.
Keep manual-only conditions such as low storage and account sign-out explicitly
documented rather than making nondeterministic tests.
