# TODO - Template Improvements

This document tracks potential enhancements for the Kotlin Multiplatform Library Template.

## Priority: High ⭐

### 1. GitHub Actions CI/CD Pipeline ✅ **COMPLETE**
Automate building, testing, and publishing across all platforms.

**Benefits:**
- Automated builds and tests on every PR
- Automatic publishing to Maven Central on release
- Multi-platform testing (macOS for iOS, Linux for JVM/Android/Linux, Windows optional)
- Generate and publish documentation automatically
- Enforce code quality gates

**Implementation:**
- [x] Create `.github/workflows/build.yml` for PR validation
- [x] Create `.github/workflows/publish.yml` for release publishing
- [x] Create `.github/workflows/docs.yml` for documentation deployment
- [x] Add secrets documentation (signing keys, Sonatype credentials)
- [x] Configure matrix builds for multiple platforms
- [x] Multi-platform testing (Ubuntu, macOS, Windows)
- [x] Detekt integration in CI
- [x] Dokka documentation generation in CI
- [x] Artifact uploads (JARs, AARs, test results)
- [x] GitHub Pages deployment for documentation
- [x] Comprehensive setup guide (`.github/SETUP_GITHUB_ACTIONS.md`)
- [x] Usage documentation (`docs/docs/development/github-actions.md`)

**Workflows:**
- **build.yml**: Runs on every PR/push - builds, tests, runs Detekt, generates docs
- **publish.yml**: Publishes to Maven Central on releases
- **docs.yml**: Deploys Dokka + MkDocs to GitHub Pages

