# Publishing to GitHub Packages

GitHub Packages is a package hosting service integrated with GitHub. It's perfect for private team libraries and offers free unlimited storage for private repositories.

## When to Use GitHub Packages

✅ **Good for:**
- Private libraries for your organization
- Internal team dependencies
- Development snapshots
- Pre-release testing
- Free private hosting

❌ **Not ideal for:**
- Public open-source libraries (use Maven Central instead)
- Libraries consumed outside your GitHub organization
- Cross-platform public distribution

## Step 1: Configure project.yml

Update your `project.yml` to enable GitHub Packages:

```yaml
publishing:
  enabled: true
  
  # Maven coordinates
  group_id: com.yourcompany.kmp
  artifact_id_prefix: kmp
  
  repositories:
    github_packages:
      enabled: true
      owner: your-org-name          # GitHub organization or username
      repository: your-repo-name     # Repository name (can be different from code repo)
    
    # Optional: Also publish to Maven Central
    maven_central:
      enabled: false
  
  signing:
    required: true    # Still recommended even for private packages
    key_from_secret: true
```

### Configuration Options

| Field | Description | Example |
|-------|-------------|---------|
| `owner` | GitHub organization or username | `mycompany`, `janesmith` |
| `repository` | Repository name for packages | `maven-packages`, `kotlin-libraries` |

**Note**: The `repository` can be:
- Same as your code repository
- Dedicated package repository (e.g., `maven-packages`)
- Any repository in your organization

## Step 2: Repository Strategy

You have two options for hosting packages:

### Option A: Same Repository (Simple)

Publish packages to the same repository as your code:

```yaml
# project.yml
publishing:
  repositories:
    github_packages:
      enabled: true
      owner: mycompany
      repository: kotlin-multiplatform-library  # Same as code repo
```

**Pros:**
- ✅ Simple setup
- ✅ Packages and code in one place
- ✅ Automatic access control

**Cons:**
- ❌ Clutters release page
- ❌ Less flexible permissions

### Option B: Dedicated Package Repository (Recommended)

Create a separate repository just for Maven packages:

```yaml
# project.yml
publishing:
  repositories:
    github_packages:
      enabled: true
      owner: mycompany
      repository: maven-packages  # Dedicated package repo
```

**Setup:**
1. Create new repository: `mycompany/maven-packages`
2. Set to private (if needed)
3. Configure team access

**Pros:**
- ✅ Clean separation
- ✅ Flexible permissions
- ✅ Can host packages from multiple projects

## Step 3: Authentication Setup

GitHub Packages uses GitHub tokens for authentication.

### For CI/CD (Automatic)

GitHub Actions automatically provides a token:

```yaml
# .github/workflows/publish.yml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Auto-provided
```

No additional configuration needed! The workflow already includes this.

### For Local Publishing (Manual)

Create a Personal Access Token:

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a name: "Maven Package Publishing"
4. Select scopes:
   - `write:packages` (upload packages)
   - `read:packages` (download packages)
   - `delete:packages` (optional, for cleanup)
5. Click **Generate token**
6. Copy the token (you won't see it again!)

Add to `~/.gradle/gradle.properties`:

```properties
# ~/.gradle/gradle.properties
gpr.user=your-github-username
gpr.token=ghp_your_personal_access_token
```

## Step 4: Publish

### Via CI/CD (Recommended)

Create a release to trigger publishing:

```bash
# Tag and push
git tag v1.0.0
git push origin v1.0.0

# Or create release via GitHub UI
```

The workflow automatically publishes to GitHub Packages.

### Manually (Local)

```bash
# Build and publish
./gradlew publish
```

## Step 5: Verify Publication

Check packages were published:

1. Go to your repository on GitHub
2. Click **Packages** in the right sidebar (or organization packages page)
3. Find your library

URL format:
```
https://github.com/orgs/YOUR_ORG/packages/container/package/YOUR_PACKAGE
```

## Using Published Packages

### In Another Project

Add GitHub Packages repository and authenticate:

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            name = "GitHubPackages"
            url = uri("https://maven.pkg.github.com/OWNER/REPOSITORY")
            credentials {
                username = project.findProperty("gpr.user") as String? ?: System.getenv("GITHUB_ACTOR")
                password = project.findProperty("gpr.token") as String? ?: System.getenv("GITHUB_TOKEN")
            }
        }
    }
}
```

Then depend on your library:

```kotlin
// build.gradle.kts
dependencies {
    implementation("com.yourcompany.kmp:library-name:1.0.0")
}
```

### Authentication for Consumers

Users need authentication to download packages:

#### Option 1: Personal Access Token (Local Development)

Add to `~/.gradle/gradle.properties`:

```properties
gpr.user=their-github-username
gpr.token=their_personal_access_token
```

#### Option 2: GITHUB_TOKEN (CI/CD)

In GitHub Actions workflows:

```yaml
# .github/workflows/build.yml
steps:
  - name: Build
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: ./gradlew build
```

## Multiple Organizations

Publishing to multiple organizations:

```yaml
# project.yml
publishing:
  repositories:
    github_packages:
      enabled: true
      owner: company-a
      repository: maven-packages
