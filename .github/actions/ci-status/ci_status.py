#!/usr/bin/env python3
"""
CI Status Checker for KMP Template

Reads project.yml configuration and determines if CI should run
for the current branch. Creates GitHub Actions annotations and
sets output variables.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Any, Dict, Union


def load_config(config_path: str) -> Dict[str, Any]:
    """Load and parse the project.yml configuration file."""
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def get_current_branch() -> str:
    """Get the current branch name from GitHub context."""
    event_name = os.environ.get('GITHUB_EVENT_NAME', '')
    
    if event_name == 'pull_request':
        # For PRs, check against base branch (where it will merge)
        return os.environ.get('GITHUB_BASE_REF', 'main')
    else:
        return os.environ.get('GITHUB_REF_NAME', 'main')


def check_branch_enabled(
    branch: str,
    enabled_branches: Union[bool, str, list]
) -> bool:
    """
    Check if CI is enabled for the given branch.
    
    Args:
        branch: Current branch name
        enabled_branches: Configuration value (false, "all", or list of branches)
    
    Returns:
        True if CI should run, False otherwise
    """
    if enabled_branches is False or enabled_branches == 'false':
        return False
    
    if enabled_branches == 'all':
        return True
    
    if isinstance(enabled_branches, list):
        return branch in enabled_branches
    
    # Default to disabled if config is invalid
    return False


def create_annotation(
    level: str,
    title: str,
    message: str
) -> str:
    """Create a GitHub Actions annotation."""
    return f"::{level} title={title}::{message}"


def format_list(value: Any) -> str:
    """Format a list or other value for output."""
    if isinstance(value, list):
        return ','.join(str(x) for x in value)
    return str(value)


def set_output(name: str, value: Any):
    """Set a GitHub Actions output variable."""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"{name}={value}\n")
    else:
        # Fallback for local testing
        print(f"OUTPUT: {name}={value}")


def main():
    """Main execution function."""
    try:
        # Load configuration
        config_file = os.environ.get('CONFIG_FILE', 'project.yml')
        config = load_config(config_file)
        
        # Get current branch
        current_branch = get_current_branch()
        
        # Extract configuration values
        ci_config = config.get('ci', {})
        docs_config = config.get('documentation', {})
        
        enabled_branches = ci_config.get('enabled_branches', False)
        ci_enabled = check_branch_enabled(current_branch, enabled_branches)
        
        # Set all outputs
        set_output('ci-enabled', str(ci_enabled).lower())
        set_output('current-branch', current_branch)
        set_output('enabled-branches', format_list(enabled_branches))
        set_output('runner', ci_config.get('runners', {}).get('primary', 'ubuntu-latest'))
        
        # Format gradle flags
        gradle_flags = ci_config.get('gradle_flags', [])
        if isinstance(gradle_flags, list):
            gradle_flags_str = ' '.join(gradle_flags)
        else:
            gradle_flags_str = str(gradle_flags)
        set_output('gradle-flags', gradle_flags_str)
        
        set_output('kotlin-native-cache', str(ci_config.get('caching', {}).get('kotlin_native', True)).lower())
        set_output('pages-enabled', str(docs_config.get('github_pages', {}).get('enabled', False)).lower())
        
        # Create status output
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 CI Configuration Status")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Current branch:    {current_branch}")
        print(f"Enabled branches:  {enabled_branches}")
        print(f"CI enabled:        {ci_enabled}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Create annotation
        if ci_enabled:
            annotation = create_annotation(
                'notice',
                'CI Enabled',
                f"CI will run for branch '{current_branch}'"
            )
            print(annotation)
            print(f"✅ CI will RUN for branch '{current_branch}'")
        else:
            annotation = create_annotation(
                'warning',
                'CI Skipped',
                f"CI disabled for branch '{current_branch}'. To enable, set ci.enabled_branches: [{current_branch}] in project.yml"
            )
            print(annotation)
            print(f"⏭️  CI will be SKIPPED (disabled for branch '{current_branch}')")
            print("")
            print("To enable CI for this branch, update project.yml:")
            print("  ci:")
            print(f"    enabled_branches: [{current_branch}]")
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return 0
        
    except Exception as e:
        error_msg = f"Error checking CI status: {str(e)}"
        print(f"::error title=CI Status Check Failed::{error_msg}", file=sys.stderr)
        print(error_msg, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
