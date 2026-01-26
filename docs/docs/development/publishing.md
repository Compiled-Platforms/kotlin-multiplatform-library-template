# Publishing

Guide to publishing your libraries to Maven Central.

## Prerequisites

Before publishing, you need:

1. **Sonatype Account** - Sign up at [Sonatype JIRA](https://issues.sonatype.org)
2. **GPG Key** - For signing artifacts
3. **Verified Domain/Group** - Claim your group ID on Sonatype

## Configuration

### 1. Create `gradle.properties`

Create `gradle.properties` in your user home (`~/.gradle/gradle.properties`):

```properties
# Sonatype credentials
mavenCentralUsername=your-username
mavenCentralPassword=your-password

# Signing configuration
signing.keyId=your-key-id
signing.password=your-key-password
signing.secretKeyRingFile=/path/to/secring.gpg
```

!!! warning "Security"
    Never commit `gradle.properties` with credentials to version control!

### 2. GPG Key Setup

Generate a GPG key if you don't have one:

```bash
# Generate key
gpg --gen-key

# Export secret key
gpg --export-secret-keys your-email@example.com > secring.gpg

# Get key ID
gpg --list-secret-keys --keyid-format SHORT
```

Upload your public key:

```bash
gpg --keyserver keyserver.ubuntu.com --send-keys YOUR_KEY_ID
```

## Publishing Process

### Publishing to Maven Local (Testing)

Test your library locally first:

```bash
./gradlew publishToMavenLocal
```

This publishes to `~/.m2/repository/`. Test by depending on it in another project.

### Publishing to Maven Central

1. **Verify Build**
   ```bash
   ./gradlew clean build
   ```

2. **Publish to Staging**
   ```bash
   ./gradlew publish
   ```

3. **Release from Staging**
   - Log in to [Nexus Repository Manager](https://s01.oss.sonatype.org/)
   - Navigate to "Staging Repositories"
   - Find your repository
   - Click "Close" then "Release"

### Automated Publishing

For automated releases, use the `vanniktech-maven-publish` plugin tasks:

```bash
# Publish and automatically release
./gradlew publishToMavenCentral --no-configuration-cache
```

## Versioning

### Library Versions

Each library has its own version in `build.gradle.kts`:

```kotlin
version = "1.0.0"
```

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### BOM Versioning

The BOM has its own version and lists compatible library versions:

```kotlin title="bom/build.gradle.kts"
version = "1.0.0"  // BOM version

dependencies.constraints {
    api("com.compiledplatforms.kmp.library:example-library:1.0.0")
    api("com.compiledplatforms.kmp.library:my-library:2.3.0")
}
```

## Release Checklist

Before releasing:

- [ ] All tests pass: `./gradlew test`
- [ ] Code quality checks pass: `./gradlew detekt`
- [ ] Documentation is updated
- [ ] CHANGELOG is updated
- [ ] Version numbers are bumped
- [ ] BOM is updated with new library versions
- [ ] Commit and tag the release
  ```bash
  git tag -a v1.0.0 -m "Release 1.0.0"
  git push origin v1.0.0
  ```

## CI/CD Integration

### GitHub Actions

Example workflow for automated publishing:

```yaml title=".github/workflows/publish.yml"
name: Publish to Maven Central

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '11'
      
      - name: Publish
        env:
          ORG_GRADLE_PROJECT_mavenCentralUsername: ${{ secrets.MAVEN_CENTRAL_USERNAME }}
          ORG_GRADLE_PROJECT_mavenCentralPassword: ${{ secrets.MAVEN_CENTRAL_PASSWORD }}
          ORG_GRADLE_PROJECT_signingKeyId: ${{ secrets.SIGNING_KEY_ID }}
          ORG_GRADLE_PROJECT_signingPassword: ${{ secrets.SIGNING_PASSWORD }}
          ORG_GRADLE_PROJECT_signingKey: ${{ secrets.SIGNING_KEY }}
        run: ./gradlew publishToMavenCentral --no-configuration-cache
```

Add secrets in GitHub repository settings.

## Troubleshooting

### Common Issues

**Missing signatures**
- Ensure GPG key is properly configured
- Check `signing.keyId` matches your key

**Validation errors**
- Verify POM information is complete
- Check that group ID is claimed on Sonatype

**Timeout errors**
- Try publishing again
- Check Sonatype status page

### Support

- [Sonatype Guide](https://central.sonatype.org/publish/)
- [vanniktech plugin docs](https://vanniktech.github.io/gradle-maven-publish-plugin/)

## Next Steps

- [Configuration](../getting-started/configuration.md) - Advanced configuration
- [Contributing](../about/contributing.md) - Contribution guidelines
