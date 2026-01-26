# Release Process

This project uses automated tools to streamline the release process.

> **Note**: The initial baseline tag `v0.0.0` has been created. Future releases will automatically show changes since the previous version.

## Overview

- **Release Drafter**: Auto-generates draft releases from PRs and commits
- **git-cliff**: Generates beautiful changelogs from conventional commits
- **Conventional Commits**: Follow this format for automatic categorization

## Automated Release Drafts

Every push to `main` and every PR automatically updates a draft release in GitHub:

1. **View Draft Release**:
   - Go to: https://github.com/Compiled-Platforms/kotlin-multiplatform-library-template/releases
   - You'll see a draft release with auto-generated notes

2. **How It Works**:
   - Reads commit messages (conventional commits)
   - Groups changes by type (Features, Bug Fixes, etc.)
   - Suggests next version based on PR labels
   - Adds contributor credits

3. **PR Labels** (optional, for version bumping):
   - `major` or `breaking` → v2.0.0
   - `minor`, `feature`, or `enhancement` → v1.1.0
   - `patch`, `fix`, `bug`, or `chore` → v1.0.1

## Publishing a Release

### Manual Process

1. **Review Draft Release**:
   ```
   Go to Releases → Edit draft
   ```

2. **Update Version** (if needed):
   ```
   Edit the tag (e.g., v1.0.0)
   ```

3. **Review Release Notes**:
   ```
   Notes are auto-generated but you can edit them
   ```

4. **Publish**:
   ```
   Click "Publish release"
   ```

5. **Changelog Generated Automatically**:
   ```
   CHANGELOG.md is auto-committed to main
   ```

### What Happens After Publishing

When you publish a release:

1. ✅ Release is created on GitHub
2. ✅ `git-cliff` generates updated `CHANGELOG.md`
3. ✅ `CHANGELOG.md` is committed to `main`
4. ✅ Tag is created (e.g., `v1.0.0`)

## Conventional Commits

Use this format for commits to get automatic categorization:

### Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New features → 🚀 Features
- `fix`: Bug fixes → 🐛 Bug Fixes
- `docs`: Documentation → 📚 Documentation
- `perf`: Performance improvements → ⚡ Performance
- `refactor`: Code refactoring → 🚜 Refactor
- `style`: Code style changes → 🎨 Styling
- `test`: Tests → 🧪 Testing
- `chore`: Maintenance → ⚙️ Miscellaneous Tasks
- `ci`: CI/CD changes → ⚙️ Miscellaneous Tasks

### Examples

```bash
# Feature
git commit -m "feat(api): add user authentication endpoint"

# Bug fix
git commit -m "fix(parser): handle null values correctly"

# Breaking change
git commit -m "feat(api)!: remove deprecated endpoints

BREAKING CHANGE: The /v1/users endpoint has been removed.
Use /v2/users instead."

# With scope
git commit -m "docs(readme): update installation instructions"

# Simple
git commit -m "chore: update dependencies"
```

## Manual Changelog Generation

Generate changelog at any time:

```bash
# Trigger workflow manually
gh workflow run changelog.yml

# Or generate locally (requires git-cliff)
git cliff --latest
```

## Versioning Strategy

This project follows [Semantic Versioning](https://semver.org/):

- **Major (x.0.0)**: Breaking changes
- **Minor (1.x.0)**: New features (backwards compatible)
- **Patch (1.0.x)**: Bug fixes (backwards compatible)

## Tips

### Good Commit Messages
```bash
✅ feat: add dark mode support
✅ fix(ui): resolve button alignment issue
✅ docs: update API documentation
```

### Bad Commit Messages
```bash
❌ updated stuff
❌ fix
❌ WIP
```

### Breaking Changes
```bash
# Method 1: ! suffix
git commit -m "feat!: redesign API endpoints"

# Method 2: Footer
git commit -m "feat: redesign API

BREAKING CHANGE: All endpoints now require authentication"
```

## Example Release Flow

```bash
# 1. Make changes with conventional commits
git commit -m "feat: add new widget component"
git commit -m "fix: resolve memory leak"
git push origin main

# 2. Check draft release (auto-updated)
# Visit: https://github.com/YOUR_ORG/YOUR_REPO/releases

# 3. When ready to release, publish the draft
# → Triggers changelog generation automatically

# 4. CHANGELOG.md is updated and committed
# 5. Release is live!
```

## Configuration Files

- `.github/release-drafter.yml` - Release Drafter config
- `cliff.toml` - git-cliff config
- `.github/workflows/release-drafter.yml` - Auto-draft workflow
- `.github/workflows/changelog.yml` - Changelog generation workflow

## Troubleshooting

### Draft release not updating
- Check workflow runs: https://github.com/YOUR_ORG/YOUR_REPO/actions
- Ensure `GITHUB_TOKEN` has permissions

### Changelog not generated
- Verify `cliff.toml` syntax
- Check workflow logs
- Ensure conventional commits are being used

### Wrong version suggested
- Add labels to PRs: `major`, `minor`, or `patch`
- Edit version manually in draft release

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [git-cliff](https://git-cliff.org/)
- [Release Drafter](https://github.com/release-drafter/release-drafter)
