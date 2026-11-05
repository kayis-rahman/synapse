# Xcode Cloud Setup

Xcode Cloud workflows are configured in Xcode/App Store Connect, not as a
YAML file in the repo. This doc records the one-time setup and what's
already committed to support it.

## What's in the repo

`apple/Wool/ci_scripts/ci_post_clone.sh` — runs after Xcode Cloud clones
the repo, before build. Currently runs `swiftlint --strict`. Add
`ci_pre_xcodebuild.sh` / `ci_post_xcodebuild.sh` in the same directory if you
need steps before/after the build (e.g. notarization, notifications).

## One-time setup (do this in Xcode)

1. Open `apple/Wool/Wool.xcodeproj` in Xcode.
2. Product → Xcode Cloud → Create Workflow. Sign in with the Apple ID that
   has App Store Connect access, select the team, and let Xcode create the
   `WOOL_...` Xcode Cloud App Store Connect API integration.
3. Create these workflows:

   **"iOS Unit Tests"**
   - Scheme: `Wool iOS Unit Tests`
   - Start condition: branch changes on `develop`
   - Action: Test (iOS Simulator only — UI tests run locally on a
     simulator, see note below)
   - Post-action: none required; Xcode Cloud reports pass/fail on the PR
     automatically if you enable "Xcode Cloud" as a required check in
     GitHub branch protection.

   **"TestFlight Release"**
   - Scheme: `Wool iOS`
   - Start condition: new tag matching `v*.*.*`
   - Action: Archive → Release (TestFlight, internal testers)
   - Post-action: TestFlight external testing group, if/when you want
     phased external rollout per `docs/RELEASING.md`.

   Optionally add a **"macOS Build"** workflow (scheme `Wool macOS`,
   Archive action) if you want Xcode Cloud to sanity-build macOS too — it
   won't upload anywhere unless you configure a Mac distribution method.

4. Confirm signing: Xcode Cloud manages certificates/profiles automatically
   once you grant it access in the Certificates, Identifiers & Profiles
   section during workflow creation. No manual `.p12`/profile management
   needed.

## Why the physical-device workflow is NOT in Xcode Cloud

Per `CLAUDE.md`, iOS builds, unit tests, and UI tests run on an iOS Simulator,
so the CI picture is simple:

- Xcode Cloud runs `Wool iOS Unit Tests` (unit/service/SwiftData tests)
  on every push.
- Run the `WoolUITests` suite locally on a simulator with
  `scripts/run-on-simulator.sh` before tagging a release.
- Xcode Cloud only provisions simulators/cloud Macs, it cannot attach to a
  specific paired physical device, so the optional device-specific workflow in
  `docs/ios-ui-tests-on-iphone-15-pro.md` would need a self-hosted Mac runner
  permanently tethered to that phone to be automated.

## Triggering a release

1. Run the UI test suite locally on an iOS Simulator, confirm green.
2. Bump marketing version / build number, update `CHANGELOG.md` per
   `docs/RELEASING.md`.
3. Tag: `git tag vX.Y.Z && git push origin vX.Y.Z`.
4. Xcode Cloud's "TestFlight Release" workflow picks up the tag, archives,
   and uploads to TestFlight automatically. Check progress in the Xcode
   Cloud report tab in Xcode, or App Store Connect.
