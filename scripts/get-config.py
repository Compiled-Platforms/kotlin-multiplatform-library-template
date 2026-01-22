#!/usr/bin/env python3
"""
Helper script to read values from project.yml
Usage: python3 scripts/get-config.py <yaml.path>
Example: python3 scripts/get-config.py versions.java
"""

import sys
import yaml
from pathlib import Path


def get_nested_value(data: dict, path: str):
    """Get a nested value from a dictionary using dot notation."""
    keys = path.split('.')
    value = data
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return None
        else:
            return None
    
    return value


def format_output(value):
    """Format the output value for display."""
    if isinstance(value, list):
        return '\n'.join(f"- {item}" for item in value)
    elif isinstance(value, dict):
        return yaml.dump(value, default_flow_style=False, sort_keys=False).strip()
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/get-config.py <yaml.path>", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python3 scripts/get-config.py versions.java", file=sys.stderr)
        print("  python3 scripts/get-config.py ci.runners.primary", file=sys.stderr)
        print("  python3 scripts/get-config.py platforms.enabled", file=sys.stderr)
        sys.exit(1)
    
    # Find project root and config file
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    config_file = project_root / 'project.yml'
    
    if not config_file.exists():
        print(f"Error: project.yml not found at {config_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load config
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing project.yml: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Get the requested value
    path = sys.argv[1]
    value = get_nested_value(config, path)
    
    if value is None:
        print(f"Error: Path '{path}' not found in project.yml", file=sys.stderr)
        sys.exit(1)
    
    # Output the value
    print(format_output(value))


if __name__ == '__main__':
    main()
