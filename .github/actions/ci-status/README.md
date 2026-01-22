# CI Status Checker Action

A composite GitHub Action that reads `project.yml` configuration and determines if CI should run for the current branch.

## Features

- ✅ Branch-specific CI control
- ✅ Reads configuration from `project.yml`
- ✅ Creates visible GitHub Actions annotations
- ✅ Provides all necessary outputs for workflows
- ✅ Fully tested with pytest

## Usage

```yaml
jobs:
  config:
    runs-on: ubuntu-latest
    outputs:
      ci-enabled: ${{ steps.status.outputs.ci-enabled }}
      java-version: ${{ steps.status.outputs.java-version }}
    steps:
      - uses: actions/checkout@v6
      
      - name: Check CI Status
        id: status
        uses: ./.github/actions/ci-status
        with:
          config-file: project.yml  # Optional, defaults to project.yml
  
  build:
    needs: config
    if: needs.config.outputs.ci-enabled == 'true'
    steps:
      - name: Build
        run: echo "Building..."
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `config-file` | Path to project.yml | No | `project.yml` |

## Outputs

| Name | Description |
|------|-------------|
| `ci-enabled` | Whether CI is enabled (`true`/`false`) |
| `current-branch` | Current branch name |
| `enabled-branches` | Configured enabled branches |
| `java-version` | Java version from config |
| `python-version` | Python version from config |
| `runner` | Primary runner from config |
| `gradle-flags` | Gradle flags from config |
| `kotlin-native-cache` | Whether Kotlin/Native caching is enabled |
| `pages-enabled` | Whether GitHub Pages is enabled |

## Configuration

The action reads from `project.yml`:

```yaml
ci:
  enabled_branches: [main, develop]  # Or 'all' or false
```

## Testing

```bash
cd .github/actions/ci-status

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest test_ci_status.py -v

# With coverage
pytest test_ci_status.py --cov=ci_status --cov-report=term-missing

# Watch mode
ptw
```

## Development

**File Structure:**
```
.github/actions/ci-status/
├── action.yml              # Action definition
├── ci_status.py           # Main Python script
├── test_ci_status.py      # Pytest tests
├── requirements.txt       # Runtime deps
├── requirements-dev.txt   # Dev deps
└── README.md             # This file
```

**Adding Features:**
1. Update `ci_status.py`
2. Add tests to `test_ci_status.py`
3. Run tests: `pytest -v`
4. Update `action.yml` if needed

## License

Apache-2.0
