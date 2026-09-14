# Run Synapse UI Tests on an iOS Simulator

Use the simulator runner for fast UI-test iteration. It boots the configured
iPhone 17 Pro simulator, builds the UI-test bundle once, and then reuses that
build for each requested test identifier.

From the repository root:

```sh
./scripts/run-on-simulator.sh
```

Run selected tests without rebuilding between them:

```sh
./scripts/run-on-simulator.sh \
  SynapseUITests/iOSSettingsUITests/testNotificationsSettingsShowsMasterAndWeeklyReviewToggles \
  SynapseUITests/iOSSettingsUITests/testDisablingNotificationsDisablesWeeklyReviewToggle
```

Use the physical-device workflow for signing, CloudKit, Siri/Shortcuts,
notification delivery, and final release confidence.
