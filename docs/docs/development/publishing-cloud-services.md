# Publishing to Cloud Services

Cloud-hosted package repositories offer managed infrastructure without the operational overhead of self-hosting. This guide covers JFrog Artifactory Cloud and CloudSmith.

## Comparison

| Feature | JFrog Artifactory Cloud | CloudSmith |
|---------|------------------------|------------|
| **Type** | Universal repository manager | Modern package registry |
| **Maven Support** | ✅ Full | ✅ Full |
| **Other Formats** | Docker, npm, PyPI, NuGet, etc. | Docker, npm, PyPI, NuGet, etc. |
| **Free Tier** | Limited (2GB storage, 10GB transfer) | Yes (public packages) |
| **Pricing** | From $150/month | From $75/month |
| **Best For** | Enterprise, multiple formats | Startups, simpler workflows |

## JFrog Artifactory Cloud {#jfrog}

JFrog Artifactory Cloud is the managed version of the popular Artifactory repository manager.

### When to Use JFrog

✅ **Good for:**
- Enterprise teams needing multiple artifact types
- Teams already using JFrog products
- Advanced features (replication, caching, metadata)
- Compliance and audit requirements
- Integration with JFrog Platform (Xray, Pipelines, etc.)

### Step 1: Create JFrog Account

1. Go to [https://jfrog.com/start-free/](https://jfrog.com/start-free/)
2. Sign up for free trial or paid plan
3. Choose cloud provider and region
4. Wait for instance provisioning (~5-10 minutes)

Your instance URL: `https://yourcompany.jfrog.io`

### Step 2: Create Maven Repository

1. Log in to your JFrog instance
2. **Administration** → **Repositories** → **Add Repositories** → **Local Repository**
3. Select **Maven**
4. Repository Key: `maven-releases`
5. Click **Create**

Repeat for snapshots repository: `maven-snapshots`

### Step 3: Generate Access Token

1. Click your profile (top right) → **Edit Profile**
2. **Authentication Settings** → **Generate Token**
3. Scopes: Select repositories or use default
4. Expiration: Set appropriate duration
5. Click **Generate** and copy the token

### Step 4: Configure project.yml

```yaml
publishing:
  enabled: true
  
  # Maven coordinates
  group_id: com.yourcompany.kmp
  artifact_id_prefix: kmp
  
  repositories:
    jfrog:
      enabled: true
      url: https://yourcompany.jfrog.io/artifactory/maven-releases/
  
  signing:
    required: true
    key_from_secret: true
```

### Step 5: Add GitHub Secrets

Add credentials to GitHub:

| Secret Name | Value |
|-------------|-------|
| `JFROG_USERNAME` | Your JFrog username or email |
| `JFROG_PASSWORD` | Generated access token (or password) |
| `SIGNING_KEY` | Base64-encoded GPG key |
| `SIGNING_PASSWORD` | GPG key password |

**Tip**: Use access token instead of password for better security.

### Step 6: Publish

Publishing happens automatically via GitHub Actions:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Or manually:
```bash
./gradlew publish
```

### Using JFrog Packages

Configure consumers to use your JFrog repository:

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            url = uri("https://yourcompany.jfrog.io/artifactory/maven-releases/")
            credentials {
                username = project.findProperty("jfrog.username") as String?
                    ?: System.getenv("JFROG_USERNAME")
                password = project.findProperty("jfrog.password") as String?
                    ?: System.getenv("JFROG_PASSWORD")
            }
        }
    }
}
```

### JFrog Advanced Features

#### Virtual Repositories

Combine multiple repositories:

1. **Administration** → **Repositories** → **Add Repositories** → **Virtual Repository**
2. Type: Maven
3. Repository Key: `maven-virtual`
4. Include repositories: `maven-releases`, `maven-snapshots`, `maven-central-cache`

Consumers use single URL:
```kotlin
url = uri("https://yourcompany.jfrog.io/artifactory/maven-virtual/")
```

#### Remote Repositories (Proxy)

Cache external dependencies:

1. **Administration** → **Repositories** → **Add Repositories** → **Remote Repository**
2. Type: Maven
3. Repository Key: `maven-central-cache`
4. URL: `https://repo1.maven.org/maven2/`

