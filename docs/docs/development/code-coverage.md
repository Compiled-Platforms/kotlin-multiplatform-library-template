# Code Coverage with Kover

This template uses [Kover](https://github.com/Kotlin/kotlinx-kover) (Kotlinx Code Coverage) to measure test coverage across all library modules.

## What is Kover?

**Kover** is JetBrains' official code coverage tool for Kotlin, designed specifically for Kotlin Multiplatform projects. It provides:

- **Multiplatform Support**: Works with JVM, Android, and (experimentally) Native targets
- **Kotlin-First**: Better Kotlin support than traditional tools like JaCoCo
- **Gradle Integration**: Seamless integration with Gradle builds
- **Aggregated Reports**: Combine coverage from multiple modules
- **Verification Rules**: Enforce minimum coverage thresholds

## How It Works

Kover instruments your code during test execution to track which lines and branches are executed. After tests run, it generates reports showing:

- **Line Coverage**: Percentage of code lines executed by tests
- **Branch Coverage**: Percentage of conditional branches taken
- **Class/Package Coverage**: Coverage broken down by structure
- **Missed Lines**: Exact lines not covered by tests

## Configuration

Kover is configured in two places:

### 1. Convention Plugin (Per-Library)

Each library automatically gets Kover applied via the `convention.library` plugin:

```kotlin
// build-logic/convention/src/main/kotlin/KmpLibraryConventionPlugin.kt
with(pluginManager) {
    apply("org.jetbrains.kotlinx.kover")
}
```

### 2. Root Build (Aggregation)

The root `build.gradle.kts` aggregates coverage from all libraries:

```kotlin
dependencies {
    // Add library projects to coverage aggregation
    subprojects.forEach { subproject ->
        if (subproject.path.startsWith(":libraries:")) {
            kover(subproject)
        }
    }
}

kover {
    reports {
        filters {
            excludes {
                // Exclude generated code
                classes("*.BuildConfig")
                classes("*.ComposableSingletons*")
                classes("*_Factory")
                classes("*_MembersInjector")
                
                // Exclude internal packages
                packages("*.internal")
                packages("*.internal.*")
            }
        }
    }
}
```

## Gradle Tasks

Kover provides several tasks for generating reports and verifying coverage:

### Generate HTML Report

```bash
./gradlew koverHtmlReport
```

**Output:** `build/reports/kover/html/index.html`

Opens a visual HTML report showing coverage by package, class, and line. This is the most user-friendly format for exploring coverage.

### Generate XML Report

```bash
./gradlew koverXmlReport
```

**Output:** `build/reports/kover/report.xml`

Generates an XML report in JaCoCo format, compatible with CI tools, coverage badges, and services like Codecov or Coveralls.

### Verify Coverage Thresholds

```bash
./gradlew koverVerify
```

Checks that coverage meets the configured minimum thresholds. Fails the build if coverage is below the threshold (currently set to 70% line coverage).

### Generate All Reports

```bash
./gradlew koverHtmlReport koverXmlReport koverVerify
```

Generates both HTML and XML reports, then verifies thresholds.

### Per-Library Reports

Each library also has its own coverage tasks:

```bash
# Generate HTML report for a specific library
./gradlew :libraries:example-library:koverHtmlReport

# Verify coverage for a specific library
./gradlew :libraries:example-library:koverVerify
```

**Output:** `libraries/example-library/build/reports/kover/html/index.html`

## Coverage Thresholds

The template enforces minimum coverage thresholds to maintain code quality. These are configured in the root `build.gradle.kts`:

```kotlin
kover {
    reports {
        verify {
            rule {
                minBound(70) // Minimum 70% line coverage
            }
        }
    }
}
```

### Adjusting Thresholds

To change the minimum coverage percentage:

```kotlin
kover {
    reports {
        verify {
            rule {
                minBound(80) // Increase to 80%
            }
        }
    }
}
```

### Per-Library Thresholds

You can also set different thresholds for individual libraries:

```kotlin
// libraries/your-library/build.gradle.kts
kover {
    reports {
        verify {
            rule {
                minBound(90) // This library requires 90% coverage
            }
        }
    }
}
```

## Excluding Code from Coverage

### 1. Exclude Packages

Exclude entire packages from coverage (already configured for `*.internal`):

```kotlin
kover {
    reports {
        filters {
            excludes {
                packages("com.example.experimental")
                packages("com.example.generated.*")
            }
        }
    }
}
```

### 2. Exclude Classes

Exclude specific class patterns:

```kotlin
kover {
    reports {
        filters {
            excludes {
                classes("*Test")
                classes("*\$Companion")
                classes("*.BuildConfig")
            }
        }
    }
}
```

### 3. Exclude Annotations

Exclude code annotated with specific annotations:

```kotlin
// Define annotation
@Target(AnnotationTarget.CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
annotation class ExcludeFromCoverage

// Configure Kover
kover {
    reports {
        filters {
            excludes {
                annotatedBy("com.example.ExcludeFromCoverage")
            }
        }
    }
}

// Use in code
@ExcludeFromCoverage
fun experimentalFeature() {
    // This won't be counted in coverage
}
```

## Writing Tests for Coverage

### Good Coverage Practices

1. **Test Public APIs**: Focus on testing public interfaces, not internal implementation
2. **Test Edge Cases**: Cover boundary conditions, null cases, empty collections
3. **Test Error Paths**: Don't just test the happy path
4. **Keep Tests Simple**: One test should verify one behavior

### Example: Improving Coverage

**Before (50% coverage):**

```kotlin
// Source
fun calculateDiscount(price: Double, percentage: Int): Double {
    if (percentage < 0 || percentage > 100) {
        throw IllegalArgumentException("Invalid percentage")
    }
    return price * (percentage / 100.0)
}

// Test
@Test
fun testCalculateDiscount() {
    assertEquals(10.0, calculateDiscount(100.0, 10))
}
```

**After (100% coverage):**

```kotlin
// Tests
@Test
fun testCalculateDiscount() {
    assertEquals(10.0, calculateDiscount(100.0, 10))
}

@Test
fun testCalculateDiscountZeroPercent() {
    assertEquals(0.0, calculateDiscount(100.0, 0))
}

@Test
fun testCalculateDiscountFullPercent() {
    assertEquals(100.0, calculateDiscount(100.0, 100))
}

@Test
fun testCalculateDiscountNegativePercentThrows() {
    assertFailsWith<IllegalArgumentException> {
        calculateDiscount(100.0, -1)
    }
}

@Test
fun testCalculateDiscountOverHundredThrows() {
    assertFailsWith<IllegalArgumentException> {
        calculateDiscount(100.0, 101)
    }
}
```

## CI/CD Integration

Kover is integrated into the GitHub Actions CI/CD pipeline:

### Build Workflow

The `build.yml` workflow runs coverage as part of the build:

```yaml
- name: Run Tests with Coverage
  run: ./gradlew koverXmlReport koverVerify --daemon

- name: Upload Coverage Reports
  uses: actions/upload-artifact@v4
  with:
    name: coverage-reports
    path: |
      **/build/reports/kover/**
```

### Coverage Badges (Optional)

You can integrate with services like Codecov or Coveralls:

#### Codecov

```yaml
- name: Upload to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: build/reports/kover/report.xml
    flags: unittests
    name: codecov-umbrella
```

#### Coveralls

```yaml
- name: Upload to Coveralls
  uses: coverallsapp/github-action@v2
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    path-to-lcov: build/reports/kover/report.xml
```

## Interpreting Coverage Reports

### HTML Report Structure

The HTML report (`build/reports/kover/html/index.html`) shows:

1. **Overview**: Total coverage percentage across all modules
2. **Packages**: Coverage broken down by package
3. **Classes**: Coverage for each class
4. **Source View**: Line-by-line coverage with color coding:
   - **Green**: Line covered by tests
   - **Red**: Line not covered
   - **Yellow**: Partially covered (branch coverage)

### What is Good Coverage?

- **70-80%**: Acceptable for most projects
- **80-90%**: Good coverage, most code paths tested
- **90%+**: Excellent coverage, high confidence
- **100%**: Perfect coverage (often impractical/unnecessary)

### Coverage vs. Quality

⚠️ **Important**: High coverage doesn't guarantee good tests!

```kotlin
// 100% coverage, but useless test
@Test
fun testCalculate() {
    calculate(1, 2) // No assertion!
}
```

Focus on **meaningful tests** that verify behavior, not just coverage numbers.

## Troubleshooting

### Coverage is 0% or Missing

**Cause**: Tests aren't running or Kover isn't instrumenting correctly.

**Solution**:
```bash
# Clean and rebuild
./gradlew clean
./gradlew test koverHtmlReport
```

### "No coverage data found"

**Cause**: No tests executed.

**Solution**: Ensure you have tests and they're running:
```bash
./gradlew test --info
```

### Coverage Lower Than Expected

**Cause**: Some code paths aren't tested.

**Solution**: Open the HTML report and look for red (uncovered) lines. Write tests for those paths.

### Kover Task Not Found

**Cause**: Plugin not applied.

**Solution**: Ensure the library uses the `convention.library` plugin:
```kotlin
plugins {
    id("convention.library")
}
```

### Multiplatform Coverage Issues

**Note**: Kover currently has best support for JVM and Android targets. Native target coverage is experimental.

For multiplatform projects:
- JVM tests: ✅ Full coverage support
- Android tests: ✅ Full coverage support  
- Native tests: ⚠️ Experimental/limited support

## Best Practices

### 1. Run Coverage Locally

Before pushing, check coverage:
```bash
./gradlew koverHtmlReport
open build/reports/kover/html/index.html
```

### 2. Don't Obsess Over 100%

Focus on testing critical paths. Some code (like simple getters, logging, or error messages) doesn't need tests.

### 3. Use Coverage to Find Gaps

Use coverage reports to identify:
- Untested error handling
- Missing edge case tests
- Dead code (0% coverage might mean unused code)

### 4. Exclude Generated Code

Always exclude generated code from coverage:
```kotlin
excludes {
    classes("*.BuildConfig")
    classes("*_Factory")
    packages("*.generated")
}
```

### 5. Set Realistic Thresholds

Start with a lower threshold (e.g., 60%) and gradually increase as you add tests. Don't set 90% if your current coverage is 40%.

### 6. Review Coverage in PRs

Make coverage part of your code review process:
1. Check if new code has tests
2. Ensure coverage doesn't decrease
3. Look at coverage diff, not just total percentage

## Resources

- [Kover Documentation](https://kotlin.github.io/kotlinx-kover/)
- [Kover GitHub](https://github.com/Kotlin/kotlinx-kover)
- [Gradle Plugin Portal](https://plugins.gradle.org/plugin/org.jetbrains.kotlinx.kover)
- [JaCoCo XML Format](https://www.jacoco.org/jacoco/trunk/doc/report.html)

## Quick Reference

```bash
# Generate HTML coverage report
./gradlew koverHtmlReport

# Generate XML coverage report (for CI/badges)
./gradlew koverXmlReport

# Verify coverage meets thresholds
./gradlew koverVerify

# Generate all reports and verify
./gradlew koverHtmlReport koverXmlReport koverVerify

# Per-library coverage
./gradlew :libraries:example-library:koverHtmlReport

# Clean and regenerate
./gradlew clean koverHtmlReport
```

**Report Locations:**
- Root aggregated: `build/reports/kover/html/index.html`
- Per-library: `libraries/*/build/reports/kover/html/index.html`
- XML (CI): `build/reports/kover/report.xml`

**Golden Rule:** Coverage is a tool to find untested code, not a goal in itself. Write meaningful tests that verify behavior!
