#!/usr/bin/env python3
"""
Parse version information from gradle/libs.versions.toml
"""

import sys
import os
import argparse

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for older Python


def parse_toml(file_path):
    """Parse TOML file."""
    with open(file_path, 'rb') as f:
        return tomllib.load(f)


def set_output(name, value):
    """Set GitHub Actions output."""
    print(f"::set-output name={name}::{value}")


def main():
    parser = argparse.ArgumentParser(description='Parse versions from TOML')
    parser.add_argument('--toml-file', default='gradle/libs.versions.toml',
                        help='Path to libs.versions.toml')
    args = parser.parse_args()

    try:
        # Parse libs.versions.toml - single source of truth for all versions
        toml_data = parse_toml(args.toml_file)
        versions = toml_data.get('versions', {})
        
        # Extract versions (with defaults as fallback)
        java_ci_version = versions.get('java-ci', '17')
        python_ci_version = versions.get('python-ci', '3.11')

        # Set outputs (GitHub Actions needs CI versions)
        set_output('java-version', java_ci_version)
        set_output('python-version', python_ci_version)

        # Log parsed versions
        print("\n📦 Parsed Versions from libs.versions.toml:")
        print(f"  Java (CI):    {java_ci_version}")
        print(f"  Python (CI):  {python_ci_version}")

    except FileNotFoundError:
        print(f"❌ Error: {args.toml_file} not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error parsing versions: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
