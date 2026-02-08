# Example Library – JVM CLI Sample

JVM command-line sample for `example-library`.

## What This Sample Demonstrates

- Generating Fibonacci sequences using `generateFibi()`
- Taking elements, sums, and filtering with `takeWhile`
- Basic sequence operations in Kotlin

## Run

```bash
./gradlew :samples:example-library:jvm-cli:run
```

## Structure

- `src/commonMain/kotlin/Main.kt` – shared logic
- `src/jvmMain/kotlin/JvmMain.kt` – JVM entry point

Depends on `example-library` from this monorepo.
