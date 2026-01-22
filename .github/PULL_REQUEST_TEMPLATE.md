## Description

<!-- Provide a clear and concise description of your changes -->

## Type of Change

<!-- Mark the relevant option with an 'x' -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Configuration change
- [ ] ♻️ Code refactoring
- [ ] ⚡ Performance improvement
- [ ] ✅ Test improvement
- [ ] 🎨 UI/Style update

## Related Issues

<!-- Link to related issues using #issue_number or "Fixes #issue_number" -->

Fixes #
Related to #

## Changes Made

<!-- List the specific changes made in this PR -->

- 
- 
- 

## Testing

<!-- Describe the tests you ran and how to reproduce them -->

### Test Configuration

- Kotlin version:
- Gradle version:
- Platforms tested:
  - [ ] JVM
  - [ ] Android
  - [ ] iOS (arm64)
  - [ ] iOS (x64)
  - [ ] iOS (Simulator arm64)
  - [ ] Linux x64

### Test Results

```bash
# Commands run to test
./gradlew build
./gradlew test
```

## Checklist

<!-- Mark completed items with an 'x' -->

### Code Quality

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have run Detekt and fixed any issues (`./gradlew detekt`)

### Testing

- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have verified all platforms compile and tests pass
- [ ] Code coverage has not decreased (check Kover report)

### Documentation

- [ ] I have updated the documentation accordingly
- [ ] I have updated the CHANGELOG.md (if applicable)
- [ ] I have updated code comments and KDoc where necessary
- [ ] I have added/updated examples in the docs if needed

### API Changes

- [ ] I have run Binary Compatibility Validator (`./gradlew apiCheck`)
- [ ] I have updated API dump files if needed (`./gradlew apiDump`)
- [ ] I have considered backward compatibility
- [ ] Breaking changes are clearly documented

### Build & CI

- [ ] The build passes locally (`./gradlew build`)
- [ ] All GitHub Actions workflows pass
- [ ] I have resolved any merge conflicts
- [ ] I have rebased on the latest `develop` branch

## Screenshots (if applicable)

<!-- Add screenshots or recordings if your change affects UI or visible behavior -->

## Additional Notes

<!-- Add any additional notes, context, or questions for reviewers -->

## Reviewer Notes

<!-- Information specifically for reviewers -->

### Areas of Focus

<!-- Highlight specific areas that need careful review -->

- 
- 

### Questions for Reviewers

<!-- Any questions or areas where you'd like specific feedback -->

- 
- 

---

By submitting this pull request, I confirm that my contribution is made under the terms of the Apache 2.0 license.
