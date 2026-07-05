# Dependency Updates with Dependabot

This template uses [Dependabot](https://docs.github.com/en/code-security/dependabot) to automatically keep dependencies up-to-date.

## What is Dependabot?

**Dependabot** is GitHub's built-in dependency update tool that:

- 🔍 **Monitors** your dependencies for new versions
- 📬 **Creates PRs** automatically when updates are available
- 📦 **Groups** related updates into single PRs
- 🔒 **Checks** for security vulnerabilities
- ⚡ **Works** immediately with no external app installation

## How It Works

Dependabot runs on a schedule and:

1. Scans your `libs.versions.toml`, `build.gradle.kts`, GitHub Actions, and Python dependencies
2. Checks for newer versions
3. Creates grouped pull requests with updates
4. Includes changelogs and compatibility information
5. Runs your CI/CD tests automatically

## Configuration

Dependabot is configured in `.github/dependabot.yml`. Gradle updates are grouped into a single weekly PR; compatibility-sensitive stacks are ignored and bumped manually.

```yaml
version: 2
updates:
  - package-ecosystem: "gradle"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "03:00"
    open-pull-requests-limit: 1
    ignore:
      - dependency-name: "org.jetbrains.kotlin*"
        update-types: ["version-update:semver-major", "version-update:semver-minor", "version-update:semver-patch"]
      - dependency-name: "com.android*"
        update-types: ["version-update:semver-major", "version-update:semver-minor", "version-update:semver-patch"]
      - dependency-name: "org.jetbrains.compose*"
        update-types: ["version-update:semver-major", "version-update:semver-minor", "version-update:semver-patch"]
      - dependency-name: "gradle-wrapper"
        update-types: ["version-update:semver-major", "version-update:semver-minor", "version-update:semver-patch"]
    groups:
      all-dependencies:
        patterns:
          - "*"
```

## Manually Managed Dependencies

Kotlin Multiplatform projects must stay within the [KMP compatibility guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html). Dependabot cannot pin a maximum version (for example, "AGP ≤ 9.1.0"); it can only skip updates entirely via `ignore`.

These ecosystems are **not** updated by Dependabot — bump them together in a deliberate migration:

| Pattern | Examples in `libs.versions.toml` |
|---------|----------------------------------|
| `org.jetbrains.kotlin*` | `kotlin`, Compose compiler plugin, serialization plugin |
| `com.android*` | AGP, `com.android.application`, KMP Android library plugin |
| `org.jetbrains.compose*` | Compose plugin, runtime, UI, Material3 |
| `gradle-wrapper` | Gradle wrapper (must stay within KMP Gradle range) |

## What Dependabot Still Updates

Low-risk dependencies that are not blocked by the ignore list, grouped into one weekly PR:

- **Dev tools** — Detekt, Dokka, Kover, Binary Compatibility Validator, Vanniktech Maven Publish, Mokkery
- **KotlinX libraries** — Coroutines, Serialization, DateTime (still verify against your Kotlin version)
- **Test libraries** — Kotest, Turbine
- **AndroidX** — Activity Compose, Lifecycle, Test Core

Review these PRs against changelogs; merge when CI is green.

## Other Ecosystems

### GitHub Actions
- All action updates grouped together
- Checked monthly

### MkDocs Dependencies
- MkDocs and plugins
- Checked monthly

## Update Schedule

| Package Ecosystem | Frequency | Day | Time (PST) |
|-------------------|-----------|-----|------------|
| Gradle (Kotlin, Android, etc.) | Weekly | Monday | 3:00 AM |
| GitHub Actions | Monthly | First Monday | N/A |
| Python (MkDocs) | Monthly | First Monday | N/A |

## Handling Dependabot PRs

### Minor/Patch Updates (Low Risk)

For updates like `1.2.3` → `1.2.4` or `1.2.0` → `1.3.0`:

1. **Review the PR** - Check the changelog and compatibility info
2. **Wait for CI** - Ensure all tests pass
3. **Merge** - If green, merge with confidence

**These are usually safe to merge quickly.**

### Major Updates (Breaking Changes)

For updates like `1.x.x` → `2.0.0`:

1. **Read release notes** - Major versions often have breaking changes
2. **Review deprecations** - Check what's deprecated or removed
3. **Test locally** - Pull the branch and test thoroughly
4. **Update code if needed** - Fix any breaking changes
5. **Update docs** - Document any migration steps

**Take your time with these.**

## Example PR Flow

### Typical Grouped PR

```
chore(deps): bump the following group with 3 updates
- mokkery: 3.4.1 → 3.4.2
- kotest: 6.2.1 → 6.2.2
- detekt: 2.0.0-alpha.5 → 2.0.0-alpha.6
```

**What to do:**
1. Confirm the PR does **not** include Kotlin, AGP, Compose, or Gradle wrapper bumps
2. Click "Files changed" to see what's updated
3. Check CI status (all checks should be green)
4. If tests pass → Merge

### Security Update PR

```
chore(deps): [SECURITY] update kotlin to 2.0.21
Fixes: CVE-2024-XXXXX
```

**What to do:**
1. **Merge immediately** after CI passes
2. Security updates should be prioritized

## Customizing Dependabot

### Change Update Frequency

Edit `.github/dependabot.yml`:

```yaml
schedule:
  interval: "daily"  # Options: daily, weekly, monthly
```

### Add New Groups

To group additional dependencies:

```yaml
groups:
  my-custom-group:
    patterns:
      - "com.example.*"
      - "org.mylib.*"
```

### Ignore Specific Updates

Dependabot does not support max-version pins (for example, `AGP <= 9.1.0`). To freeze a dependency, ignore all semver update types:

```yaml
ignore:
  - dependency-name: "com.android*"
    update-types:
      - "version-update:semver-major"
      - "version-update:semver-minor"
      - "version-update:semver-patch"
```

To ignore a specific version range instead of all updates:

```yaml
ignore:
  - dependency-name: "com.android.tools.build:gradle"
    versions: ["9.2.x", "9.3.x"]
```

If an `ignore` rule in `dependabot.yml` does not take effect for a Gradle **plugin** from the version catalog, comment on the PR:

```
@dependabot ignore dependency-name com.android.application
```

### Limit Open PRs

To control how many PRs Dependabot creates:

```yaml
open-pull-requests-limit: 5  # Max 5 open PRs at once
```

## Disabling Dependabot

If you want to disable Dependabot temporarily:

1. Go to your repository settings
2. Navigate to "Code security and analysis"
3. Disable "Dependabot version updates"

Or delete/rename `.github/dependabot.yml`.

## Dependabot Commands

You can control Dependabot by commenting on PRs:

- `@dependabot rebase` - Rebase the PR
- `@dependabot recreate` - Recreate the PR from scratch
- `@dependabot merge` - Merge the PR (if checks pass)
- `@dependabot squash and merge` - Squash and merge
- `@dependabot cancel merge` - Cancel auto-merge
- `@dependabot close` - Close the PR
- `@dependabot ignore this dependency` - Ignore this dependency
- `@dependabot ignore this major version` - Ignore this major version
- `@dependabot ignore this minor version` - Ignore this minor version

## Best Practices

### 1. Review Weekly

Set aside time each week (e.g., Monday morning) to review and merge Dependabot PRs.

### 2. Don't Let PRs Pile Up

Merge regularly to avoid conflicts between PRs. If you have 10+ open PRs, start merging the simple ones.

### 3. Test Major Updates Locally

Before merging major version updates:

```bash
# Fetch the Dependabot branch
git fetch origin dependabot/gradle/kotlin-2.0.0

# Check it out locally
git checkout dependabot/gradle/kotlin-2.0.0

# Build and test
./gradlew build
./gradlew test
```

### 4. Keep CI Green

Only merge PRs where CI is passing. If tests fail:
- Investigate the failure
- Fix in the Dependabot branch
- Or close the PR and wait for a better version

### 5. Update Dependabot Config

When you adopt a new Kotlin/AGP/Compose stack, update the ignore list if you start allowing Dependabot to manage a previously manual dependency.

### 6. Enable Auto-merge for Low-Risk Updates

You can enable auto-merge for patch-only Dependabot PRs that only touch allowed dependencies (dev tools, test libs, etc.).

Then use GitHub's auto-merge feature for these PRs.

## Troubleshooting

### Dependabot Proposes Kotlin, AGP, or Compose Updates

**Possible causes:**
- Ignore patterns in `dependabot.yml` do not match Gradle plugin IDs from the version catalog ([known limitation](https://github.com/dependabot/dependabot-core/issues/13937))
- PR was opened before ignore rules were merged

**Solution:**
1. Close the PR without merging
2. Add or broaden the `ignore` pattern in `.github/dependabot.yml`
3. Comment `@dependabot ignore this dependency` on the PR to persist the block
4. Bump the stack manually when the [KMP compatibility guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html) allows it

### Dependabot Not Creating PRs

**Possible causes:**
- Dependabot is disabled in repository settings
- Configuration file has syntax errors
- All dependencies are already up-to-date
- Rate limits reached

**Solution:**
1. Check `.github/dependabot.yml` for syntax errors
2. Go to "Insights" → "Dependency graph" → "Dependabot" to see status
3. Wait for the next scheduled run

### Too Many Open PRs

**Solution:**
- Increase grouping (fewer, larger groups)
- Reduce `open-pull-requests-limit`
- Merge more frequently

### Conflicting PRs

When multiple Dependabot PRs conflict:

1. **Merge one PR first** (usually the smallest/safest)
2. **Rebase the others**: Comment `@dependabot rebase` on each conflicting PR
3. Dependabot will automatically update them

### Updates Breaking CI

If a Dependabot PR breaks tests:

1. **Don't merge** - Close the PR
2. **Investigate** - Check if it's a real issue or flaky test
3. **Wait** - Often a patch release will fix the issue
4. **Report** - File an issue with the dependency maintainer if needed

## GitHub Dependency Graph

Dependabot integrates with GitHub's dependency graph:

**To view:**
1. Go to your repository
2. Click "Insights" tab
3. Click "Dependency graph"

**Features:**
- 📊 Visual dependency tree
- 🔒 Security vulnerability alerts
- 📈 Dependency update history
- 🔍 Dependabot status

## Security Alerts

Dependabot automatically creates PRs for security vulnerabilities:

- **Priority**: Security PRs are created immediately, not on schedule
- **Label**: Tagged with "security"
- **Action**: Merge ASAP after CI passes

**Example:**
```
chore(deps): [SECURITY] Bump kotlin from 1.9.0 to 1.9.10
Fixes CVE-2023-XXXXX
```

## Integration with CI/CD

Dependabot PRs automatically trigger your CI/CD:

- ✅ Build & Test workflow runs
- ✅ Detekt static analysis runs
- ✅ API compatibility check runs
- ✅ Code coverage verification runs
- ✅ All checks must pass before merge

This ensures updates don't break your library.

## Comparison with Renovate

If you're considering alternatives:

| Feature | Dependabot | Renovate |
|---------|------------|----------|
| **Built-in to GitHub** | ✅ Yes | ❌ No (app/self-host) |
| **Grouped updates** | ✅ Yes | ✅ Yes |
| **Monorepo support** | ✅ Yes | ✅ Yes (better) |
| **Gradle catalog support** | ✅ Yes | ✅ Yes |
| **Setup complexity** | 🟢 Simple | 🟡 Complex |
| **Customization** | 🟡 Good | 🟢 Excellent |
| **Max-version pinning** | ❌ No (`ignore` only) | ✅ Yes (`allowedVersions`) |
| **Dependency dashboard** | ❌ No | ✅ Yes |
| **Best for** | Templates, simplicity | Complex projects |

**For this template:** Dependabot is the right choice because it works immediately for template users with zero setup.

## Resources

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Configuration Options](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [Dependency Graph](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph)
- [Security Alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts)

## Quick Reference

```bash
# View Dependabot status
# Go to: Insights → Dependency graph → Dependabot

# Force Dependabot to check now
# Comment on any PR: @dependabot rebase

# Merge a Dependabot PR
git fetch origin
git checkout <dependabot-branch>
./gradlew build  # Test locally
git checkout develop
git merge <dependabot-branch>
git push
```

**Golden Rule:** Review, test, merge. Keep dependencies fresh, but don't rush major updates!
