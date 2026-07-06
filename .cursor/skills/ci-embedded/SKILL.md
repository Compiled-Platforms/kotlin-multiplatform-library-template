---
name: ci-embedded
description: CI for embedded and IoT systems — firmware builds, multi-target firmware, ESP-IDF CI, embedded C++ CI, cross-toolchain management, hardware simulation, emulator testing, flash size validation, memory usage validation, and OTA package generation. Use when setting up or improving CI for embedded/IoT projects.
---

# CI Embedded / IoT

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Principles

- Embedded CI is harder than application CI because the target is not the host. Account for this in every pipeline decision.
- Hardware is a scarce, shared resource. CI must work reliably without physical hardware wherever possible.
- Binary constraints (flash, RAM, timing) are hard limits. Catching violations in CI is cheaper than catching them in the field.
- Reproducibility is critical — a firmware that builds differently on different machines causes production incidents.

## Firmware Builds

- Build firmware in CI for every target and configuration required to preserve PR confidence. Full supported matrices may run on main, nightly, or release workflows.
- Use the official toolchain (e.g., ESP-IDF, ARM GCC) pinned to a specific version. Never use the "latest" toolchain in CI.
- Document the exact toolchain version in the repository. Make it easy to replicate the CI environment locally.
- Build debug variants for diagnostics and release variants for size, optimization, and production behavior. Use PR/main/release scope to control where each variant runs.
- Treat build warnings as errors. Embedded code must compile cleanly.

## Build Matrix Scope

- PR builds should cover the smallest target and configuration matrix that preserves confidence.
- Main, nightly, and release builds should cover the full supported matrix.
- Matrix dimensions should include: board, MCU, build type, feature flags, SDK/toolchain version, and partition layout when they affect binary behavior.
- Exclude unsupported or redundant combinations explicitly rather than letting them fail at runtime.

## Cross-Toolchain Management

- Pin all cross-compilation toolchains to specific versions. Document where to obtain them.
- Cache toolchain downloads in CI — they are large and slow to download.
- Validate the toolchain checksum on first use to detect corrupted downloads.
- Use Docker images with the toolchain pre-installed where available to eliminate download time and ensure consistency.

## ESP-IDF CI

- Use the official ESP-IDF Docker image pinned to the required IDF version.
- Cache the IDF component manager dependencies.
- Run `idf.py build` for all relevant targets in parallel.
- Capture the build size report (`idf.py size`) as a build artifact.
- Fail the build if flash usage exceeds the budget.

## Embedded C++ CI

- Enforce a strict C++ standard version in CI — do not rely on compiler defaults.
- Enable all relevant compiler warnings (`-Wall -Wextra -Wpedantic`) and treat them as errors.
- Run static analysis on every PR.
- Use sanitizers (AddressSanitizer, UBSanitizer) on host-compiled test builds to catch memory errors.

## Multi-Target Firmware

- Build for all supported hardware targets in parallel using a matrix strategy.
- Use a shared build configuration where possible and isolate target-specific overrides.
- Ensure that each target's binary is validated independently — a passing build on one target does not imply passing on another.

## Firmware Artifact Strategy

- Store every artifact required for debugging or release: ELF, BIN/HEX/UF2, map file, symbol file, size report, partition table, bootloader, and OTA package.
- Artifacts must be traceable to: source revision, target, build type, toolchain version, SDK version, feature flags, and partition layout.
- Retain release artifacts longer than PR artifacts.
- Never rebuild firmware to recover a missing release artifact. If the artifact is gone, the release is gone.

## Bootloader / Partition Compatibility

- Validate bootloader, partition table, firmware image, and OTA package compatibility together.
- Fail CI when firmware no longer fits the configured partition.
- Validate upgrade paths from the previous production firmware to the new firmware.
- Check firmware version metadata and downgrade-prevention behavior.

## Resource Budgets

- Define explicit budgets for: flash, static RAM, stack, heap, boot time, CPU usage, power, and binary growth rate.
- Budgets must be target-specific — one budget does not apply across different boards or configurations.
- Report resource usage deltas on every relevant PR. Reviewers must be aware of size and memory impact.
- Treat regressions against budget as quality failures.

