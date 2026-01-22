# Contributing

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

Be respectful and inclusive. We're all here to build great software together.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports:

1. **Check existing issues** - Someone may have already reported it
2. **Verify the issue** - Make sure it's reproducible
3. **Collect information** - Version numbers, error messages, steps to reproduce

Create a detailed bug report including:

- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Kotlin version, etc.)
- Code samples or stack traces

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:

- Use case description
- Current limitations
- Proposed solution
- Alternative solutions considered

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** - `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** - Ensure your changes are tested
5. **Run quality checks** - `./gradlew build detekt`
6. **Commit your changes** - Use clear, descriptive commit messages
7. **Push to your fork** - `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## Development Process

### Setting Up

See the [Development Setup](../development/setup.md) guide.

### Coding Standards

- **Code Style** - Follow Kotlin coding conventions
- **Detekt** - All code must pass Detekt checks
- **Tests** - Add tests for new functionality
- **Documentation** - Update docs for user-facing changes
- **Commit Messages** - Use clear, descriptive messages

### Testing

```bash
# Run all tests
./gradlew test

# Run specific test
./gradlew :libraries:example-library:test

# Run code quality checks
./gradlew detekt
```

### Documentation

Update documentation when making changes:

- Add examples for new features
- Update existing docs if behavior changes
- Include code samples
- Run `mkdocs serve` to preview docs locally

## Pull Request Process

1. **Update dependencies** - Keep dependencies current
2. **Update docs** - Include documentation changes
3. **Add tests** - Ensure adequate test coverage
4. **Pass CI** - All checks must pass
5. **Get review** - At least one approval required
6. **Squash commits** - Clean up commit history before merge

## Release Process

Maintainers follow this process for releases:

1. Update version numbers
2. Update CHANGELOG
3. Create release commit
4. Tag the release
5. Push to GitHub
6. CI publishes to Maven Central
7. Create GitHub release with notes

## Questions?

- Open a [GitHub Discussion](https://github.com/compiledplatforms/kotlin-multiplatform-library-template/discussions)
- Check existing [Issues](https://github.com/compiledplatforms/kotlin-multiplatform-library-template/issues)

## Recognition

Contributors will be recognized in:

- GitHub contributors list
- Release notes
- Project documentation

Thank you for contributing! 🎉
