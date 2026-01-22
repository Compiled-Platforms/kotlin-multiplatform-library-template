# Contributing to Kotlin Multiplatform Library Template

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Java 11 or higher
- Android SDK (for Android targets)
- Xcode (for iOS targets, macOS only)
- Python 3 (for setup scripts)
- Lefthook (for Git hooks)

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/kotlin-multiplatform-library-template.git
   cd kotlin-multiplatform-library-template
   ```
3. Install Lefthook:
   ```bash
   brew install lefthook  # macOS
   lefthook install
   ```
4. Build the project:
   ```bash
   ./gradlew build
   ```

## Development Workflow

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `chore/` for maintenance tasks

### Making Changes

1. Make your changes
2. Run tests: `./gradlew test`
3. Run code quality checks: `./gradlew detekt`
4. Ensure the build passes: `./gradlew build`

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples:**
```
feat: add support for JS target
fix(detekt): resolve false positive warnings
docs: update README with BOM usage
chore: update Kotlin to 2.2.20
```

### Submitting a Pull Request

1. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a Pull Request on GitHub
3. Fill out the PR template
4. Wait for review

## Code Standards

### Kotlin Style

- Follow the [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use the official Kotlin code style (enforced by EditorConfig)
- Maximum line length: 120 characters

### Code Quality

- All code must pass Detekt checks
- Maintain or improve test coverage
- Write clear, self-documenting code
- Add KDoc comments for public APIs

### Testing

- Write tests for new features
- Update tests when modifying existing code
- Ensure all tests pass before submitting PR
- Tests should be:
  - **Fast**: Run quickly
  - **Independent**: Don't depend on other tests
  - **Repeatable**: Give same results every time
  - **Self-validating**: Pass or fail clearly

## Project Structure

```
kotlin-multiplatform-library-template/
├── buildSrc/                  # Convention plugins
├── libraries/                 # Library modules
├── bom/                      # Bill of Materials
├── samples/                  # Sample applications
├── config/                   # Configuration files
│   └── detekt/              # Detekt rules
├── docs/                     # MkDocs documentation
└── scripts/                  # Helper scripts
```

## Documentation

- Update documentation for user-facing changes
- Add examples for new features
- Keep README up to date
- Update MkDocs documentation in `docs/`

## Questions?

- Open a [Discussion](https://github.com/Compiled-Platforms/kotlin-multiplatform-library-template/discussions)
- Check existing [Issues](https://github.com/Compiled-Platforms/kotlin-multiplatform-library-template/issues)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

Thank you for contributing! 🎉
