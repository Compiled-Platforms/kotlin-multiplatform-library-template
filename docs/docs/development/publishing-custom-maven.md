# Publishing to Custom Maven Repository

Custom Maven repositories (like Nexus or Artifactory) give you full control over your artifact hosting. Perfect for enterprise environments and self-hosted infrastructure.

## When to Use Custom Maven

✅ **Good for:**
- Enterprise/corporate environments
- On-premises deployment requirements
- Full control over infrastructure
- Custom authentication/authorization
- Compliance and audit requirements
- Air-gapped environments

❌ **Consider alternatives if:**
- You want managed hosting (use JFrog Cloud or CloudSmith)
- Small team without ops resources (use GitHub Packages)
- Public open-source (use Maven Central)

## Common Solutions

| Solution | Type | License | Best For |
|----------|------|---------|----------|
| **Sonatype Nexus** | Repository Manager | Open Source + Pro | Enterprise, mature ecosystem |
| **JFrog Artifactory** | Universal Repository | Open Source + Pro | Multi-format artifacts, DevOps |
| **Apache Archiva** | Repository Manager | Open Source | Lightweight, simple setup |

## Step 1: Set Up Repository Server

### Option A: Sonatype Nexus (Recommended)

#### Install Nexus

```bash
# Download Nexus Repository OSS
wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz
tar -xzf latest-unix.tar.gz
cd nexus-3.x.x-xx/bin
./nexus run
```

Access at: `http://localhost:8081`

Default credentials: `admin` / Check `sonatype-work/nexus3/admin.password`

#### Create Repositories

1. Log in to Nexus
2. Go to **Server administration and configuration** → **Repositories** → **Create repository**

Create two repositories:

**Maven Releases:**
```
Type: maven2 (hosted)
Name: maven-releases
Version policy: Release
Layout policy: Strict
```

**Maven Snapshots:**
```
Type: maven2 (hosted)
Name: maven-snapshots
Version policy: Snapshot
Layout policy: Strict
```

#### Create Deployment User

1. **Settings** → **Security** → **Users** → **Create user**
2. User ID: `deployer`
3. Password: Strong password
4. Roles: `nx-deploy`

### Option B: JFrog Artifactory

#### Install Artifactory

```bash
# Docker (easiest)
docker run --name artifactory -d \
  -p 8081:8081 -p 8082:8082 \
  releases-docker.jfrog.io/jfrog/artifactory-oss:latest
```

Access at: `http://localhost:8082`

Default credentials: `admin` / `password`

#### Create Repositories

1. **Administration** → **Repositories** → **Add Repository** → **Local**
2. Select **Maven**
3. Create two repositories:
   - `maven-releases` (for releases)
   - `maven-snapshots` (for snapshots)

## Step 2: Configure project.yml

```yaml
publishing:
  enabled: true
  
  # Maven coordinates
  group_id: com.yourcompany.kmp
  artifact_id_prefix: kmp
  
  repositories:
    custom_maven:
      enabled: true
      name: Company Nexus
      releases_url: https://nexus.company.com/repository/maven-releases/
      snapshots_url: https://nexus.company.com/repository/maven-snapshots/
  
  signing:
    required: true  # Recommended even for internal use
    key_from_secret: true
```

### URL Formats

**Nexus:**
```
https://nexus.company.com/repository/maven-releases/
https://nexus.company.com/repository/maven-snapshots/
```

**Artifactory:**
```
https://artifactory.company.com/artifactory/maven-releases/
https://artifactory.company.com/artifactory/maven-snapshots/
```

## Step 3: Add GitHub Secrets

Add repository credentials as secrets:

1. **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:

| Secret Name | Value |
|-------------|-------|
| `CUSTOM_MAVEN_USERNAME` | Repository username (e.g., `deployer`) |
| `CUSTOM_MAVEN_PASSWORD` | Repository password |
| `SIGNING_KEY` | Base64-encoded GPG key (optional) |
| `SIGNING_PASSWORD` | GPG key password (optional) |

