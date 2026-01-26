# GitHub Actions CI/CD

This project uses GitHub Actions for continuous integration and deployment.

## Workflows

### 1. Build & Test (`build.yml`)

**Triggers:**
- Pull requests to `main` or `develop`
- Push to `main` or `develop`
- Manual trigger

**What it does:**
- ✅ Builds on Ubuntu, macOS, and Windows
- ✅ Runs all tests (JVM, Android, iOS, Linux)
- ✅ Runs Detekt code quality checks
- ✅ Generates Dokka documentation
- ✅ Uploads build artifacts and test results

**Jobs:**
- `build` - Builds and tests on Ubuntu and macOS
- `test-linux` - Runs Linux native tests
- `test-ios` - Runs iOS simulator tests (macOS only)
- `build-windows` - Validates Windows build
- `code-quality` - Runs Detekt and uploads reports

### 2. Publish to Maven Central (`publish.yml`)

**Triggers:**
- GitHub release is published
- Manual trigger with version input

**What it does:**
- ✅ Publishes all libraries to Maven Central (Sonatype)
- ✅ Signs artifacts with GPG
- ✅ Creates GitHub release assets
- ✅ Attaches JARs and AARs to GitHub release

**Requirements:**
- GPG signing key
- Maven Central (Sonatype) credentials

### 3. Deploy Documentation (`docs.yml`)

**Triggers:**
- Push to `main`
- GitHub release is published
- Manual trigger

**What it does:**
- ✅ Generates Dokka API documentation
- ✅ Builds MkDocs site with API docs
- ✅ Deploys to GitHub Pages

## Setup Instructions

### Step 1: Enable GitHub Actions

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Under "Actions permissions", select **Allow all actions and reusable workflows**
4. Click **Save**

### Step 2: Configure GitHub Pages

1. Go to **Settings** → **Pages**
2. Under "Source", select **GitHub Actions**
3. Click **Save**

Your documentation will be available at: `https://your-username.github.io/your-repo-name/`

### Step 3: Set Up Maven Central Publishing

#### 3.1: Create Sonatype Account