**Resources:**
- [GitHub Actions for Gradle](https://github.com/gradle/gradle-build-action)
- [Publishing to Maven Central with GitHub Actions](https://vanniktech.github.io/gradle-maven-publish-plugin/central/#configuring-the-pom)
- [Setup Guide](.github/SETUP_GITHUB_ACTIONS.md)

---

### 2. Dokka API Documentation ✅ **COMPLETE**
Generate professional KDoc-based API documentation.

**Benefits:**
- Professional HTML documentation for all modules
- Multi-module and multi-platform support
- Multiple output formats (HTML, Markdown, Javadoc)
- Automatic publishing to GitHub Pages
- Better developer experience for library users

**Implementation:**
- [x] Add Dokka plugin to convention plugin
- [x] Configure per-library documentation
- [x] Configure multi-module documentation support
- [x] Create documentation writing guidelines
- [x] Set up GitHub Pages deployment (in CI/CD)
- [x] Add documentation generation to CI/CD

**Resources:**
- [Dokka Documentation](https://kotlinlang.org/docs/dokka-introduction.html)
- [Dokka Gradle Plugin](https://kotlinlang.org/docs/dokka-gradle.html)

**Usage:**
```bash
# Generate docs for a single library
./gradlew :libraries:example-library:dokkaGeneratePublicationHtml

# Generate docs for all libraries
./gradlew dokkaGeneratePublicationHtml
```

---

### 3. Binary Compatibility Validator ✅ **COMPLETE**
Prevent accidental breaking changes to public API.

**Benefits:**
- Tracks public API changes across versions
- Fails build on binary incompatible changes
- Generates API dump files for review
- Essential for semantic versioning
- Protects library users from unexpected breaks

**Implementation:**
- [x] Add `kotlinx-binary-compatibility-validator` plugin (v0.18.1)
- [x] Generate initial API dumps for all modules
- [x] Configure exclusions for internal APIs (samples, BOM, internal packages)
- [x] Add validation to CI/CD pipeline (runs with `check`)
- [x] Document API change workflow
- [x] Enable experimental KLib ABI validation for multiplatform
- [x] Add comprehensive documentation (`docs/docs/development/api-compatibility.md`)

**Usage:**
```bash
# Generate/update API dumps
./gradlew apiDump

# Verify API compatibility (runs automatically in CI)
./gradlew apiCheck
```

**Resources:**
- [Binary Compatibility Validator](https://github.com/Kotlin/binary-compatibility-validator)
- [Semantic Versioning](https://semver.org/)
- [Documentation](docs/docs/development/api-compatibility.md)

---

## Priority: Medium 📊

### 4. Kover Code Coverage
Track test coverage across all platforms.

**Benefits:**
- Kotlin-native coverage tool from JetBrains
- Multi-platform support
- Integrates with CI/CD
- HTML and XML reports for coverage visualization
- Helps identify untested code paths

**Implementation:**
- [ ] Add Kover plugin to convention plugin
- [ ] Configure coverage thresholds
- [ ] Generate coverage reports in CI/CD
- [ ] Integrate with coverage reporting services (Codecov, Coveralls)
- [ ] Add coverage badges to README

**Resources:**
- [Kover Plugin](https://github.com/Kotlin/kotlinx-kover)
- [Codecov](https://codecov.io/)

---

### 5. Dependency Updates Automation
Keep dependencies up-to-date automatically.

**Benefits:**
- Automated PR creation for dependency updates
- Reduces security vulnerabilities
- Customizable update schedules
- Grouped updates by type (major, minor, patch)
- Reduces maintenance burden

**Implementation:**
- [ ] Choose between Renovate or Dependabot
- [ ] Create configuration file (`.github/renovate.json` or `.github/dependabot.yml`)
- [ ] Configure update schedules
- [ ] Set up grouping rules for related dependencies
- [ ] Configure auto-merge rules for low-risk updates

**Resources:**
- [Renovate](https://docs.renovatebot.com/)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)

---

### 6. GitHub Templates
Improve contributor experience with issue and PR templates.

**Benefits:**
- Consistent bug reports and feature requests
- Better information gathering from contributors
- Faster issue triage
- Professional project appearance
- Guides contributors through the process

**Implementation:**
- [ ] Create `.github/ISSUE_TEMPLATE/bug_report.yml`
- [ ] Create `.github/ISSUE_TEMPLATE/feature_request.yml`
- [ ] Create `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Add config for issue template chooser
- [ ] Include links to contributing guidelines

**Resources:**
- [GitHub Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)

---

## Priority: Low 🔧

### 7. Version Catalog Documentation
Document all dependencies and versions.

**Benefits:**
- Clear visibility of all dependencies
- Helps users choose compatible versions
- Can be included in release notes
- Useful for security audits

**Implementation:**
- [ ] Create script to generate dependency markdown
- [ ] Add to documentation site
- [ ] Include in release process
- [ ] Add dependency graphs

---

### 8. Gradle Build Scans
Enable performance insights for builds.

**Benefits:**
- Detailed build performance analysis
- Dependency resolution insights
- Build failure debugging
- Configuration cache diagnostics
- Helps optimize build times

**Implementation:**
- [ ] Add build scan plugin
- [ ] Configure automatic publishing (opt-in)
- [ ] Add build scan links to CI/CD output
- [ ] Document how to read and use build scans

**Resources:**
- [Gradle Build Scans](https://scans.gradle.com/)
- [Gradle Enterprise](https://gradle.com/gradle-enterprise/)

---

### 9. Pre-commit Hooks Enhancement
Expand current Lefthook configuration.

**Benefits:**
- More comprehensive pre-commit checks
- Catch issues before CI/CD
- Faster feedback loop
- Enforce code standards locally

**Potential Additions:**
- [ ] Kotlin formatting check (ktlint)
- [ ] License header validation
- [ ] TODO/FIXME detection
- [ ] Large file prevention
- [ ] Trailing whitespace removal
- [ ] YAML/JSON validation

---

### 10. Sample Applications Enhancement
Expand sample applications for better demonstration.

**Benefits:**
- Better showcase of library features
- Real-world usage examples
- Testing ground for new features
- Documentation through code

**Implementation:**
- [ ] Add Android app sample
- [ ] Add iOS app sample (SwiftUI)
- [ ] Add Compose Multiplatform sample
- [ ] Add backend sample (Ktor)
- [ ] Document how to run each sample

---

## Future Considerations 💭

### Performance Testing
- Benchmarking framework integration
- Performance regression detection

### Security
- OWASP dependency check
- Security scanning in CI/CD
- Vulnerability disclosure policy

### Accessibility
- Documentation accessibility audit
- API naming consistency checks

### Internationalization
- i18n support examples
- Multi-language documentation

---

## Completed ✅

- [x] **GitHub Actions CI/CD** - Build, test, publish, and deploy workflows
- [x] **Dokka API Documentation** - KDoc generation with GitHub Pages deployment
- [x] **Binary Compatibility Validator** - API stability tracking with BCV
- [x] Enhanced `gradle.properties` with performance optimizations
- [x] Community health files (CODE_OF_CONDUCT, SECURITY, CONTRIBUTING, LICENSE, NOTICE)
- [x] Migrate `buildSrc` to `build-logic`
- [x] R8 optimization support for Android libraries
- [x] Detekt static code analysis
- [x] MkDocs Material documentation
- [x] Lefthook Git hooks (with GitHub Actions secret handling)
- [x] EditorConfig for consistent formatting
- [x] git-cliff for automated changelog generation
- [x] Bill of Materials (BOM) support
- [x] Setup automation scripts (Python)
- [x] Sample application structure

---

## Notes

- Prioritize items based on your specific needs and timeline
- Each item can be tackled independently
- Consider community feedback when prioritizing
- Some items may require paid services (e.g., Gradle Enterprise)
- Test each addition thoroughly before merging

---

**Last Updated:** 2026-01-20