## Step 4: Local Development Setup

For local publishing, add credentials to `~/.gradle/gradle.properties`:

```properties
# ~/.gradle/gradle.properties
customMaven.username=your-username
customMaven.password=your-password
```

**Security Note**: Never commit this file! It's in `.gitignore` by default.

## Step 5: Publish

### Via CI/CD

Publishing happens automatically when you create a release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

### Manually (Local)

```bash
# Build and publish
./gradlew publish

# Or publish to specific repository
./gradlew publishAllPublicationsToCustomMavenRepository
```

## Step 6: Verify Publication

### Via Web UI

**Nexus:**
1. Browse → `maven-releases` or `maven-snapshots`
2. Navigate to your group ID
3. Find your artifacts

**Artifactory:**
1. Artifacts → `maven-releases` or `maven-snapshots`
2. Tree View → Navigate to your group ID

### Via API

```bash
# Check artifact exists
curl -u username:password \
  https://nexus.company.com/repository/maven-releases/com/yourcompany/kmp/library-name/1.0.0/
```

## Using Published Artifacts

### In Consumer Projects

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            name = "CompanyNexus"
            url = uri("https://nexus.company.com/repository/maven-releases/")
            credentials {
                username = project.findProperty("nexus.username") as String?
                    ?: System.getenv("NEXUS_USERNAME")
                password = project.findProperty("nexus.password") as String?
                    ?: System.getenv("NEXUS_PASSWORD")
            }
        }
    }
}

// build.gradle.kts
dependencies {
    implementation("com.yourcompany.kmp:library-name:1.0.0")
}
```

### User Authentication

Each user needs credentials in `~/.gradle/gradle.properties`:

```properties
nexus.username=their-username
nexus.password=their-password
```

Or set environment variables:
```bash
export NEXUS_USERNAME=their-username
export NEXUS_PASSWORD=their-password
```

## Advanced Configuration

### Repository Groups (Nexus/Artifactory)

Create a group repository that combines multiple repositories:

**Nexus:**
1. Create repository → `maven2 (group)`
2. Name: `maven-public`
3. Members: `maven-releases`, `maven-snapshots`, `maven-central`

Users configure single URL:
```kotlin
maven {
    url = uri("https://nexus.company.com/repository/maven-public/")
}
```

### Proxy Remote Repositories

Cache external dependencies (Maven Central, Google, etc.):

**Nexus:**
1. Create repository → `maven2 (proxy)`
2. Remote URL: `https://repo1.maven.org/maven2/`
3. Add to group repository

**Benefits:**
- ✅ Faster builds (local cache)
- ✅ Resilient to external outages
- ✅ Control over external dependencies

### Anonymous Read Access

Allow unauthenticated downloads (read-only):

**Nexus:**
1. **Security** → **Anonymous Access** → Enable
2. **Roles** → `nx-anonymous` → Add `nx-repository-view-*-*-read`

**Artifactory:**
1. **Repositories** → Select repository → **Permissions**
2. Add `anonymous` user with read permission

Then consumers don't need credentials for downloads:
```kotlin
maven {
    url = uri("https://nexus.company.com/repository/maven-public/")
    // No credentials needed!
}
```

## Security Best Practices

### SSL/TLS Configuration

Always use HTTPS for production:

**Nexus:**
1. **Administration** → **Server** → **SSL Certificates**
2. Upload certificate
3. Configure `nexus.properties` for SSL

**Artifactory:**
1. **Administration** → **General Configuration** → **HTTP Settings**
2. Enable SSL
3. Upload certificate

### Access Control

**Principle of Least Privilege:**

| Role | Permissions | Use Case |
|------|-------------|----------|
| Deployer | Deploy (write) | CI/CD publishing |
| Developer | Read | Building projects |
| Admin | Full access | Infrastructure management |

**Nexus:**
1. **Security** → **Roles** → Create custom roles
2. Assign minimal required permissions

**Artifactory:**
1. **Administration** → **Security** → **Permissions**
2. Create permission targets for repositories

