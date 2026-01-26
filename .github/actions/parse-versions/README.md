# Parse Versions Action

A composite GitHub Action that parses version information from `gradle/libs.versions.toml` for use in CI workflows.

## Overview

This action provides a centralized way to read tool versions (Java, Python) from your project's version catalog, ensuring consistency across all workflows.

## Features

- ✅ Parses `gradle/libs.versions.toml` (single source of truth)
- ✅ Outputs CI tool versions for GitHub Actions
- ✅ Provides sensible defaults if versions are missing
- ✅ Fully tested with unit tests

## Usage

```yaml
jobs:
  versions:
    runs-on: ubuntu-latest
    outputs:
      java-version: ${{ steps.parse-versions.outputs.java-version }}
      python-version: ${{ steps.parse-versions.outputs.python-version }}
    steps:
      - uses: actions/checkout@v6
      
      - name: Parse Versions
        id: parse-versions
        uses: ./.github/actions/parse-versions
        
  build:
    needs: versions
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-java@v5
        with:
          distribution: 'temurin'
          java-version: ${{ needs.versions.outputs.java-version }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `toml-file` | Path to libs.versions.toml | No | `gradle/libs.versions.toml` |

## Outputs

| Output | Description | Default |
|--------|-------------|---------|
| `java-version` | Java version for CI runners | `17` |
| `python-version` | Python version for CI runners | `3.11` |

## Version Configuration

Add these versions to your `gradle/libs.versions.toml`:

```toml
[versions]
# Tool versions for CI/CD
python-ci = "3.11"       # Python version for GitHub Actions runners
java-ci = "17"           # Java version for GitHub Actions runners

# Java versions for build
java-toolchain = "17"    # JVM toolchain for Kotlin compilation
java-target = "11"       # Target JVM bytecode version
```

The action reads:
- `java-ci` - Version for `setup-java` action
- `python-ci` - Version for `setup-python` action

Other versions (toolchain, target) are for Gradle and not used by this action.

## Development

### Running Tests

```bash
cd .github/actions/parse-versions

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest test_parse_versions.py -v

# Run with coverage
pytest test_parse_versions.py --cov=. --cov-report=html
```

### Test Coverage

The test suite includes:
- ✅ Unit tests for TOML parsing
- ✅ Version extraction with defaults
- ✅ GitHub Actions output formatting
- ✅ Integration tests
- ✅ Error handling

## Dependencies

- **Production**: `tomli` (TOML parser for Python <3.11)
- **Development**: `pytest`, `pytest-cov`

## License

Same as parent repository.
