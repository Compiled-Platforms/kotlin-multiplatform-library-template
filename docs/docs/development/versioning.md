# Versioning & Releases

This project uses **semantic-release** for fully automated versioning based on [Conventional Commits](https://www.conventionalcommits.org/).

## Overview

- **Automated**: Versions are calculated from commit messages
- **Semantic Versioning**: Follows [SemVer 2.0.0](https://semver.org/)
- **CI-Driven**: Releases happen automatically on merge to `main`

## How It Works

1. Write commits using conventional format
2. Merge PR to `main`
3. Tests run automatically
4. semantic-release analyzes commits
5. Version bumped, changelog generated, release created

## Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

### Commit Types

| Type | Description | Version Bump | Example |
|------|-------------|--------------|---------|
| `feat:` | New feature | **Minor** (1.2.0 → 1.3.0) | `feat: add authentication API` |
| `fix:` | Bug fix | **Patch** (1.2.0 → 1.2.1) | `fix: correct validation logic` |
| `feat!:` | Breaking change | **Major** (1.2.0 → 2.0.0) | `feat!: redesign API` |
| `fix!:` | Breaking fix | **Major** (1.2.0 → 2.0.0) | `fix!: remove deprecated method` |
| `chore:` | Maintenance | **None** | `chore: update dependencies` |
| `docs:` | Documentation | **None** | `docs: improve README` |
| `ci:` | CI/CD changes | **None** | `ci: fix workflow` |
| `test:` | Tests only | **None** | `test: add unit tests` |
| `refactor:` | Code refactoring | **None** | `refactor: simplify logic` |
| `style:` | Code formatting | **None** | `style: fix indentation` |
| `perf:` | Performance | **Patch** (1.2.0 → 1.2.1) | `perf: optimize algorithm` |

## When to Trigger a Release

### ✅ DO Release For:

- Bug fixes users would notice: `fix: correct API response format`
- New features users can use: `feat: add new API endpoint`
- Performance improvements: `perf: reduce memory usage by 50%`

### ❌ DON'T Release For:

- Internal tooling: `chore: update Gradle config`
- Documentation: `docs: fix typos in README`
- Internal refactoring: `refactor: reorganize internal classes`
- Test-only changes: `test: add integration tests`
- CI/CD config: `ci: optimize GitHub Actions`

## Breaking Changes

Mark breaking changes with `!` or `BREAKING CHANGE:`:

**Using `!` (simplest):**
```
git commit -m "feat!: redesign authentication API"
```

**Using footer:**
```
git commit -m "feat: redesign auth API

BREAKING CHANGE: The login() method signature changed"
```

Both formats trigger a **major** version bump (1.2.0 → 2.0.0)

## Enforcement

### Local Validation (Lefthook + commitlint)

Commits are validated locally via git hooks using [commitlint](https://github.com/conventional-changelog/commitlint):

```bash
lefthook install  # First time only
git commit -m "invalid message"  # ❌ Blocked!
git commit -m "feat: valid message"  # ✅ Allowed
```

Validation rules are defined in `.commitlintrc.json` at the project root.

### CI Validation (GitHub Actions)

All PR commits are validated in CI automatically via the "Validate Commit Messages" workflow.

## Further Reading

- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message specification
- [commitlint](https://github.com/conventional-changelog/commitlint) - Commit message linting tool
- [Semantic Versioning](https://semver.org/) - Version numbering scheme
- [semantic-release Documentation](https://semantic-release.gitbook.io/) - Automated release tool
