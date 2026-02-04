---
name: make-commit
description: Create a well-formatted conventional commit with proper message structure
---

# Make Commit Skill

## Purpose

Guide the user through creating a proper [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) formatted commit message that follows project standards and automatically determines semantic versioning impact.

## When to Use

Use this skill when the user asks to:
- "create a commit"
- "commit changes"
- "make a commit"
- "commit this"
- Help with commit messages

## Process

### 1. Review Current State

Check what changes are being committed:

```bash
# Check status
git status --short

# View staged changes
git diff --staged --stat

# View unstaged changes
git diff --stat
```

### 2. Analyze Recent Commits

Review recent commit messages to maintain consistency:

```bash
git log --oneline -10
```

### 3. Determine Commit Type

Based on the changes, determine the appropriate type.

**Note:** The project's `.commitlintrc.json` defines the allowed types and rules. Check it for the authoritative list.

**Common Types:**
- `feat:` - New feature (triggers MINOR version bump)
- `fix:` - Bug fix (triggers PATCH version bump)
- `docs:` - Documentation only changes
- `style:` - Code style/formatting (no code change)
- `refactor:` - Code refactoring (no behavior change)
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `build:` - Build system or dependencies
- `ci:` - CI/CD configuration changes
- `chore:` - Maintenance tasks
- `revert:` - Reverting previous commits

**Breaking Changes:**
- Add `!` after type: `feat!:` or `fix!:`
- Or use footer: `BREAKING CHANGE: description`
- Triggers MAJOR version bump

### 4. Draft Commit Message

Format: `type(scope): subject`

**Structure:**
```
type(optional-scope): short description (max 100 chars)

[optional body - explain WHY, not what]
- Provide context and reasoning
- Can be multiple paragraphs

[optional footer(s)]
BREAKING CHANGE: describe the breaking change
Refs: #issue-number
Reviewed-by: name
```

**Guidelines:**
- **Subject line:**
  - Start with lowercase
  - No period at the end
  - Imperative mood ("add" not "adds" or "added")
  - Max 100 characters
  - Focus on WHAT changed

- **Body (optional but recommended):**
  - Explain WHY the change was made
  - Provide context for future readers
  - Separated from subject by blank line

- **Footer (optional):**
  - `BREAKING CHANGE:` for breaking changes
  - `Refs:` for issue references
  - `Reviewed-by:` for reviewers

### 5. Examples by Scenario

**New Feature:**
```
feat(auth): add OAuth2 social login support

Implement Google and GitHub OAuth2 providers to allow users to sign in
using their social accounts. This reduces friction in the signup flow
and improves conversion rates.

Refs: #234
```

**Bug Fix:**
```
fix(parser): prevent crash on malformed input

Add validation to reject null values before processing. Previously,
null values would cause NPE during parsing.

Fixes: #456
```

**Breaking Change (with !):**
```
feat(api)!: change response format to include metadata

The API now returns an object with `data` and `meta` fields instead of
returning the data directly. This enables pagination and versioning.

BREAKING CHANGE: All API responses now wrapped in {data, meta} object.
Clients must update to access response.data instead of response directly.
```

**Documentation:**
```
docs: update installation guide for Windows users

Add troubleshooting section for common PATH issues on Windows.
Include screenshots of environment variable configuration.
```

**Refactoring:**
```
refactor(core): extract validation logic into separate module

Move validation functions from UserService to new ValidationService.
No behavior changes, improves testability and separation of concerns.
```

**Multiple Changes (scope-specific):**
```
feat(ui): add dark mode toggle
feat(api): implement rate limiting
fix(auth): resolve session timeout issue
```
*Note: These should be separate commits, not combined*

### 6. Stage and Commit

**If changes aren't staged:**
```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Or stage all
git add .
```

**Create commit:**
```bash
git commit -m "type(scope): subject" -m "

Body paragraph explaining the change.
More context if needed.

Refs: #123"
```

Or use heredoc for complex messages:
```bash
git commit -m "$(cat <<'EOF'
type(scope): subject

Body paragraph with detailed explanation.

BREAKING CHANGE: describe what breaks and how to migrate
Refs: #123
EOF
)"
```

### 7. Verify Commit

```bash
# Check the commit was created correctly
git log -1 --format=fuller

# If incorrect, amend
git commit --amend
```

## Common Patterns

### Multi-file Feature
```
feat(checkout): implement multi-step checkout flow

Add wizard-style checkout with validation at each step:
- Step 1: Shipping address
- Step 2: Payment method
- Step 3: Order review

Refs: #789
```

### Security Fix
```
fix(auth): patch XSS vulnerability in user profile

Sanitize user input before rendering profile bio. Prevents script
injection through profile fields.

Security: CVE-2024-12345
```

### Performance Improvement
```
perf(db): optimize user query with composite index

Add composite index on (org_id, created_at) to speed up dashboard
queries. Reduces query time from 2.3s to 45ms in production.
```

### Dependency Update
```
build(deps): upgrade React from 18.2.0 to 18.3.0

Update to latest stable version for security patches and bug fixes.
No breaking changes in this update.
```

## Validation Checklist

Before committing, verify:
- ✅ Type is one of the allowed types (see `.commitlintrc.json`)
- ✅ Subject line follows length limits (commitlint will validate)
- ✅ Subject uses imperative mood
- ✅ Body explains WHY (if needed)
- ✅ Breaking changes are marked with `!` or `BREAKING CHANGE:`
- ✅ Only related changes in this commit
- ✅ Build passes and tests pass

**Note:** Commitlint will automatically validate format rules. Focus on content quality.

## Semantic Versioning Impact

Commits automatically determine version bumps:
- `fix:` → PATCH (1.0.0 → 1.0.1)
- `feat:` → MINOR (1.0.0 → 1.1.0)
- `BREAKING CHANGE:` or `!` → MAJOR (1.0.0 → 2.0.0)

## Tips

1. **Keep commits atomic** - One logical change per commit
2. **Commit often** - Small, frequent commits are better than large ones
3. **Write for future you** - Explain context that won't be obvious in 6 months
4. **Test before committing** - Ensure the code works
5. **Don't commit WIP** - Use stash or branches for work-in-progress
6. **Use scope consistently** - Check recent commits for scope naming patterns

## References

- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) - Specification
- [Semantic Versioning](https://semver.org/) - Version numbering
- `.commitlintrc.json` - Project's commit validation rules (source of truth)
- `.github/workflows/validate-commits.yml` - Automated validation
