# Changelog

All notable Synapse releases are recorded here. Each entry identifies the
CloudKit/SwiftData schema state required by that app version.

## [Unreleased]

- Release preparation for Synapse 1.0: aligned version/build metadata, cleaned
  stale coverage references, and documented the pre-release checklist.
- iOS unit test baseline: 196 tests passed, 7 skipped, 0 failures.
- Schema state: `1` (baseline versioned schema).

## [1.0.0] - 2026-08-30

- Initial Synapse release candidate.
- App build: `1`.
- CloudKit container: `iCloud.com.sparkage.synapse`.
- SwiftData schema: `1` (`SynapseSchemaV1`).
- Malayalam voice, Gmail, and GitHub Projects flags default to disabled.
- Compatibility target: fresh install and upgrade from the pre-versioned
  baseline store.
