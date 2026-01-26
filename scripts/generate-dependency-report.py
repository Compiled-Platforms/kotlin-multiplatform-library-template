#!/usr/bin/env python3
"""
Generate a markdown report of all dependencies from gradle/libs.versions.toml

Usage:
    python3 scripts/generate-dependency-report.py
    python3 scripts/generate-dependency-report.py --output docs/DEPENDENCIES.md
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # pip install tomli
    except ImportError:
        print("Error: tomli library required for Python < 3.11")
        print("Install with: pip install tomli")
        sys.exit(1)


def load_version_catalog(toml_path: Path) -> dict:
    """Load and parse the version catalog TOML file."""
    with open(toml_path, "rb") as f:
        return tomllib.load(f)


def generate_markdown(catalog: dict) -> str:
    """Generate a markdown report from the version catalog."""
    lines = [
        "# Dependency Report",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This document lists all dependencies defined in `gradle/libs.versions.toml`.",
        "",
    ]

    # Versions section
    if "versions" in catalog:
        lines.extend([
            "## Versions",
            "",
            "| Name | Version |",
            "|------|---------|",
        ])
        
        versions = catalog["versions"]
        for name, version in sorted(versions.items()):
            # Format name for display
            display_name = name.replace("-", " ").replace("_", " ").title()
            lines.append(f"| **{display_name}** | `{version}` |")
        
        lines.append("")

    # Libraries section
    if "libraries" in catalog:
        lines.extend([
            "## Libraries",
            "",
            "| Library | Module | Version |",
            "|---------|--------|---------|",
        ])
        
        libraries = catalog["libraries"]
        for name, config in sorted(libraries.items()):
            if isinstance(config, dict):
                module = config.get("module", "N/A")
                
                # Get version - either direct or referenced
                if "version" in config:
                    if isinstance(config["version"], dict):
                        version_ref = config["version"].get("ref", "")
                        version = f"→ `{version_ref}`"
                    else:
                        version = f"`{config['version']}`"
                else:
                    version = "N/A"
                
                # Format name for display
                display_name = name.replace("-", " ").replace("_", " ").title()
                lines.append(f"| **{display_name}** | `{module}` | {version} |")
        
        lines.append("")

    # Plugins section
    if "plugins" in catalog:
        lines.extend([
            "## Plugins",
            "",
            "| Plugin | ID | Version |",
            "|--------|----|---------| ",
        ])
        
        plugins = catalog["plugins"]
        for name, config in sorted(plugins.items()):
            if isinstance(config, dict):
                plugin_id = config.get("id", "N/A")
                
                # Get version - either direct or referenced
                if "version" in config:
                    if isinstance(config["version"], dict):
                        version_ref = config["version"].get("ref", "")
                        version = f"→ `{version_ref}`"
                    else:
                        version = f"`{config['version']}`"
                else:
                    version = "N/A"
                
                # Format name for display
                display_name = name.replace("-", " ").replace("_", " ").title()
                lines.append(f"| **{display_name}** | `{plugin_id}` | {version} |")
        
        lines.append("")

    # Add footer
    lines.extend([
        "---",
        "",
        "## Version References",
        "",
        "Entries marked with `→ version-name` reference the version defined in the `[versions]` section.",
        "",
        "## Updating Dependencies",
        "",
        "See [Dependency Updates](docs/docs/development/dependency-updates.md) for information on keeping dependencies up-to-date.",
        "",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate dependency report from version catalog"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("DEPENDENCIES.md"),
        help="Output markdown file (default: DEPENDENCIES.md)",
    )
    parser.add_argument(
        "--toml",
        "-t",
        type=Path,
        default=Path("gradle/libs.versions.toml"),
        help="Version catalog TOML file (default: gradle/libs.versions.toml)",
    )
    
    args = parser.parse_args()

    # Check if TOML file exists
    if not args.toml.exists():
        print(f"Error: Version catalog not found at {args.toml}", file=sys.stderr)
        sys.exit(1)

    try:
        # Load version catalog
        print(f"Reading version catalog from {args.toml}...")
        catalog = load_version_catalog(args.toml)

        # Generate markdown
        print("Generating dependency report...")
        markdown = generate_markdown(catalog)

        # Write output
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown)
        
        print(f"✅ Dependency report generated: {args.output}")
        
        # Print summary
        version_count = len(catalog.get("versions", {}))
        library_count = len(catalog.get("libraries", {}))
        plugin_count = len(catalog.get("plugins", {}))
        
        print(f"   • {version_count} versions")
        print(f"   • {library_count} libraries")
        print(f"   • {plugin_count} plugins")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
