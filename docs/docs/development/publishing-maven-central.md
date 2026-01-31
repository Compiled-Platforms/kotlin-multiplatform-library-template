# Publishing to Maven Central

Maven Central is the industry-standard repository for open-source Java and Kotlin libraries. It's free, widely used, and provides excellent discoverability.

## Prerequisites

Before publishing to Maven Central, you need:

1. **Sonatype Account** - For publishing access
2. **GPG Key** - For signing artifacts
3. **Verified Group ID** - Claim your namespace
4. **GitHub Secrets** - Store credentials securely

## Step 1: Create Sonatype Account

### Register Account

1. Go to [https://central.sonatype.com/](https://central.sonatype.com/)
2. Click **Sign Up** in the top right
3. Create an account with your email

### Claim Your Group ID

1. Log in to [https://central.sonatype.com/](https://central.sonatype.com/)
2. Navigate to **Namespaces**
3. Click **Add Namespace**

#### Option A: GitHub-based Group ID (Easiest)

```
Group ID: io.github.yourusername
```

Verification: Add TXT record to your GitHub profile or verify via repository

#### Option B: Domain-based Group ID

```
Group ID: com.yourcompany
```

Verification: Add TXT record to your domain's DNS

**Example:**
```
io.github.janesmith → For GitHub user janesmith
com.mycompany.kmp → For company owning mycompany.com
```

### Approval

Namespace verification is usually instant for GitHub-based IDs, 1-2 days for domain-based IDs.

## Step 2: Generate GPG Key

Maven Central requires all artifacts to be cryptographically signed.

### Generate Key

```bash
# Generate a new GPG key
gpg --full-generate-key

# Choose:
# Kind: (1) RSA and RSA
# Size: 4096 bits
# Expiration: 0 (does not expire) or your preference
# Real name: Your Name
# Email: your.email@example.com
# Password: [Create a strong password - save it!]
```

### Export Keys

```bash
# List your keys to get the key ID
gpg --list-secret-keys --keyid-format SHORT

# Output will look like:
# sec   rsa4096/ABCD1234 2026-01-28 [SC]
#       ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234
# uid   Your Name <your.email@example.com>

# Export the private key as base64 (use your key ID)
gpg --armor --export-secret-keys ABCD1234 | base64 > signing-key.txt

# This creates signing-key.txt with your base64-encoded key
```

### Publish Public Key

```bash
# Publish to key servers (use your key ID)
gpg --keyserver keyserver.ubuntu.com --send-keys ABCD1234
gpg --keyserver keys.openpgp.org --send-keys ABCD1234
```

## Step 3: Configure project.yml

Update your `project.yml` to enable Maven Central:

```yaml
publishing:
  enabled: true
  
  # Maven coordinates
  group_id: io.github.yourusername  # Must match claimed namespace
  artifact_id_prefix: kmp
  
  repositories:
    maven_central:
      enabled: true
      auto_release: false  # Set to true for automatic release from staging
    
    # Disable other repositories (or keep them enabled for multi-repo)
    github_packages:
      enabled: false
    custom_maven:
      enabled: false
  
  signing:
    required: true
    key_from_secret: true
```

## Step 4: Add GitHub Secrets

Add these secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** for each:

| Secret Name | Value | Where to find it |
|-------------|-------|------------------|
| `MAVEN_CENTRAL_USERNAME` | Your Sonatype account username | From Step 1 |
| `MAVEN_CENTRAL_PASSWORD` | Your Sonatype account password | From Step 1 |
| `SIGNING_KEY` | Content of `signing-key.txt` | From Step 2 |
| `SIGNING_PASSWORD` | Your GPG key password | From Step 2 |

**Important**: For `SIGNING_KEY`, copy the **entire contents** of `signing-key.txt`, including the `-----BEGIN PGP PRIVATE KEY BLOCK-----` and `-----END PGP PRIVATE KEY BLOCK-----` sections after base64 encoding.

## Step 5: Test Locally

Before publishing to Maven Central, test locally:

```bash
# 1. Build everything
./gradlew clean build

# 2. Publish to local Maven repository
./gradlew publishToMavenLocal

# 3. Check artifacts in ~/.m2/repository
ls -la ~/.m2/repository/io/github/yourusername/
```

You should see:
- `.jar` files (library artifacts)
- `.pom` files (Maven metadata)
- `.module` files (Gradle metadata)
- `.asc` files (signatures)

## Step 6: Publish Release

### Update Version

```properties
# gradle.properties
VERSION_NAME=1.0.0
```

### Create Release

```bash
# Commit version bump
git add gradle.properties
git commit -m "chore: prepare release 1.0.0"
git push origin main

# Create and push tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

### Trigger Publishing

Publishing happens automatically via GitHub Actions when you create a release:

1. Go to GitHub → **Releases** → **Draft a new release**
2. Choose tag: `v1.0.0`
3. Generate release notes or write custom notes
4. Click **Publish release**

The workflow will:
- ✅ Build all platforms
- ✅ Run tests
- ✅ Sign artifacts
- ✅ Publish to Maven Central Staging

## Step 7: Release from Staging

If `auto_release: false` (recommended), manually release from staging:

1. Go to [https://central.sonatype.com/](https://central.sonatype.com/)
2. Log in
3. Click **Deployments** in left sidebar
4. Find your deployment (search by group ID)
5. Click on the deployment
6. Click **Publish** button

Artifacts will be available on Maven Central within:
- **Search**: 10-15 minutes
- **Maven/Gradle**: 2-4 hours (CDN propagation)

### Auto-Release (Optional)

To skip manual staging release:

```yaml
# project.yml
publishing:
  repositories:
    maven_central:
      enabled: true
      auto_release: true  # ← Automatically release from staging
```

## Step 8: Verify Publication

Check your library is available:

```bash
# Search Maven Central
https://search.maven.org/search?q=g:io.github.yourusername

# Or use Maven Central API
curl "https://search.maven.org/solrsearch/select?q=g:io.github.yourusername+AND+a:your-library&rows=1"
```

## Using Published Library

Users can now depend on your library:

```kotlin
// build.gradle.kts
dependencies {
    implementation("io.github.yourusername:library-name:1.0.0")
}
```

## Troubleshooting

### 401 Unauthorized

**Problem**: Invalid Sonatype credentials

**Solution**:
- Verify `MAVEN_CENTRAL_USERNAME` and `MAVEN_CENTRAL_PASSWORD` are correct
- Log in to [https://central.sonatype.com/](https://central.sonatype.com/) to verify account
- Check if account has publishing permissions for your group ID

### Signature Verification Failed

**Problem**: GPG signing issues

**Solution**:
- Ensure `SIGNING_KEY` contains the complete base64-encoded key
- Verify `SIGNING_PASSWORD` is correct
- Re-export the key and update the secret
- Check public key is published to key servers

### Namespace Not Verified

**Problem**: Group ID not claimed

**Solution**:
- Log in to Sonatype and verify namespace ownership
- For GitHub-based IDs, add TXT record to GitHub profile
- For domain-based IDs, add TXT record to DNS
- Wait for verification (instant for GitHub, 1-2 days for domains)

### Upload Timeout

**Problem**: Network issues during upload

**Solution**:
- Try publishing again (idempotent operation)
- Check Sonatype status page
- Ensure artifacts aren't too large (split into smaller modules if needed)

### Validation Errors

**Problem**: POM validation failed

**Solution**:
- Ensure all required POM fields are filled in library's `build.gradle.kts`
- Required: name, description, url, licenses, developers, scm
- Check `mavenPublishing` block in library's build file

## Best Practices

### Version Management

- ✅ Use semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Don't publish SNAPSHOT versions to Maven Central
- ✅ Create Git tags for all releases
- ✅ Keep CHANGELOG.md updated

### Release Process

- ✅ Test thoroughly before releasing
- ✅ Run API validation: `./gradlew apiCheck`
- ✅ Update documentation
- ✅ Write clear release notes
- ✅ Let CI/CD handle publishing (don't publish from local machine)

### Security

- ✅ Rotate GPG keys periodically
- ✅ Use strong GPG password
- ✅ Never commit signing keys to version control
- ✅ Backup your GPG keys securely

### Group ID Selection

- ✅ Use `io.github.username` for personal projects
- ✅ Use `com.yourcompany` if you own the domain
- ✅ Keep it consistent across all your libraries
- ✅ Once published, you cannot change the group ID

## Next Steps

- [Publishing to GitHub Packages](publishing-github-packages.md) - Add private snapshots
- [Publishing Overview](publishing.md) - Multi-repository strategy
- [Versioning](versioning.md) - Version management guide
