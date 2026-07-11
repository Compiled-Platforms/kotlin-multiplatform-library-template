---
name: write-code
description: Write production-quality Kotlin Multiplatform code for this project. Use when implementing features, adding classes, writing functions, or making any code changes.
---

# Write Code

> If context shifts to a different task type, re-read `.cursor/rules/development-process/skill-context.mdc` and switch skills accordingly.

Before writing any code, read the following project rules:

## Always apply
- `.cursor/rules/coding-guidelines/code-style.mdc` — clarity, readability, maintainability
- `.cursor/rules/coding-guidelines/naming-conventions.mdc` — names must reveal intent
- `.cursor/rules/coding-guidelines/comment-usage.mdc` — comments explain why, not what
- `.cursor/rules/coding-principles/principle-of-least-exposure.mdc` — default to `internal`
- `.cursor/rules/coding-principles/dry.mdc` — no duplication
- `.cursor/rules/coding-principles/kiss.mdc` — prefer simple solutions
- `.cursor/rules/coding-principles/yagni.mdc` — only what is needed now
- `.cursor/rules/coding-principles/composition-over-inheritance.mdc`
- `.cursor/rules/coding-principles/solid/single-responsibility-principle.mdc`
- `.cursor/rules/coding-principles/solid/open-closed-principle.mdc`
- `.cursor/rules/coding-principles/solid/liskov-substitution-principle.mdc`
- `.cursor/rules/coding-principles/solid/interface-segregation-principle.mdc`
- `.cursor/rules/coding-principles/solid/dependency-inversion-principle.mdc`

## Apply when relevant
- `.cursor/rules/coding-guidelines/thread-safety.mdc` — any shared mutable state or concurrency
- `.cursor/rules/kotlin/structured-concurrency.mdc` — any coroutines or suspend functions
- `.cursor/rules/kotlin/reactive-programming.mdc` — any Flow usage
- `.cursor/rules/kotlin/multiplatform/multiplatform-structured-concurrency.mdc` — KMP coroutine patterns
- `.cursor/rules/kotlin/multiplatform/multiplatform-reactive-programming.mdc` — KMP Flow patterns
- `.cursor/rules/kotlin/multiplatform/android/android-reactive-programming.mdc` — Android-specific Flow/coroutine patterns
- `.cursor/rules/kotlin/multiplatform/ios/ios-reactive-programming.mdc` — iOS-specific reactive patterns

## Detekt (required before finishing code)

Pre-commit (lefthook) and CI run Detekt. Source of truth: `config/detekt/detekt.yaml`.

After non-trivial Kotlin edits, run the affected module (or root) **before** claiming the work is done or handing the user a commit command:

```bash
./gradlew :libraries:<name>:detekt
# or
./gradlew detekt
```

**Limits that commonly break Compose UI work** — design for these; do not discover them at commit time:

| Rule | Limit | What to do |
|---|---|---|
| `LongMethod` | 60 lines | Extract helpers / private composables |
| `CyclomaticComplexMethod` | 14 | Split branches; extract `when` arms |
| `NestedBlockDepth` | 4 | Flatten nesting |
| `TooManyFunctions` | 15 per file | Split file (e.g. `XxxDefaults.kt`, `XxxLogic.kt`) |
| `LargeClass` | 600 lines | Split types / files |
| `LongParameterList` | 5 function params | Prefer a params/state holder, or match existing narrow `@Suppress` on large composables |

Prefer extraction over `@Suppress`. Suppress only when the function truly cannot shrink without hurting clarity (e.g. IME wiring already suppressed on `SlotInput`), and keep the annotation as narrow as possible.