Add to virtual repository for transparent caching.

#### Xray Integration (Security Scanning)

If you have JFrog Xray:

1. **Administration** → **Xray** → **Settings**
2. Enable Xray for repositories
3. Configure policies and watches
4. Automatic scanning of artifacts for vulnerabilities

#### Build Info

Track build metadata:

```bash
# In CI/CD
./gradlew artifactoryPublish \
  -Partifactory.publish.buildInfo=true
```

### JFrog Pricing

**Free Tier:**
- 2GB storage
- 10GB data transfer/month
- Basic features

**Pro Plans:**
- From $150/month
- More storage and transfer
- Advanced features

See [JFrog pricing](https://jfrog.com/pricing/) for details.

---

## CloudSmith {#cloudsmith}

CloudSmith is a modern cloud-native package repository with focus on developer experience.

### When to Use CloudSmith

✅ **Good for:**
- Startups and scale-ups
- Teams wanting simpler workflows
- Public package hosting
- Fast setup and deployment
- Modern UI and API

### Step 1: Create CloudSmith Account

1. Go to [https://cloudsmith.com/](https://cloudsmith.com/)
2. Sign up for free or paid plan
3. Create organization (or use personal namespace)

### Step 2: Create Repository

1. Click **Create** → **Create Repository**
2. Repository name: `maven`
3. Visibility: Private or Public
4. Repository type: Maven
5. Click **Create Repository**

Your repository URL:
```
https://maven.cloudsmith.io/yourcompany/maven/
```

### Step 3: Generate API Key

1. Click your profile → **Settings** → **API Keys**
2. Click **Create API Key**
3. Name: "Maven Publishing"
4. Scopes: `write:repos`
5. Click **Create** and copy the key

### Step 4: Configure project.yml

```yaml
publishing:
  enabled: true
  
  # Maven coordinates
  group_id: com.yourcompany.kmp
  artifact_id_prefix: kmp
  
  repositories:
    cloudsmith:
      enabled: true
      owner: yourcompany      # Organization or username
      repository: maven       # Repository name
  
  signing:
    required: true
    key_from_secret: true
```

### Step 5: Add GitHub Secrets

| Secret Name | Value |
|-------------|-------|
| `CLOUDSMITH_API_KEY` | Generated API key |
| `SIGNING_KEY` | Base64-encoded GPG key |
| `SIGNING_PASSWORD` | GPG key password |

### Step 6: Publish

Publishing happens automatically:

```bash
git tag v1.0.0
git push origin v1.0.0
```

### Using CloudSmith Packages

#### Public Repository (No Authentication)

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            url = uri("https://dl.cloudsmith.io/public/yourcompany/maven/maven/")
        }
    }
}
```

#### Private Repository (With Authentication)

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            url = uri("https://maven.cloudsmith.io/yourcompany/maven/")
            credentials {
                username = project.findProperty("cloudsmith.username") as String?
                    ?: System.getenv("CLOUDSMITH_USERNAME")
                    ?: "token"  # Use "token" as username for API key
                password = project.findProperty("cloudsmith.apiKey") as String?
                    ?: System.getenv("CLOUDSMITH_API_KEY")
            }
        }
    }
}
```

### CloudSmith Features

#### Entitlements (Access Control)

Create tokens for fine-grained access:

1. **Repository** → **Settings** → **Entitlements**
2. Click **Create Entitlement Token**
3. Name: "Developer Access"
4. Permissions: Download only
5. Copy token

Users use entitlement token as password for read access.

#### Webhooks

Trigger actions on package upload:

1. **Repository** → **Settings** → **Webhooks**
2. Add webhook URL
3. Select events (package uploaded, etc.)
4. Use for notifications, CI triggers, etc.

#### Package Retention Policies

Auto-delete old packages:

1. **Repository** → **Settings** → **Retention**
2. Configure rules:
   - Keep last N versions
   - Delete after X days
   - Keep specific versions

