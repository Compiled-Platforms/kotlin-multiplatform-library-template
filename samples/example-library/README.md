# Example Library Sample

A sample application demonstrating the use of `example-library`.

## What This Sample Demonstrates

- ✅ Generating Fibonacci sequences using `generateFibi()`
- ✅ Taking a limited number of elements from the sequence
- ✅ Calculating sums of sequence elements
- ✅ Filtering sequences with `takeWhile`
- ✅ Basic sequence operations in Kotlin

## Running the Sample

### From Command Line

```bash
# From the root of the monorepo
./gradlew :samples:example-library:run
```

### Expected Output

```
=== Example Library Sample ===

First 10 Fibonacci numbers:
F(0) = 0
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(9) = 34

Sum of first 10 Fibonacci numbers: 88

Fibonacci numbers less than 100:
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
```

## Code Structure

- `src/commonMain/kotlin/Main.kt` - Main sample logic (platform-agnostic)
- `src/jvmMain/kotlin/JvmMain.kt` - JVM entry point

## Dependencies

This sample uses:
- `example-library` (from this monorepo)

## Learning More

- See [example-library documentation](../../libraries/example-library/README.md)
- Explore the [library source code](../../libraries/example-library/src/commonMain/kotlin/)
- Check out [library tests](../../libraries/example-library/src/commonTest/kotlin/) for more usage examples
