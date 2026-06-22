---
name: debug
description: Investigate and fix bugs, build failures, test failures, and runtime errors in this KMP project. Use when the user pastes an error, reports unexpected behavior, asks to debug something, or when a command you run fails.
---

# Debug

> If context shifts to a different task type, re-read `.cursor/rules/development-process/skill-context.mdc` and switch skills accordingly.

Before investigating, read:

- `.cursor/rules/development-process/debugging.mdc` — primary source of truth for debug standards
- `.cursor/rules/coding-guidelines/thread-safety.mdc` — when concurrency or shared state is involved
- `.cursor/rules/kotlin/structured-concurrency.mdc` — when coroutines or suspend functions are involved
- `.cursor/rules/kotlin/multiplatform/multiplatform-structured-concurrency.mdc` — when the failure is KMP-specific

## Process

### 1. Capture the failure

- Record the exact error message, exit code, and command that failed
- Note platform(s): JVM, Android, iOS, JS, WASM, Linux, CI check name
- Distinguish expected vs actual behavior

### 2. Gather evidence — do not guess

- Read the full stack trace or CI log — start from the first actionable error, not the last line
- Locate the failing test, Gradle task, or source file
- Reproduce locally when possible:

```bash
# Single library JVM tests
./gradlew :libraries:<name>:jvmTest

# Platform-scoped tests (from repo root)
python3 scripts/test_platforms.py --platforms jvm

# Lint / static analysis
./gradlew detekt

# Full build (when needed)
./gradlew build
```

- If reproduction is not possible (e.g. iOS on Linux), say so and work from the available log

### 3. Form a hypothesis

- State what you think is wrong and why, in one sentence
- Point to the specific file, line, or task if known

### 4. Fix minimally

- Switch to `write-code` for the production fix
- Switch to `write-tests` if the fix needs a regression test
- Do not refactor unrelated code

### 5. Verify

- Re-run the exact command or test that failed
- For KMP changes, verify at least the failing platform; broaden only when the fix is cross-platform

### 6. Report

- Root cause (one sentence)
- What changed and why
- Command(s) used to verify
