# GitHub Actions Setup Guide

This guide will help you set up GitHub Actions for your Kotlin Multiplatform library template.

## Quick Start Checklist

- [ ] Enable GitHub Actions in repository settings
- [ ] Configure GitHub Pages for documentation
- [ ] Create Sonatype OSSRH account (for Maven Central)
- [ ] Generate GPG signing key
- [ ] Add required secrets to GitHub
- [ ] Update publishing configuration with your details
- [ ] Test workflows manually
- [ ] Create your first release

## Detailed Setup Steps

### 1. Enable GitHub Actions

✅ **This is usually already enabled by default**

If not:
1. Go to your repository → **Settings** → **Actions** → **General**
2. Select **Allow all actions and reusable workflows**
3. Click **Save**

### 2. Configure GitHub Pages

1. Go to **Settings** → **Pages**
2. Under "Build and deployment" → "Source", select **GitHub Actions**
3. Your docs will be at: `https://your-username.github.io/your-repo-name/`

### 3. Set Up Maven Central Publishing

#### Step 3a: Create Sonatype Account

1. Go to https://issues.sonatype.org/
2. Click **Sign up** and create an account
3. Create a new issue to claim your group ID:
   - **Project**: Community Support - Open Source Project Repository Hosting (OSSRH)
   - **Issue Type**: New Project
   - **Summary**: `Request for com.yourcompany`
   - **Group Id**: `com.yourcompany` (use your actual domain/GitHub org)
   - **Project URL**: Your GitHub repository URL
   - **SCM URL**: Your GitHub repository `.git` URL
4. Wait for approval (usually 1-2 business days)

#### Step 3b: Generate GPG Key

Run these commands in your terminal:

```bash
# 1. Generate a new GPG key
gpg --full-generate-key

# Choose:
# - Kind: (1) RSA and RSA
# - Size: 4096
# - Expiration: 0 (does not expire) or your preference
# - Real name: Your Name
# - Email: your.email@example.com
# - Password: [Create a strong password - save this!]

# 2. List your keys
gpg --list-keys

# Output will look like:
# pub   rsa4096 2026-01-20 [SC]
#       ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234
# uid   Your Name <your.email@example.com>

# 3. Export the private key (replace the KEY_ID with your actual key ID from above)
gpg --armor --export-secret-keys ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234 | base64

# This will output a long base64 string - copy it (you'll need it for GitHub secrets)

# 4. Publish your public key to a key server
gpg --keyserver keyserver.ubuntu.com --send-keys ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234
```

#### Step 3c: Add GitHub Secrets

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add each of these:

| Secret Name | Value |
|-------------|-------|
| `MAVEN_CENTRAL_USERNAME` | Your Sonatype JIRA username |
| `MAVEN_CENTRAL_PASSWORD` | Your Sonatype JIRA password |
| `SIGNING_KEY` | The base64 string from step 3b (the entire output) |
| `SIGNING_PASSWORD` | The password you created for your GPG key |

**Screenshot Example:**

![GitHub Secrets](../images/github_secrets.png)

### 4. Update Your Library Configuration

Update the publishing configuration in your library's `build.gradle.kts`:

```kotlin
mavenPublishing {
    pom {
        name = "Your Library Name"
        description = "A great Kotlin Multiplatform library"
        inceptionYear = "2026"
        url = "https://github.com/YOUR_USERNAME/YOUR_REPO/"
        
        licenses {
            license {
                name = "The Apache Software License, Version 2.0"
                url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
            }
        }
        
        developers {
            developer {
                id = "YOUR_GITHUB_USERNAME"
                name = "Your Name"
                url = "https://github.com/YOUR_GITHUB_USERNAME"
            }
        }
        
        scm {
            url = "https://github.com/YOUR_USERNAME/YOUR_REPO/"
            connection = "scm:git:git://github.com/YOUR_USERNAME/YOUR_REPO.git"
            developerConnection = "scm:git:ssh://git@github.com/YOUR_USERNAME/YOUR_REPO.git"
        }
    }
}
```

