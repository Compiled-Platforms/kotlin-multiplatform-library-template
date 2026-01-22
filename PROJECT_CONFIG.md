# Project Configuration System

This project uses a centralized configuration file (`project.yml`) as a **single source of truth** for all tooling, CI/CD, and project settings.

## Overview

Instead of hardcoding values across multiple files, all configuration is defined once in `project.yml` and consumed by:

- ✅ GitHub Actions workflows
- ✅ Shell scripts
- ✅ Documentation
- ✅ Local development tools
- ✅ Publishing configurations

## Configuration File

**Location:** `project.yml` (project root)

**Structure:**
```yaml
project:        # Project metadata and info
versions:       # Tool and runtime versions
platforms:      # Platform-specific settings
ci:             # CI/CD configuration
testing:        # Testing frameworks and strategy
code_quality:   # Code quality tools
publishing:     # Maven/package publishing
documentation:  # Docs generation and deployment
dependencies:   # Dependency management
release:        # Release process
development:    # Workflow and conventions
security:       # Security policies
```

## Reading Configuration

### In GitHub Actions

Workflows automatically load config values using a `config` job:

```yaml
jobs:
  config:
    runs-on: ubuntu-latest
    outputs:
      java-version: ${{ steps.load.outputs.java-version }}
    steps:
      - uses: actions/checkout@v6
      - id: load
        run: |
          sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
          sudo chmod +x /usr/local/bin/yq
          echo "java-version=$(yq '.versions.java' project.yml)" >> $GITHUB_OUTPUT
  
  build:
    needs: config
    steps:
      - uses: actions/setup-java@v5
        with:
          java-version: ${{ needs.config.outputs.java-version }}
```

### In Python Scripts

Use the provided helper script:

```bash
# Get a single value
python scripts/get-config.py versions.java
# Output: 17

# Get an array
python scripts/get-config.py platforms.enabled
# Output:
# - android
# - ios
# - jvm
# - linux

# Use in scripts
JAVA_VERSION=$(python scripts/get-config.py versions.java)
echo "Using Java $JAVA_VERSION"
```

### Programmatically

**Python (using the helper):**
```python
import subprocess

def get_config(path: str) -> str:
    result = subprocess.run(
        ['python', 'scripts/get-config.py', path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

java_version = get_config('versions.java')
```

**Python (direct YAML parsing):**
```python
import yaml

with open('project.yml') as f:
    config = yaml.safe_load(f)
    print(config['versions']['kotlin'])
```

**Shell (from bash scripts):**
```bash
# Use yq if available
yq '.versions.kotlin' project.yml

# Or use the Python helper
KOTLIN_VERSION=$(python scripts/get-config.py versions.kotlin)
```

## Common Configuration Values

### Versions
```bash
python scripts/get-config.py versions.java        # 17
python scripts/get-config.py versions.kotlin      # 2.3.0
python scripts/get-config.py versions.gradle      # 9.0.0
python scripts/get-config.py versions.python      # 3.11
```

### CI Settings
```bash
python scripts/get-config.py ci.enabled_branches          # Branch list or "all" or false
python scripts/get-config.py ci.runners.primary           # ubuntu-latest
python scripts/get-config.py ci.gradle_flags              # List of flags
python scripts/get-config.py ci.caching.kotlin_native     # true
```

### Platform Configuration
```bash
python scripts/get-config.py platforms.enabled                  # List of enabled platforms
python scripts/get-config.py platforms.android.min_sdk          # 24
python scripts/get-config.py platforms.ios.deployment_target    # 13.0
```

### Publishing
```bash
python scripts/get-config.py publishing.group_id                # com.compiledplatforms.kmp
python scripts/get-config.py publishing.repositories.maven_central.enabled  # true
```

### Documentation
```bash
python scripts/get-config.py documentation.github_pages.enabled  # false
python scripts/get-config.py documentation.local_port            # 8000
```

## Benefits

### 1. **Single Source of Truth**
- Change Java version once, updates everywhere
- No more hunting for hardcoded values
- Consistency across all tooling

### 2. **Self-Documenting**
- Configuration file is readable and commented
- Easy to understand project setup at a glance
- New contributors know exactly what's configured

### 3. **Easy Updates**
- Update tool versions in one place
- Enable/disable features with a boolean flag
- Adjust CI strategy without touching workflow files

### 4. **Local Development**
- Scripts can read the same config as CI
- Consistent behavior between local and remote
- Easy to test changes before pushing