1. Go to [Sonatype OSSRH](https://issues.sonatype.org/)
2. Create an account
3. Create a ticket to claim your group ID (e.g., `com.compiledplatforms`)
4. Wait for approval (usually 1-2 days)

#### 3.2: Generate GPG Signing Key

```bash
# Generate a new GPG key
gpg --gen-key

# Follow the prompts:
# - Real name: Your Name
# - Email: your.email@example.com
# - Password: Create a strong password

# List your keys and note the key ID
gpg --list-keys

# Export the private key (replace KEY_ID with your actual key ID)
gpg --armor --export-secret-keys KEY_ID | base64 > signing-key.txt
```

#### 3.3: Add GitHub Secrets

Go to **Settings** → **Secrets and variables** → **Actions** and add:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `MAVEN_CENTRAL_USERNAME` | Sonatype username | Your Sonatype JIRA username |
| `MAVEN_CENTRAL_PASSWORD` | Sonatype password | Your Sonatype JIRA password |
| `SIGNING_KEY` | GPG private key (base64) | Contents of `signing-key.txt` from step 3.2 |
| `SIGNING_PASSWORD` | GPG key password | Password you set when generating the GPG key |

**Important:** Never commit these secrets to your repository!

### Step 4: Update Publishing Configuration

Update `libraries/example-library/build.gradle.kts` with your information:

```kotlin
mavenPublishing {
    pom {
        name = "Your Library Name"
        description = "Your library description"
        inceptionYear = "2026"
        url = "https://github.com/your-username/your-repo/"
        
        licenses {
            license {
                name = "The Apache Software License, Version 2.0"
                url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
            }
        }
        
        developers {
            developer {
                id = "your-id"
                name = "Your Name"
                url = "https://github.com/your-username"
            }
        }
        
        scm {
            url = "https://github.com/your-username/your-repo/"
            connection = "scm:git:git://github.com/your-username/your-repo.git"
            developerConnection = "scm:git:ssh://git@github.com/your-username/your-repo.git"
        }
    }
}
```

## Usage

### Running Workflows Manually

#### Build & Test
1. Go to **Actions** → **Build & Test**
2. Click **Run workflow**
3. Select branch
4. Click **Run workflow**

#### Publish to Maven Central
1. Go to **Actions** → **Publish to Maven Central**
2. Click **Run workflow**
3. Enter version (e.g., `1.0.0`)
4. Click **Run workflow**

#### Deploy Documentation
1. Go to **Actions** → **Deploy Documentation**
2. Click **Run workflow**
3. Select branch
4. Click **Run workflow**

### Creating a Release

1. Ensure all changes are merged to `main`
2. Update version in `gradle.properties`:
   ```properties
   VERSION_NAME=1.0.0
   ```
3. Commit and push:
   ```bash
   git add gradle.properties
   git commit -m "chore: bump version to 1.0.0"
   git push origin main
   ```
4. Create and push a tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
5. Go to GitHub **Releases** → **Create a new release**
6. Select the tag you just created (`v1.0.0`)
7. Generate release notes or write your own
8. Click **Publish release**

This will automatically:
- ✅ Build and test the project
- ✅ Publish to Maven Central
- ✅ Deploy documentation to GitHub Pages
- ✅ Attach build artifacts to the GitHub release

### Monitoring Workflows

1. Go to the **Actions** tab in your repository
2. Click on a specific workflow run to see details
3. Click on individual jobs to see logs
4. Download artifacts from the workflow summary page

## Troubleshooting

### Build Failures

**Problem:** Tests fail on CI but pass locally

**Solutions:**
- Check if you're using absolute paths (use project-relative paths)
- Ensure timezone-independent code
- Check for race conditions in tests

### Publishing Failures

**Problem:** `401 Unauthorized` when publishing

**Solutions:**
- Verify `MAVEN_CENTRAL_USERNAME` and `MAVEN_CENTRAL_PASSWORD` secrets
- Check that your Sonatype account is active
- Verify you have rights to publish to your group ID

**Problem:** `Invalid signature` error

**Solutions:**
- Verify `SIGNING_KEY` is base64 encoded correctly
- Check `SIGNING_PASSWORD` matches your GPG key password
- Try regenerating and re-adding the GPG key

### Documentation Deployment Failures

**Problem:** GitHub Pages shows 404

**Solutions:**
- Ensure GitHub Pages is enabled and set to "GitHub Actions" source
- Check the workflow ran successfully
- Verify the `docs/site` directory was created during the build
- Wait a few minutes for GitHub Pages to update

**Problem:** Dokka documentation missing

**Solutions:**
- Check that Dokka task ran successfully in the workflow logs
- Verify the copy command correctly moved docs to MkDocs site
- Ensure library paths are correct in the workflow

## Best Practices

### 1. Always Test Before Releasing

Run a full build locally before creating a release:

```bash
./gradlew clean build detekt dokkaGeneratePublicationHtml
```

### 2. Use Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes

### 3. Write Good Release Notes

Include:
- New features added
- Bug fixes
- Breaking changes (if any)
- Migration guide (for major versions)
- Contributors

### 4. Keep Secrets Secure

- Never commit secrets to the repository
- Rotate secrets periodically
- Use GitHub's secret scanning
- Limit access to repository secrets

### 5. Monitor Workflow Status

- Add a build status badge to README.md:
  ```markdown
  [![Build](https://github.com/your-username/your-repo/actions/workflows/build.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/build.yml)
  ```

### 6. Keep Dependencies Updated

- Regularly update GitHub Actions versions
- Keep Gradle and plugin versions current
- Review Dependabot/Renovate PRs promptly

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Publishing to Maven Central](https://central.sonatype.org/publish/publish-guide/)
- [Gradle Maven Publish Plugin](https://vanniktech.github.io/gradle-maven-publish-plugin/)
- [GitHub Pages](https://docs.github.com/en/pages)
- [Semantic Versioning](https://semver.org/)
