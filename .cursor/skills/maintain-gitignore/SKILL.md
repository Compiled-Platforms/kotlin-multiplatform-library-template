---
name: maintain-gitignore
description: Maintain .gitignore when adding, updating, or removing dependencies in Kotlin Multiplatform projects. Use when working with dependencies, build configurations, or when the user mentions adding libraries, updating gradle files, or .gitignore maintenance.
---

# Maintain .gitignore for KMP Projects

## Purpose

Ensure .gitignore stays current when dependencies change, preventing unwanted artifacts from being committed while preserving intentional files like API dumps.

## When to Use

- Adding new dependencies to `libs.versions.toml` or `build.gradle.kts`
- Updating existing library versions
- Removing dependencies
- User explicitly asks about .gitignore
- After observing new build artifacts in `git status`

## Process

### 1. Identify Library-Specific Artifacts

When a dependency is added, check for:
- **Cache directories** - Library-specific build caches
- **Generated files** - Code generation outputs
- **Platform artifacts** - Native binaries, frameworks
- **IDE integration** - Plugin-generated files

### 2. Check Library Documentation

Look for recommended .gitignore entries in:
- Library's README or setup docs
- GitHub repository .gitignore
- Official integration guides

### 3. Test Locally

Run a build to identify generated files:

```bash
./gradlew clean build
git status
```

Look for untracked files that shouldn't be committed.

## Common Library Patterns

### Database Libraries

```gitignore
# SQLite
*.db
*.sqlite
*.db-shm
*.db-wal

# Realm
*.realm
*.realm.lock
*.realm.management/

# SQLDelight
.sqldelight/
```

### Code Generation

```gitignore
# KSP (Kotlin Symbol Processing)
**/generated/ksp/

# Kapt
**/generated/kapt/

# BuildConfig
**/generated/buildconfig/
```

### Compose Multiplatform

```gitignore
# Compose
**/compose/
composeResources/
```

### Network Libraries

```gitignore
# Ktor
.ktor/

# Apollo GraphQL
.apollo/
**/generated/apollo/
```

### Native/iOS

```gitignore
# Frameworks
*.xcframework/
*.framework/

# CocoaPods
Pods/
*.xcworkspace
Podfile.lock
```

### Serialization

```gitignore
# kotlinx-serialization generated schemas
**/generated/serialization/
```

## Update .gitignore

1. **Find the appropriate section** - Group by category (Kotlin, Android, iOS, Build tools, etc.)
2. **Add entries with comments** - Explain non-obvious entries
3. **Keep organized** - Maintain consistent formatting
4. **Test** - Run `git status` to verify

### Example Addition

```gitignore
# SQLDelight (added 2026-01-28)
.sqldelight/
**/generated/sqldelight/
```

## Verification Checklist

After updating .gitignore:
- [ ] Run `./gradlew clean build` to regenerate artifacts
- [ ] Check `git status` - unwanted files should not appear
- [ ] Verify intentional files still tracked (e.g., `**/api/*.api` dumps)
- [ ] Commit .gitignore changes with dependency changes

## Platform-Specific Considerations

### Android
When adding Android-specific libraries, check for:
- R8/ProGuard outputs (`mapping.txt`, `seeds.txt`)
- Lint reports
- APK/AAB files in non-standard locations

### iOS
When adding iOS/native libraries, check for:
- Xcode derived data
- Framework binaries
- CocoaPods artifacts

### Desktop (JVM)
When adding desktop-specific libraries, check for:
- Distribution packages (`*.dmg`, `*.exe`, `*.deb`)
- Native launchers

## Don't Ignore

**Keep these tracked:**
- `**/api/**/*.api` - Binary compatibility validator dumps
- `gradle/wrapper/gradle-wrapper.jar` - Gradle wrapper
- Documentation files
- Test fixtures
- Example configurations (non-sensitive)

## Example Workflow

**Scenario:** Adding SQLDelight to the project

1. **Add dependency** to `libs.versions.toml`:
   ```toml
   sqldelight = "2.0.0"
   ```

2. **Run build**:
   ```bash
   ./gradlew build
   ```

3. **Check git status**:
   ```bash
   git status
   # Shows: .sqldelight/ directory
   ```

4. **Update .gitignore**:
   ```gitignore
   # SQLDelight
   .sqldelight/
   ```

5. **Verify**:
   ```bash
   git status
   # .sqldelight/ no longer appears
   ```

6. **Commit together**:
   ```bash
   git add libs.versions.toml .gitignore
   git commit -m "feat(deps): add SQLDelight for database management"
   ```

## Quick Reference

| Library Type | Common Patterns |
|--------------|-----------------|
| Database | `*.db`, `.sqldelight/`, `*.realm` |
| Code Gen | `**/generated/`, `.apollo/` |
| Network | `.ktor/` |
| UI | `composeResources/` |
| Native | `*.xcframework/`, `DerivedData/` |
