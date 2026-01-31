#!/usr/bin/env python3
"""
Publishing Configuration Helper

Reads and validates publishing configuration from project.yml.
Used by convention plugins and CI/CD workflows to configure publishing targets.

Usage:
    python3 scripts/get-publishing-config.py --list-enabled
    python3 scripts/get-publishing-config.py --repository maven_central
    python3 scripts/get-publishing-config.py --validate
"""

import sys
import yaml
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class PublishingConfig:
    """Publishing configuration reader and validator."""
    
    REQUIRED_SECRETS = {
        'maven_central': ['MAVEN_CENTRAL_USERNAME', 'MAVEN_CENTRAL_PASSWORD'],
        'github_packages': ['GITHUB_TOKEN'],
        'custom_maven': ['CUSTOM_MAVEN_USERNAME', 'CUSTOM_MAVEN_PASSWORD'],
        'jfrog': ['JFROG_USERNAME', 'JFROG_PASSWORD'],
        'cloudsmith': ['CLOUDSMITH_API_KEY'],
    }
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()
        self.publishing = self.config.get('publishing', {})
        
    def _load_config(self) -> Dict:
        """Load and parse project.yml."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config: {e}")
    
    def is_enabled(self) -> bool:
        """Check if publishing is globally enabled."""
        return self.publishing.get('enabled', False)
    
    def get_enabled_repositories(self) -> List[str]:
        """Get list of enabled repository names."""
        if not self.is_enabled():
            return []
        
        repos = self.publishing.get('repositories', {})
        return [name for name, config in repos.items() 
                if isinstance(config, dict) and config.get('enabled', False)]
    
    def get_repository_config(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific repository."""
        repos = self.publishing.get('repositories', {})
        config = repos.get(repo_name)
        
        if not isinstance(config, dict):
            return None
        
        if not config.get('enabled', False):
            return None
        
        return config
    
    def get_group_id(self) -> str:
        """Get Maven group ID."""
        return self.publishing.get('group_id', '')
    
    def get_artifact_prefix(self) -> str:
        """Get artifact ID prefix."""
        return self.publishing.get('artifact_id_prefix', '')
    
    def is_signing_required(self) -> bool:
        """Check if artifact signing is required."""
        signing = self.publishing.get('signing', {})
        return signing.get('required', True)
    
    def uses_secret_signing_key(self) -> bool:
        """Check if signing key should come from secrets."""
        signing = self.publishing.get('signing', {})
        return signing.get('key_from_secret', True)
    
    def get_required_secrets(self, repo_name: str) -> List[str]:
        """Get list of required secrets for a repository."""
        secrets = self.REQUIRED_SECRETS.get(repo_name, []).copy()
        
        if self.is_signing_required() and self.uses_secret_signing_key():
            secrets.extend(['SIGNING_KEY', 'SIGNING_PASSWORD'])
        
        return secrets
    
    def validate(self) -> List[str]:
        """Validate publishing configuration. Returns list of errors."""
        errors = []
        
        if not self.is_enabled():
            return []  # Not an error, just disabled
        
        # Validate group_id
        group_id = self.get_group_id()
        if not group_id:
            errors.append("publishing.group_id is required")
        elif '-' in group_id:
            errors.append(f"publishing.group_id cannot contain hyphens: {group_id}")
        
        # Check at least one repository is enabled
        enabled_repos = self.get_enabled_repositories()
        if not enabled_repos:
            errors.append("No repositories enabled in publishing.repositories")
        
        # Validate each enabled repository
        for repo_name in enabled_repos:
            repo_config = self.get_repository_config(repo_name)
            repo_errors = self._validate_repository(repo_name, repo_config)
            errors.extend(repo_errors)
        
        return errors
    
    def _validate_repository(self, name: str, config: Dict) -> List[str]:
        """Validate a specific repository configuration."""
        errors = []
        prefix = f"publishing.repositories.{name}"
        
        if name == 'maven_central':
            # Maven Central requires auto_release setting
            if 'auto_release' not in config:
                errors.append(f"{prefix}.auto_release is required (true or false)")
        
        elif name == 'github_packages':
            # GitHub Packages requires owner and repository
            if not config.get('owner'):
                errors.append(f"{prefix}.owner is required")
            if not config.get('repository'):
                errors.append(f"{prefix}.repository is required")
        
        elif name == 'custom_maven':
            # Custom Maven requires URLs
            if not config.get('releases_url'):
                errors.append(f"{prefix}.releases_url is required")
            if not config.get('snapshots_url'):
                errors.append(f"{prefix}.snapshots_url is required")
        
        elif name == 'jfrog':
            # JFrog requires URL
            if not config.get('url'):
                errors.append(f"{prefix}.url is required")
        
        elif name == 'cloudsmith':
            # CloudSmith requires owner and repository
            if not config.get('owner'):
                errors.append(f"{prefix}.owner is required")
            if not config.get('repository'):
                errors.append(f"{prefix}.repository is required")
        
        return errors
    
    def to_gradle_properties(self) -> str:
        """Generate gradle.properties format output."""
        lines = []
        
        if not self.is_enabled():
            return "# Publishing is disabled"
        
        lines.append("# Publishing Configuration (from project.yml)")
        lines.append(f"publishing.enabled=true")
        lines.append(f"publishing.groupId={self.get_group_id()}")
        
        prefix = self.get_artifact_prefix()
        if prefix:
            lines.append(f"publishing.artifactPrefix={prefix}")
        
        lines.append(f"publishing.signing.required={str(self.is_signing_required()).lower()}")
        
        # Repository-specific properties
        for repo_name in self.get_enabled_repositories():
            config = self.get_repository_config(repo_name)
            lines.append(f"\npublishing.{repo_name}.enabled=true")
            
            if repo_name == 'maven_central':
                auto_release = config.get('auto_release', False)
                lines.append(f"publishing.mavenCentral.autoRelease={str(auto_release).lower()}")
            
            elif repo_name == 'github_packages':
                lines.append(f"publishing.githubPackages.owner={config['owner']}")
                lines.append(f"publishing.githubPackages.repository={config['repository']}")
            
            elif repo_name == 'custom_maven':
                lines.append(f"publishing.customMaven.name={config.get('name', 'Custom Maven')}")
                lines.append(f"publishing.customMaven.releasesUrl={config['releases_url']}")
                lines.append(f"publishing.customMaven.snapshotsUrl={config['snapshots_url']}")
            
            elif repo_name == 'jfrog':
                lines.append(f"publishing.jfrog.url={config['url']}")
            
            elif repo_name == 'cloudsmith':
                lines.append(f"publishing.cloudsmith.owner={config['owner']}")
                lines.append(f"publishing.cloudsmith.repository={config['repository']}")
        
        return '\n'.join(lines)
    
    def to_json(self) -> str:
        """Export configuration as JSON."""
        data = {
            'enabled': self.is_enabled(),
            'group_id': self.get_group_id(),
            'artifact_prefix': self.get_artifact_prefix(),
            'signing_required': self.is_signing_required(),
            'enabled_repositories': self.get_enabled_repositories(),
            'repositories': {}
        }
        
        for repo_name in self.get_enabled_repositories():
            config = self.get_repository_config(repo_name)
            data['repositories'][repo_name] = config
        
        return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Read and validate publishing configuration from project.yml'
    )
    parser.add_argument(
        '--list-enabled',
        action='store_true',
        help='List enabled repositories'
    )
    parser.add_argument(
        '--repository',
        type=str,
        help='Get configuration for specific repository'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate configuration and report errors'
    )
    parser.add_argument(
        '--gradle-properties',
        action='store_true',
        help='Output as gradle.properties format'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--required-secrets',
        type=str,
        help='List required secrets for a repository'
    )
    
    args = parser.parse_args()
    
    # Find project root and config file
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    config_file = project_root / 'project.yml'
    
    try:
        config = PublishingConfig(config_file)
        
        if args.list_enabled:
            repos = config.get_enabled_repositories()
            if repos:
                for repo in repos:
                    print(repo)
            else:
                print("No repositories enabled", file=sys.stderr)
                sys.exit(1)
        
        elif args.repository:
            repo_config = config.get_repository_config(args.repository)
            if repo_config:
                print(yaml.dump({args.repository: repo_config}, default_flow_style=False))
            else:
                print(f"Repository '{args.repository}' not found or not enabled", file=sys.stderr)
                sys.exit(1)
        
        elif args.validate:
            errors = config.validate()
            if errors:
                print("Validation errors:", file=sys.stderr)
                for error in errors:
                    print(f"  - {error}", file=sys.stderr)
                sys.exit(1)
            else:
                print("✓ Publishing configuration is valid")
        
        elif args.gradle_properties:
            print(config.to_gradle_properties())
        
        elif args.json:
            print(config.to_json())
        
        elif args.required_secrets:
            secrets = config.get_required_secrets(args.required_secrets)
            if secrets:
                for secret in secrets:
                    print(secret)
            else:
                print(f"Unknown repository: {args.required_secrets}", file=sys.stderr)
                sys.exit(1)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