## Hardware Simulation

- Use hardware simulators (QEMU, Renode, ESP32 QEMU fork) to run firmware tests without physical hardware.
- Validate that simulator results match hardware results periodically on real devices.
- Document the known differences between simulator and hardware behavior.
- Simulator-based tests catch logic errors but not hardware-specific timing or power behavior — be explicit about what is and isn't covered.

## Emulator Testing

- Run application logic tests compiled for the host (with hardware abstraction layers mocked) to maximize test coverage without hardware.
- Run emulator tests in CI for every PR — they are fast and catch most logic errors.
- Reserve physical hardware tests for integration and release validation.
- Track which tests run only on hardware and why.

## Hardware-in-the-Loop (HIL)

- HIL should validate behavior that simulation cannot prove: real peripherals, timing, radio behavior, power behavior, flashing, reboot, and OTA.
- Treat HIL hardware as a scarce, serialized resource. Queue and isolate jobs accordingly.
- HIL jobs must be isolated by device, board revision, and firmware target.
- Always restore HIL devices to a known good state before and after tests.
- Capture serial logs, power/reset events, firmware version, and device identifiers as artifacts for every HIL run.

## Hardware Fleet Management

- Track board inventory, board revision, firmware currently flashed, attached peripherals, calibration state, and known defects.
- Quarantine unreliable or failing hardware immediately. Flaky hardware produces flaky CI.
- Assign ownership for maintaining each class of test hardware.
- Replace or recalibrate test hardware on a defined schedule when measurement accuracy matters.

## Flashing & Provisioning

- Flashing must be automated, repeatable, and logged.
- Validate that the flashed firmware matches the expected artifact digest before running tests.
- Provisioning steps must be explicit and reproducible.
- Secrets, certificates, keys, and device identities used during provisioning must never appear in build artifacts or logs.
- Test devices must be distinguishable from production devices.

## Runtime Diagnostics

- Capture boot logs, reset reason, crash dumps, core dumps, panic output, and watchdog events when available.
- Symbolicate crashes using the exact ELF/symbol file from the CI artifact — never from a locally rebuilt binary.
- Fail CI on unexpected resets, watchdog triggers, panics, or boot loops.
- Preserve all diagnostic artifacts from failed hardware and OTA tests.

## Radio / Connectivity Testing

- Test Wi-Fi, BLE, Zigbee, Matter, Thread, or other radios on real hardware when supported.
- Validate provisioning, reconnect, timeout, reboot recovery, and poor-signal behavior.
- Keep radio tests isolated from unstable shared networks where practical.
- Record the network configuration used during tests as part of the test artifact.

## Power / Timing Testing

- Validate boot time, sleep current, wake behavior, watchdog timing, and critical real-time deadlines on real hardware.
- Simulation is not sufficient for timing- or power-sensitive validation.
- Power measurements must define fixture, method, tolerance, and pass/fail threshold.
- Track power and timing regressions over time.

## Flash Size Validation

- Fail the build if total flash usage exceeds the budget for the target.
- Report flash usage delta on every relevant PR.
- Separate flash usage by component (application, libraries, data, bootloader) for actionable reports.
- Track flash usage over time to identify gradual growth before it becomes a problem.

## OTA Package Generation

- Generate OTA update packages as part of the release pipeline, not as a manual step.
- Validate the OTA package before distribution: signature, size, version metadata, and update compatibility.
- Test the OTA update process against the previous release version in CI using a simulator or HIL device.
- Store OTA packages with full traceability: commit SHA, build configuration, toolchain version.
- Never distribute an OTA package that has not been validated by CI.

## Release Readiness

- Release firmware must pass: the full supported matrix, required HIL tests, OTA validation, all size and memory budgets, and artifact traceability checks.
- Release candidates must be built once and promoted — never rebuilt for release.
- Release evidence must include: firmware artifacts, build logs, size reports, test reports, SBOM/provenance if used, and OTA validation results.