Also update `gradle.properties`:

```properties
GROUP=com.yourcompany.kmp.library
VERSION_NAME=1.0.0
```

### 5. Test Your Setup

#### Test Build Workflow

1. Make a change to any file
2. Commit and push to a branch
3. Create a pull request to `develop` or `main`
4. Check the **Actions** tab - the build workflow should run automatically

#### Test Documentation Deployment

1. Go to **Actions** → **Deploy Documentation**
2. Click **Run workflow** → **Run workflow**
3. Wait for completion
4. Visit `https://your-username.github.io/your-repo-name/`

#### Test Publishing (Dry Run)

Before creating a real release, test locally:

```bash
# This simulates what the publish workflow will do
./gradlew publishToMavenLocal --no-daemon

# Check ~/.m2/repository/com/yourcompany/kmp/library/
# You should see your library artifacts there
```

### 6. Create Your First Release

Once everything is set up:

1. Update version in `gradle.properties`:
   ```properties
   VERSION_NAME=1.0.0
   ```

2. Update `CHANGELOG.md` with release notes

3. Commit and push to `main`:
   ```bash
   git add gradle.properties CHANGELOG.md
   git commit -m "chore: prepare release 1.0.0"
   git push origin main
   ```

4. Create and push a tag:
   ```bash
   git tag -a v1.0.0 -m "Release 1.0.0"
   git push origin v1.0.0
   ```

5. Go to GitHub → **Releases** → **Draft a new release**
   - Choose tag: `v1.0.0`
   - Title: `v1.0.0`
   - Description: Copy from `CHANGELOG.md`
   - Click **Publish release**

6. Watch the magic happen in the **Actions** tab! 🎉

The publish workflow will:
- ✅ Build and test your library
- ✅ Sign artifacts with your GPG key
- ✅ Publish to Maven Central
- ✅ Attach JARs/AARs to the GitHub release

### 7. Verify Publication

After the workflow completes (15-30 minutes):

1. Go to https://s01.oss.sonatype.org/
2. Log in with your Sonatype credentials
3. Navigate to **Staging Repositories**
4. Find your repository (it will be closed automatically)
5. Click **Release** to publish to Maven Central
6. Within 2-4 hours, your library will be available on Maven Central

## Troubleshooting

### "401 Unauthorized" When Publishing

❌ **Problem:** Secrets are incorrect or expired

✅ **Solution:**
- Double-check `MAVEN_CENTRAL_USERNAME` and `MAVEN_CENTRAL_PASSWORD`
- Verify your Sonatype account is active
- Try logging in to https://s01.oss.sonatype.org/ to confirm credentials

### "Invalid Signature" Error

❌ **Problem:** GPG key issues

✅ **Solution:**
- Ensure `SIGNING_KEY` is the complete base64 output (including `-----BEGIN/END-----`)
- Verify `SIGNING_PASSWORD` is correct
- Try regenerating the GPG key and re-adding secrets

### GitHub Pages Shows 404

❌ **Problem:** Pages not configured or deployment failed

✅ **Solution:**
- Ensure Pages is enabled and set to "GitHub Actions" source
- Check the workflow logs in the **Actions** tab
- Wait 5-10 minutes after first deployment

### Workflows Not Running

❌ **Problem:** Actions not enabled or workflow syntax error

✅ **Solution:**
- Check Actions are enabled in Settings
- Validate YAML syntax (use an online YAML validator)
- Check branch protection rules aren't blocking Actions

## Next Steps

Once everything is working:

- ✅ Add build status badges to your README
- ✅ Set up Dependabot or Renovate for dependency updates
- ✅ Configure branch protection rules
- ✅ Add more comprehensive tests
- ✅ Set up code coverage reporting

## Need Help?

- Check the [GitHub Actions documentation](docs/docs/development/github-actions.md)
- Review workflow logs in the **Actions** tab
- Search existing GitHub issues
- Open a new issue with "CI/CD" label

---

**Congratulations!** You now have a fully automated CI/CD pipeline! 🚀
