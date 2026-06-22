---
name: publish-library
description: Publish Compiled Platforms KMP libraries to GitHub Packages. Use when the user wants to publish, release, or deploy a library, asks about versioning a release, or asks how consumers add the library as a dependency.
---

# Publish Library

Private KMP libraries published to GitHub Packages under `com.compiledplatforms`.
No signing. Triggered automatically on GitHub Release publish.

## Publishing target

```
https://maven.pkg.github.com/Compiled-Platforms/kotlin-multiplatform-suite-internal
```

Configured in `project.yml` — all other targets (Maven Central, JFrog, CloudSmith) are off.

## Release workflow

```bash
# 1. Ensure all changes are committed and on main
git status

# 2. Create a GitHub Release (triggers publish.yml automatically)
gh release create v<VERSION> --title "v<VERSION>" --notes "Release notes"

# VERSION must match gradle.properties VERSION_NAME
```

The workflow at `.github/workflows/publish.yml` runs on `release: published` and
calls `./gradlew publish` with GitHub Packages credentials injected automatically via `GITHUB_TOKEN`.

## Test locally before releasing

```bash
# Validate config
python3 scripts/get-publishing-config.py --validate

# Publish to local Maven (smoke test — no credentials needed)
./gradlew publishToMavenLocal

# Check artifacts
ls ~/.m2/repository/com/compiledplatforms/
```

## Versioning

Version is set in `gradle.properties`:
```properties
VERSION_NAME=1.3.2       # release
VERSION_NAME=1.4.0-SNAPSHOT  # dev snapshot
```

Follows semantic versioning. Managed by semantic-release on main branch merges.
Do not manually edit `VERSION_NAME` unless overriding a release.

## BOM

All libraries share the same version (lockstep). The BOM at `:bom` constrains all
`com.compiledplatforms` artifacts to `VERSION_NAME`. Add new libraries to `bom/build.gradle.kts`.

## Consumer setup

**`settings.gradle.kts`:**
```kotlin
maven {
    url = uri("https://maven.pkg.github.com/Compiled-Platforms/kotlin-multiplatform-suite-internal")
    credentials {
        username = providers.gradleProperty("gpr.user").orNull
        password = providers.gradleProperty("gpr.token").orNull
    }
}
```

**`~/.gradle/gradle.properties` (consumer's machine — never commit):**
```properties
gpr.user=GITHUB_USERNAME
gpr.token=ghp_TOKEN  # needs read:packages scope
```

**`build.gradle.kts`:**
```kotlin
// Recommended: use BOM
implementation(platform("com.compiledplatforms:bom:<version>"))
implementation("com.compiledplatforms:in-app-reviews")
implementation("com.compiledplatforms:eligibility-gate")
```

## Client access management

Access is granted via a GitHub classic PAT with `read:packages` scope. The token
is tied to the `aiithak` account (org owner), so it always has access to
Compiled-Platforms packages regardless of any client-side repo changes.

### Onboarding a new client

1. Generate a new classic PAT from [github.com/settings/tokens](https://github.com/settings/tokens):
   - Name: `compiled-platforms-packages-read-<clientname>`
   - Expiration: No expiration
   - Scope: `read:packages` only
2. Send the client:
   ```
   Maven repo: https://maven.pkg.github.com/Compiled-Platforms/kotlin-multiplatform-suite-internal
   Username: aiithak
   Token: ghp_xxxxxxxxxxxx
   ```
3. Direct them to `docs/development/client-access.md` for setup instructions.

### Offboarding a client

Revoke their token at [github.com/settings/tokens](https://github.com/settings/tokens).
Their builds will immediately get 401 errors on next dependency resolution.

### Upgrading to per-client isolation

When you have multiple clients and need independent revocation:
- Create one GitHub bot account per client (costs $4/seat/month on Team plan)
- Add each bot as a Read collaborator on this repo
- Generate a PAT from each bot account
- Revoke access by removing the bot collaborator — does not affect other clients

## Adding a new library to publishing

1. Add `mavenPublishing { pom { name = "..."; description = "..." } }` to the library's `build.gradle.kts`
2. Add the artifact constraint to `bom/build.gradle.kts`
3. The convention plugin (`convention.library`) handles the rest automatically

## Switching publish target

To switch from GitHub Packages to another target (JFrog, CloudSmith, etc.):
1. Edit `project.yml` — flip `github_packages: enabled: false`, enable the new target
2. Update consumer `settings.gradle.kts` with new repository URL + credentials
3. No other code changes needed