### 5. **Template Reusability**
- Fork the template and update `project.yml`
- Most workflows don't need modification
- Project-specific values are centralized

## Example: Updating Java Version

**Before (multiple files to change):**
```
.github/workflows/build.yml:        java-version: '17'
.github/workflows/docs.yml:         java-version: '17'
README.md:                          Java 17+
docs/docs/getting-started.md:      Java 17 or higher
build.gradle.kts:                   JavaVersion.VERSION_17
```

**After (single change):**
```yaml
# project.yml
versions:
  java: '21'  # ✅ Changed once
```

All workflows and scripts automatically use Java 21.

## Example: Disabling GitHub Pages

**Before:** Comment out workflow triggers, add conditions, etc.

**After:**
```yaml
# project.yml
documentation:
  github_pages:
    enabled: false  # ✅ One change
```

Docs workflow automatically skips when disabled.

## Example: Branch-Specific CI Control

Control which branches run CI workflows:

### Option 1: Specific Branches Only
```yaml
# project.yml
ci:
  enabled_branches: [main]  # Only run on main
```

### Option 2: Multiple Branches
```yaml
# project.yml
ci:
  enabled_branches: [main, develop]  # Run on main and develop
```

### Option 3: All Branches
```yaml
# project.yml
ci:
  enabled_branches: all  # Run on every branch
```

### Option 4: Disable Completely
```yaml
# project.yml
ci:
  enabled_branches: false  # Don't run on any branch
```

**Use Cases:**
- **Single branch (`[main]`)**: Production-only testing
- **Main + develop**: Test staging and production
- **All branches**: Comprehensive testing on every branch
- **Disabled (`false`)**: Template forks, major refactoring, or save CI minutes

**How it works:**
- ✅ Workflows check the current branch automatically
- ✅ PRs check against the base branch (where PR will merge)
- ✅ Disabled jobs show as "successful" (won't block PRs)

## Best Practices

### 1. **Always Use Config Values**
Don't hardcode values in workflows or scripts - read from `project.yml`.

### 2. **Document Changes**
Add comments in `project.yml` explaining why certain values are set.

### 3. **Validate Changes**
After updating `project.yml`, test locally:
```bash
./scripts/get-config.sh <your.path>
```

### 4. **Keep Backwards Compatible**
If you add new keys, provide sensible defaults in scripts.

### 5. **Version Control**
Always commit `project.yml` changes with descriptive messages.

## Requirements

The helper script requires Python 3.6+ and PyYAML:

```bash
pip install pyyaml
```

Or install from project requirements (if available):
```bash
pip install -r requirements.txt
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"
Install PyYAML:
```bash
pip install pyyaml
```

### "Error reading project.yml"
Ensure the file exists in the project root and has valid YAML syntax.

### "Error: Path 'xxx' not found"
The path doesn't exist in `project.yml`. Check the structure:
```bash
python scripts/get-config.py project  # Print project section
```

### "Workflow fails to load config"
GitHub Actions installs yq automatically in the `config` job. Check the job logs for yq-related errors.

## Migration Guide

To migrate an existing hardcoded value to `project.yml`:

1. **Add to config:**
   ```yaml
   # project.yml
   my_section:
     my_value: "some-value"
   ```

2. **Update workflow:**
   ```yaml
   # Add to config job outputs
   my-value: ${{ steps.load.outputs.my-value }}
   
   # Add to load step
   echo "my-value=$(yq '.my_section.my_value' project.yml)" >> $GITHUB_OUTPUT
   
   # Use in other jobs
   needs: config
   run: echo "${{ needs.config.outputs.my-value }}"
   ```

3. **Update scripts:**
   ```bash
   MY_VALUE=$(python scripts/get-config.py my_section.my_value)
   ```

4. **Remove hardcoded value** from original location.

## Future Enhancements

Potential additions to the configuration system:

- [ ] Gradle plugin to read `project.yml` directly in `build.gradle.kts`
- [ ] Pre-commit hook to validate `project.yml` schema
- [ ] Auto-generate documentation from config values
- [ ] IDE integration (code completion, validation)
- [ ] Config value interpolation (e.g., `${versions.kotlin}` in other values)

## See Also

- `project.yml` - The configuration file itself
- `scripts/get-config.py` - Helper script for reading config
- `.github/workflows/build.yml` - Example workflow using config
- `.github/workflows/docs.yml` - Another example with conditional execution
