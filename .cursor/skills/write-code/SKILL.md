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
