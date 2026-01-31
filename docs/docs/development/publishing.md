# Publishing Overview

This template supports flexible publishing to multiple repository types. Configure once in `project.yml`, publish anywhere.

## Supported Repositories

| Repository | Type | Use Case | Cost |
|------------|------|----------|------|
| [Maven Central](publishing-maven-central.md) | Public | Open-source libraries | Free |
| [GitHub Packages](publishing-github-packages.md) | Private/Public | Team/org libraries | Free for private repos |
| [Custom Maven](publishing-custom-maven.md) | Private | Self-hosted Nexus/Artifactory | Your infrastructure |
| [JFrog Cloud](publishing-cloud-services.md#jfrog) | Private | Managed Artifactory | Paid service |
| [CloudSmith](publishing-cloud-services.md#cloudsmith) | Private | Modern package hosting | Paid service |

## Quick Start

### 1. Configure in `project.yml`

```yaml
publishing:
  enabled: true
  group_id: com.yourcompany.kmp
  
  repositories:
    maven_central:
      enabled: true      # ← Enable desired repositories
      auto_release: false
    
    github_packages:
      enabled: false     # ← Enable/disable as needed
      owner: your-org
      repository: your-repo
```

### 2. Add Required Secrets

Each repository requires specific secrets in GitHub Actions:

| Repository | Required Secrets |
|------------|------------------|
| Maven Central | `MAVEN_CENTRAL_USERNAME`, `MAVEN_CENTRAL_PASSWORD` |
| GitHub Packages | `GITHUB_TOKEN` (automatically provided) |
| Custom Maven | `CUSTOM_MAVEN_USERNAME`, `CUSTOM_MAVEN_PASSWORD` |
| JFrog | `JFROG_USERNAME`, `JFROG_PASSWORD` |
| CloudSmith | `CLOUDSMITH_API_KEY` |
| All (signing) | `SIGNING_KEY`, `SIGNING_PASSWORD` |

### 3. Publish

```bash
# Test locally
./gradlew publishToMavenLocal

# Publish to configured repositories
./gradlew publish

# Or let CI/CD handle it on release
git tag v1.0.0
git push origin v1.0.0
```

## Publishing Strategy

The template supports two publishing strategies:

### Manual Publishing (Recommended)

- **When**: Only on explicit releases
- **How**: Create GitHub release or push tag
- **Why**: Full control, review before publish

```yaml
# project.yml
publishing:
  strategy:
    snapshots_on_main: false
    releases_on_tag: true
```

### Automatic Publishing

- **When**: Every commit to main (snapshots)
- **How**: CI automatically publishes
- **Why**: Continuous delivery for internal teams

```yaml
# project.yml
publishing:
  strategy:
    snapshots_on_main: true
    releases_on_tag: true
```

## Configuration Validation

Validate your configuration before publishing:

```bash
# Check configuration is valid
python3 scripts/get-publishing-config.py --validate

# See which repositories are enabled
python3 scripts/get-publishing-config.py --list-enabled

# Get configuration for specific repository
python3 scripts/get-publishing-config.py --repository maven_central
```

## Publishing Workflow

### Local Development

```bash
# 1. Test build
./gradlew clean build

# 2. Publish to local Maven repository
./gradlew publishToMavenLocal

# 3. Test in another project
# Add mavenLocal() to repositories
# Then depend on: com.yourcompany.kmp:library-name:1.0.0-SNAPSHOT
```

### CI/CD Publishing

The workflow automatically:

1. ✅ Validates `project.yml` configuration
2. ✅ Builds and tests all platforms
3. ✅ Signs artifacts (if enabled)
4. ✅ Publishes to all enabled repositories
5. ✅ Creates GitHub release (optional)

See `.github/workflows/publish.yml` for details.

## Repository-Specific Guides

Choose your publishing target(s):

### Public Publishing

- **[Maven Central](publishing-maven-central.md)** - Industry standard for open-source Kotlin/Java libraries

### Private Publishing

- **[GitHub Packages](publishing-github-packages.md)** - Free, integrated with GitHub, great for org/team libraries
- **[Custom Maven Repository](publishing-custom-maven.md)** - Self-hosted Nexus or Artifactory
- **[Cloud Services](publishing-cloud-services.md)** - JFrog Artifactory Cloud or CloudSmith

## Multiple Repositories

You can publish to multiple repositories simultaneously:

```yaml
# project.yml
publishing:
  repositories:
    maven_central:
      enabled: true       # Public open-source release
    
    github_packages:
      enabled: true       # Private development snapshots
      owner: your-org
      repository: maven-packages
```

This allows:
- Public releases → Maven Central
- Development snapshots → GitHub Packages
- Keep internal versions private while releasing stable versions publicly

## Artifact Signing

All repositories require or strongly recommend signing artifacts:

### Using GitHub Actions Secrets (Recommended)

```yaml
# project.yml
publishing:
  signing:
    required: true
    key_from_secret: true
```

Add secrets to GitHub:
- `SIGNING_KEY` - Base64-encoded GPG key
- `SIGNING_PASSWORD` - GPG key password

See [Maven Central guide](publishing-maven-central.md#gpg-key-setup) for generating keys.

### Using Local GPG (Development)

```yaml
# project.yml
publishing:
  signing:
    required: true
    key_from_secret: false  # Uses ~/.gnupg
```

## Versioning

Versions are managed through `gradle.properties`:

```properties
# gradle.properties
VERSION_NAME=1.0.0
```

### Version Formats

- **Release**: `1.0.0`
- **Snapshot**: `1.0.0-SNAPSHOT`
- **Pre-release**: `1.0.0-alpha.1`

Follow [Semantic Versioning](https://semver.org/):
- **Major** (x.0.0): Breaking changes
- **Minor** (1.x.0): New features, backward compatible
- **Patch** (1.0.x): Bug fixes, backward compatible

## Troubleshooting

### Configuration Issues

```bash
# Validate configuration
python3 scripts/get-publishing-config.py --validate

# Check required secrets for a repository
python3 scripts/get-publishing-config.py --required-secrets maven_central
```

### Publishing Failures

**401 Unauthorized**
- Check credentials are correct in secrets
- Verify account is active and has permissions

**Signature Verification Failed**
- Ensure `SIGNING_KEY` is complete base64-encoded key
- Verify `SIGNING_PASSWORD` is correct

**Repository Not Found**
- Check repository URLs in `project.yml`
- Verify owner/organization names

### Local Testing

Skip signing for local development:

```bash
./gradlew publish -PskipSigning=true
```

## Best Practices

### Security

- ✅ Use GitHub Actions secrets for credentials
- ✅ Never commit secrets to version control
- ✅ Rotate credentials regularly
- ✅ Use API tokens instead of passwords when possible

### Release Process

- ✅ Test locally with `publishToMavenLocal` first
- ✅ Validate configuration before releasing
- ✅ Update CHANGELOG.md
- ✅ Tag releases with semantic versions
- ✅ Let CI handle publishing (don't publish from local machine)

### Multi-Repository Strategy

- **Public + Private**: Maven Central for releases, GitHub Packages for snapshots
- **Multi-Org**: Separate repositories for different teams/organizations
- **Staging**: Custom Maven for staging, production repository for releases

## Next Steps

- [Set up Maven Central](publishing-maven-central.md)
- [Set up GitHub Packages](publishing-github-packages.md)
- [Set up Custom Maven](publishing-custom-maven.md)
- [Set up Cloud Services](publishing-cloud-services.md)
