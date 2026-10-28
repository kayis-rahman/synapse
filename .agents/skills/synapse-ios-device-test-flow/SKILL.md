---
name: synapse-ios-device-test-flow
description: >
  Load immediately before any iOS build, install, launch, simulator/device
  decision, or physical-device UI test run.
user-invocable: true
---

# synapse-ios-device-test-flow

Trigger: load immediately before any iOS build, install, launch,
simulator/device decision, or physical-device UI test run.

In scope: device discovery, lock-state, destination checks, xcodebuild flags,
derived-data paths, `-focus-test-reset`, store env vars, and `--test-each`.

Out of scope: source changes, model/schema conventions, and deployment
decisions.

## Core rules

1. Never use simulator destinations for Synapse iOS app validation.
2. Verify `xcrun devicectl list devices` reports the paired iPhone 15 Pro.
3. Use `scripts/run-on-iphone15pro.sh` for standard build/install/launch.
4. Keep physical-device UI test commands from
   `docs/ios-ui-tests-on-iphone-15-pro.md`.