#### Storage Quotas

Monitor usage:

1. **Organization** → **Settings** → **Usage**
2. View storage and bandwidth usage
3. Set up alerts for quota limits

### CloudSmith Pricing

**Free Tier:**
- Unlimited public packages
- 500MB storage
- 5GB bandwidth/month

**Paid Plans:**
- From $75/month
- More storage and bandwidth
- Private repositories
- Team features

See [CloudSmith pricing](https://cloudsmith.com/pricing/) for details.

---

## Choosing Between JFrog and CloudSmith

### Choose JFrog If:

- ✅ Need enterprise-grade features
- ✅ Multiple artifact types (Docker, npm, Maven, etc.)
- ✅ Already invested in JFrog ecosystem
- ✅ Compliance and audit requirements
- ✅ Advanced caching and replication

### Choose CloudSmith If:

- ✅ Prefer modern, simple UI
- ✅ Focus on developer experience
- ✅ Primarily Maven/Gradle packages
- ✅ Startup/scale-up team
- ✅ Lower cost for getting started

### Consider Self-Hosted If:

- ✅ On-premises requirement
- ✅ Air-gapped environment
- ✅ Want full control
- ✅ Have ops resources

See [Custom Maven Repository](publishing-custom-maven.md) guide.

---

## Multi-Cloud Strategy

Publish to multiple cloud services:

```yaml
# project.yml
publishing:
  repositories:
    jfrog:
      enabled: true
      url: https://company.jfrog.io/artifactory/maven-releases/
    
    cloudsmith:
      enabled: true
      owner: company
      repository: maven-backup
```

**Use cases:**
- Redundancy and high availability
- Different teams using different services
- Migration between services
- Regional distribution

---

## Migration

### From Self-Hosted to Cloud

1. **Enable both repositories** during transition:
```yaml
repositories:
  custom_maven:
    enabled: true  # Keep existing
  jfrog:
    enabled: true  # Add cloud
```

2. **Publish to both** for transition period
3. **Update consumer configurations** gradually
4. **Disable self-hosted** once migration complete

### Between Cloud Providers

Use the same strategy - enable both, migrate consumers, then disable old provider.

---

## Troubleshooting

### JFrog Issues

**401 Unauthorized**
- Verify access token is valid and not expired
- Check user has deploy permissions
- Ensure token has correct scopes

**404 Not Found**
- Verify repository exists: `maven-releases`
- Check URL format: `https://yourcompany.jfrog.io/artifactory/maven-releases/`
- Ensure repository is not disabled

### CloudSmith Issues

**403 Forbidden**
- Verify API key has write permissions
- Check organization name is correct
- Ensure repository visibility settings

**Rate Limited**
- CloudSmith has rate limits on free tier
- Consider upgrading plan
- Spread out publishing operations

### General Cloud Issues

**Slow Uploads**
- Check network connection
- Consider enabling compression
- Upload during off-peak hours
- Check if hitting bandwidth limits

**Storage Quota Exceeded**
- Review and delete old packages
- Configure retention policies
- Upgrade storage plan
- Use multiple repositories

---

## Security Best Practices

### API Keys

- ✅ Use API keys/tokens instead of passwords
- ✅ Set appropriate expiration dates
- ✅ Use minimum required scopes
- ✅ Rotate keys regularly
- ✅ Use different keys for CI/CD vs. developers

### Access Control

- ✅ Use organization-level access control
- ✅ Grant minimum required permissions
- ✅ Use entitlements/tokens for consumers
- ✅ Audit access logs regularly
- ✅ Enable MFA for admin accounts

### Network Security

- ✅ Always use HTTPS
- ✅ Verify SSL certificates
- ✅ Use IP allowlisting if available
- ✅ Enable webhooks with secret validation

---

## Next Steps

- [Publishing Overview](publishing.md) - Multi-repository strategy
- [Maven Central](publishing-maven-central.md) - Add public distribution
- [GitHub Packages](publishing-github-packages.md) - Free private alternative
- [Custom Maven](publishing-custom-maven.md) - Self-hosted option