```

For additional organizations, create separate publishing workflows or use multiple repositories in your convention plugin.

## Snapshot vs Release Versions

### Snapshots

Great for continuous integration:

```properties
# gradle.properties
VERSION_NAME=1.0.0-SNAPSHOT
```

Snapshots are always overwritable and perfect for development branches.

### Releases

Use semantic versions for stable releases:

```properties
# gradle.properties
VERSION_NAME=1.0.0
```

Once published, releases should not be overwritten.

## Troubleshooting

### 401 Unauthorized

**Problem**: Authentication failed

**Solution**:
- Verify `GITHUB_TOKEN` or Personal Access Token is valid
- Check token has `write:packages` permission
- Ensure user has write access to the repository
- For organization repos, check org permissions allow package publishing

### 404 Not Found

**Problem**: Repository not found

**Solution**:
- Verify `owner` and `repository` names in `project.yml` are correct
- Check repository exists and you have access
- Ensure repository is not disabled or archived

### Package Version Already Exists

**Problem**: Trying to republish the same version

**Solution**:
- Don't republish release versions (immutable)
- Use SNAPSHOT versions for development
- Increment version number for new releases
- Delete old version if you really need to replace it (requires `delete:packages` permission)

### Access Denied for Consumers

**Problem**: Users can't download packages

**Solution**:
- Ensure users have read access to the repository
- Users need valid GitHub token with `read:packages`
- For public packages, repository must be public
- Check organization SSO requirements

## Best Practices

### Organization Setup

- ✅ Create dedicated `maven-packages` repository
- ✅ Set up team-based access control
- ✅ Use organization secrets for shared credentials
- ✅ Document authentication setup for team members

### Version Management

- ✅ Use `-SNAPSHOT` for development versions
- ✅ Use semantic versioning for releases
- ✅ Tag all release versions in Git
- ✅ Automate version bumping

### Security

- ✅ Use fine-grained Personal Access Tokens
- ✅ Rotate tokens regularly
- ✅ Use organization secrets for CI/CD
- ✅ Review package access permissions periodically

### CI/CD Integration

- ✅ Publish snapshots on every main branch commit
- ✅ Publish releases only on tagged versions
- ✅ Use GitHub Actions built-in `GITHUB_TOKEN`
- ✅ Don't publish from local machines

## Combined Strategy: GitHub Packages + Maven Central

Publish to both for maximum flexibility:

```yaml
# project.yml
publishing:
  repositories:
    maven_central:
      enabled: true
      auto_release: false  # Manual review for public releases
    
    github_packages:
      enabled: true
      owner: yourcompany
      repository: maven-packages
  
  strategy:
    snapshots_on_main: true   # Auto-publish snapshots to GitHub Packages
    releases_on_tag: true     # Publish releases to both
```

**Benefits:**
- ✅ Development snapshots → GitHub Packages (private, fast)
- ✅ Stable releases → Maven Central (public, discoverable)
- ✅ Internal team uses GitHub Packages
- ✅ External users use Maven Central

## Package Retention

GitHub Packages has retention policies:

- **Public packages**: Free, unlimited storage
- **Private packages**: Free, unlimited storage for private repos
- **Organization**: Configure retention in organization settings

To clean up old versions:

```bash
# Using GitHub CLI
gh api -X DELETE /user/packages/maven/com.yourcompany.library-name/versions/VERSION_ID
```

## Next Steps

- [Publishing to Maven Central](publishing-maven-central.md) - Add public distribution
- [Custom Maven Repository](publishing-custom-maven.md) - Self-hosted alternative
- [Publishing Overview](publishing.md) - Multi-repository strategy
