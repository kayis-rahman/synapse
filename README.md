# Synapse

Synapse is a privacy-first task and focus manager for iOS, macOS, and watchOS.
Everyday task data stays on the user's Apple devices and syncs through the
private CloudKit database when available.

## Release status

- App version: `1.0.0`
- Build: `1`
- CloudKit container: `iCloud.com.sparkage.synapse`
- SwiftData schema: `1` (`SynapseSchemaV1`)
- Feature flags default to disabled: Malayalam voice, Gmail integration, GitHub
  Projects integration

## Build and test

Open `apple/Synapse/Synapse.xcodeproj` in Xcode. The shared schemes are:

- `Synapse iOS` - iOS app
- `Synapse iOS Unit Tests` - unit/service/SwiftData tests
- `Synapse macOS` - macOS app
- `SynapseWatch Watch App` - watchOS app

Run iOS unit tests from the command line:

```sh
cd apple/Synapse
xcodebuild -scheme "Synapse iOS Unit Tests" \
  -destination "platform=iOS Simulator,name=iPhone 18 Pro" test
```

## Continuous integration

Xcode Cloud runs the `Synapse iOS Unit Tests` suite on every push and archives
`Synapse iOS` for TestFlight when a `v*.*.*` tag is pushed. Physical-device UI
tests remain a manual pre-release gate; see `docs/xcode-cloud-setup.md` and
`docs/ios-ui-tests-on-iphone-15-pro.md`.

## Documentation

- `docs/RELEASING.md` - versioning, schema, CloudKit, and rollout process
- `docs/pre-release-checklist.md` - pre-release gate checklist
- `docs/app-feature.md` - feature inventory
- `docs/feature-flags-cloudkit.md` - feature flag setup
- `CHANGELOG.md` - release history and schema state

## Contributing

Follow `AGENTS.md` and the installed `write-swift` skill for Swift changes. Run
the iOS unit tests and keep changes inside the repository worktree.