### Token-Based Authentication

Use API tokens instead of passwords:

**Nexus:**
1. **Security** → **User Tokens** → Enable
2. Users can generate tokens in their profile

**Artifactory:**
1. Profile → **Authentication Settings** → **Generate Token**

Update GitHub secrets to use tokens:
```
CUSTOM_MAVEN_PASSWORD → API token instead of password
```

## Backup and Disaster Recovery

### Backup Strategy

**What to backup:**
- Repository data (artifacts)
- Repository metadata
- Configuration files
- User and permission data

**Nexus Backup:**
```bash
# Backup blob stores
tar -czf nexus-backup.tar.gz sonatype-work/nexus3/blobs/

# Backup database
pg_dump nexus > nexus-db-backup.sql
```

**Artifactory Backup:**
```bash
# Use built-in backup
# Administration → Backup → Create Backup
```

### High Availability

For production environments:

**Nexus HA (Pro):**
- Active-active cluster
- Shared blob store (S3, NFS)
- Load balancer

**Artifactory HA:**
- Multiple nodes
- Shared database
- Binary replication

## Monitoring

### Health Checks

**Nexus:**
```bash
curl https://nexus.company.com/service/rest/v1/status
```

**Artifactory:**
```bash
curl https://artifactory.company.com/artifactory/api/system/ping
```

### Metrics

**Key metrics to monitor:**
- Repository size
- Number of artifacts
- Download/upload rates
- Failed authentication attempts
- Disk space usage

**Nexus (Prometheus):**
```yaml
# Enable metrics
nexus.analytics.enabled=true
```

**Artifactory:**
- Built-in analytics dashboard
- Integration with Prometheus/Grafana

## Troubleshooting

### 401 Unauthorized

**Problem**: Authentication failed

**Solution**:
- Verify credentials are correct
- Check user has deployment permissions
- Ensure token hasn't expired
- Test credentials via web UI first

### 403 Forbidden

**Problem**: User authenticated but lacks permissions

**Solution**:
- Check user has `nx-deploy` role (Nexus) or deploy permissions (Artifactory)
- Verify repository permissions
- Check repository exists and is enabled

### Connection Refused / Timeout

**Problem**: Cannot reach repository server

**Solution**:
- Verify URL is correct
- Check server is running
- Verify firewall rules allow connection
- Check SSL certificate is valid

### Artifact Already Exists

**Problem**: Trying to redeploy same version

**Solution**:
- Don't redeploy release versions (immutable)
- Use SNAPSHOT versions for development
- Configure repository to allow redeployment (not recommended for releases)

## Cost Optimization

### Open Source vs Pro

**Nexus Repository OSS (Free):**
- ✅ Maven repositories
- ✅ Docker registry
- ✅ npm, PyPI, etc.
- ❌ High availability
- ❌ Advanced security

**Nexus Repository Pro:**
- ✅ Everything in OSS
- ✅ High availability
- ✅ Advanced security features
- ✅ Staging repositories

### Infrastructure Costs

**Self-hosted:**
- Server costs (VM/bare metal)
- Storage costs
- Bandwidth
- Operations/maintenance

**Cloud-hosted:**
- Consider [JFrog Cloud](publishing-cloud-services.md#jfrog) or [CloudSmith](publishing-cloud-services.md#cloudsmith) for managed hosting

## Migration

### From Maven Central to Custom Maven

Keep both enabled during transition:

```yaml
# project.yml
publishing:
  repositories:
    maven_central:
      enabled: true  # Keep for existing users
    custom_maven:
      enabled: true  # Add for internal use
```

### From GitHub Packages to Custom Maven

Similar strategy - enable both, gradually migrate consumers.

## Next Steps

- [JFrog Artifactory Cloud](publishing-cloud-services.md#jfrog) - Managed alternative
- [GitHub Packages](publishing-github-packages.md) - Simpler alternative
- [Publishing Overview](publishing.md) - Multi-repository strategy
