#!/usr/bin/env python3

"""
Kotlin Multiplatform Library Template Setup Script
This script helps you customize the template with your own values
"""

import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color


def print_error(message: str) -> None:
    """Print error message in red"""
    print(f"{Colors.RED}{message}{Colors.NC}")


def print_success(message: str) -> None:
    """Print success message in green"""
    print(f"{Colors.GREEN}{message}{Colors.NC}")


def print_warning(message: str) -> None:
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}{message}{Colors.NC}")


def get_input(prompt: str) -> str:
    """Get input from user with validation"""
    value = input(prompt).strip()
    if not value:
        print_error("Error: Value cannot be empty")
        sys.exit(1)
    return value


def replace_in_file(file_path: Path, old: str, new: str) -> None:
    """Replace text in a file"""
    if not file_path.exists():
        return
    
    try:
        content = file_path.read_text(encoding='utf-8')
        content = content.replace(old, new)
        file_path.write_text(content, encoding='utf-8')
    except Exception as e:
        print_error(f"Error processing {file_path}: {e}")


def find_files_with_pattern(pattern: str, extensions: list[str], exclude_dirs: list[str]) -> list[Path]:
    """Find all files containing a pattern"""
    files_with_pattern = []
    
    for ext in extensions:
        for file_path in Path('.').rglob(f'*{ext}'):
            # Check if file is in excluded directory
            if any(excluded in str(file_path) for excluded in exclude_dirs):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                if pattern in content:
                    files_with_pattern.append(file_path)
            except Exception:
                # Skip files that can't be read
                continue
    
    return files_with_pattern


def main():
    """Main setup function"""
    print("🚀 Kotlin Multiplatform Library Template Setup")
    print("=" * 46)
    print()
    
    # Check if we're in the right directory
    if not Path('settings.gradle.kts').exists():
        print_error("Error: This script must be run from the root of the project")
        sys.exit(1)
    
    # Check if template has already been set up
    template_file = Path('.template')
    if template_file.exists():
        content = template_file.read_text().strip()
        if content == 'configured':
            print_warning("Note: Template has already been configured once")
            response = input("Do you want to reconfigure? (y/n): ").strip().lower()
            if response != 'y':
                print("Setup cancelled")
                sys.exit(0)
    
    print()
    print("Please provide the following information:")
    print()
    
    # Get user input
    group_id = get_input("📦 Enter your Maven group ID (e.g., com.example.libraries): ")
    project_name = get_input("📝 Enter your project name (e.g., my-kmp-libraries): ")
    github_org = get_input("🐙 Enter your GitHub username or organization: ")
    developer_name = get_input("👤 Enter developer name (for POM files): ")
    developer_username = get_input("🔗 Enter developer GitHub username: ")
    
    # Show summary
    print()
    print("Summary of changes:")
    print("-" * 19)
    print(f"Group ID: com.compiledplatforms.kmp.library → {group_id}")
    print(f"Project Name: kotlin-multiplatform-library-template → {project_name}")
    print(f"GitHub Org: compiledplatforms → {github_org}")
    print(f"Developer Name: Developer Name → {developer_name}")
    print(f"Developer Username: developer → {developer_username}")
    print()
    
    response = input("Proceed with these changes? (y/n): ").strip().lower()
    if response != 'y':
        print("Setup cancelled")
        sys.exit(0)
    
    print()
    print("🔧 Applying changes...")
    
    # Create backup
    print("📋 Creating backup...")
    backup_dir = Path(f'.setup-backup-{int(datetime.now().timestamp())}')
    backup_dir.mkdir(exist_ok=True)
    
    items_to_backup = ['settings.gradle.kts', 'README.md', 'buildSrc', 
                       'libraries', 'bom', 'samples', 'scripts']
    for item in items_to_backup:
        item_path = Path(item)
        if item_path.exists():
            try:
                if item_path.is_dir():
                    shutil.copytree(item_path, backup_dir / item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item_path, backup_dir / item)
            except Exception:
                pass  # Continue even if some items fail to backup
    
    exclude_dirs = ['build', '.gradle', '.git', '.setup-backup-']
    
    # Replace group ID
    print("📦 Updating group ID...")
    extensions = ['.gradle.kts', '.kt', '.md', '.sh', '.py']
    files = find_files_with_pattern('com.compiledplatforms.kmp.library', extensions, exclude_dirs)
    for file_path in files:
        replace_in_file(file_path, 'com.compiledplatforms.kmp.library', group_id)
    
    # Replace project name
    print("📝 Updating project name...")
    replace_in_file(Path('settings.gradle.kts'), 
                   'kotlin-multiplatform-library-template', project_name)
    
    extensions = ['.md', '.gradle.kts']
    files = find_files_with_pattern('kotlin-multiplatform-library-template', extensions, exclude_dirs)
    for file_path in files:
        replace_in_file(file_path, 'kotlin-multiplatform-library-template', project_name)
    
    # Replace GitHub org
    print("🐙 Updating GitHub URLs...")
    extensions = ['.gradle.kts', '.md']
    files = find_files_with_pattern('compiledplatforms', extensions, exclude_dirs)
    for file_path in files:
        replace_in_file(file_path, 'compiledplatforms', github_org)
    
    # Replace developer info
    print("👤 Updating developer information...")
    extensions = ['.gradle.kts']
    files = find_files_with_pattern('Developer Name', extensions, exclude_dirs)
    for file_path in files:
        replace_in_file(file_path, 'Developer Name', developer_name)
    
    files = find_files_with_pattern('id = "developer"', extensions, exclude_dirs)
    for file_path in files:
        replace_in_file(file_path, 'id = "developer"', f'id = "{developer_username}"')
        replace_in_file(file_path, 'url = "https://github.com/developer"', 
                       f'url = "https://github.com/{developer_username}"')
    
    # Update namespace in convention plugin
    print("🔧 Updating Android namespaces...")
    for file_path in Path('buildSrc').rglob('*.gradle.kts'):
        if 'build' not in str(file_path):
            replace_in_file(file_path, 'com.compiledplatforms.kmp.library', group_id)
    
    # Mark as configured
    template_file.write_text('configured\n')
    
    print()
    print_success("✅ Setup complete!")
    print()
    print("Next steps:")
    print("1. Review the changes with: git diff")
    print("2. Test the build: ./gradlew build")
    print("3. Remove the example library if not needed: rm -rf libraries/example-library")
    print("4. Create your first library: python scripts/create-library.py <library-name>")
    print("5. Update README.md with your project details")
    print()
    print(f"Backup saved to: {backup_dir}")
    print("You can remove it after verifying everything works correctly.")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_error("Setup cancelled by user")
        sys.exit(1)
