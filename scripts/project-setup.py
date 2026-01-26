#!/usr/bin/env python3
"""
Kotlin Multiplatform Library Template Setup Script
Reads configuration from project.yml and updates all project files
"""

import sys
import re


def get_input(prompt: str, required: bool = True) -> str:
    """Get input from user with optional validation."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("❌ Error: This field is required. Please enter a value.")


def parse_domain(domain: str) -> str:
    """
    Parse domain from various formats and return clean domain name.
    
    Accepts formats:
    - https://mycompany.com
    - http://www.mycompany.com
    - mycompany.com
    - www.mycompany.com
    
    Returns: mycompany.com (clean domain without protocol or www)
    """
    # Remove protocol
    domain = re.sub(r'^https?://', '', domain)
    
    # Remove www.
    domain = re.sub(r'^www\.', '', domain)
    
    # Remove trailing slash
    domain = domain.rstrip('/')
    
    # Remove any path
    domain = domain.split('/')[0]
    
    # Basic validation - should have at least one dot
    if '.' not in domain:
        raise ValueError("Invalid domain format - must include TLD (e.g., .com, .io)")
    
    return domain.lower()


def domain_to_group_id(domain: str) -> str:
    """
    Convert domain to reverse notation group ID.
    
    Examples:
    - mycompany.com → com.mycompany
    - stripe.io → io.stripe
    - touchlab.co → co.touchlab
    """
    parts = domain.split('.')
    return '.'.join(reversed(parts))


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Parse GitHub URL to extract organization and repository name.
    
    Accepts formats:
    - https://github.com/org/repo
    - https://github.com/org/repo.git
    - git@github.com:org/repo.git
    - org/repo
    
    Returns: (organization, repository)
    """
    # Remove .git suffix if present
    url = url.rstrip('/').replace('.git', '')
    
    # Try HTTPS format
    match = re.search(r'github\.com[:/]([^/]+)/([^/]+)', url)
    if match:
        return match.group(1), match.group(2)
    
    # Try simple org/repo format
    match = re.match(r'^([^/]+)/([^/]+)$', url)
    if match:
        return match.group(1), match.group(2)
    
    raise ValueError("Invalid GitHub URL format")


def main():
    """Main setup function."""
    print("🚀 Kotlin Multiplatform Library Template Setup")
    print("=" * 50)
    print()
    
    # Determine project type
    print("What type of project is this?")
    print()
    print("1. Personal project (GitHub username)")
    print("2. Company project (with owned domain)")
    print("3. Open source organization")
    print()
    
    while True:
        choice = get_input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            break
        print("❌ Please enter 1, 2, or 3")
        print()
    
    project_type = {
        '1': 'personal',
        '2': 'company',
        '3': 'organization'
    }[choice]
    
    print()
    print(f"✓ Project type: {project_type}")
    
    # Ask for domain if company project
    domain = None
    if project_type == 'company':
        print()
        print("Enter your company domain (e.g., mycompany.com):")
        
        while True:
            domain_input = get_input("Domain: ")
            try:
                domain = parse_domain(domain_input)
                print(f"✓ Domain: {domain}")
                break
            except ValueError as e:
                print(f"❌ Error: {e}")
                print("Please enter a valid domain (e.g., mycompany.com, stripe.io)")
    
    print()
    
    # Get GitHub URL
    print("Next, let's get your GitHub repository information:")
    print()
    
    while True:
        github_url = get_input("Enter your GitHub repository URL: ")
        
        try:
            organization, repository = parse_github_url(github_url)
            print()
            print(f"✓ Organization: {organization}")
            print(f"✓ Repository: {repository}")
            print()
            
            confirm = input("Is this correct? (y/n): ").strip().lower()
            if confirm == 'y':
                break
            print()
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("Please use format: https://github.com/org/repo or org/repo")
            print()
    
    # Get project name (default to repository name)
    print()
    project_name_input = input(f"Project name [{repository}]: ").strip()
    project_name = project_name_input if project_name_input else repository
    
    if project_name != repository:
        print(f"✓ Using custom project name: {project_name}")
    else:
        print(f"✓ Using repository name: {project_name}")
    
    # Get Maven Group ID (with suggestions based on project type)
    print()
    print("Maven Group ID (reverse domain notation):")
    
    # Suggest group_id based on project type
    if project_type == 'personal':
        suggestion = f"io.github.{organization.lower()}"
        print(f"  Suggestion for personal project: {suggestion}")
    elif project_type == 'company':
        if domain:
            suggestion = domain_to_group_id(domain)
            print(f"  Based on your domain: {suggestion}")
        else:
            print(f"  Example: com.yourcompany.kmp")
            suggestion = ""
    else:  # organization
        # Try to make a suggestion from org name
        org_lower = organization.lower().replace('-', '')
        suggestion = f"org.{org_lower}.libs"
        print(f"  Suggestion for organization: {suggestion}")
    
    print("  Format: reverse.domain.notation (no hyphens)")
    print()
    
    if suggestion:
        group_id_input = input(f"Maven Group ID [{suggestion}]: ").strip()
        group_id = group_id_input if group_id_input else suggestion
    else:
        group_id = get_input("Maven Group ID: ", required=True)
    
    print(f"✓ Maven Group ID: {group_id}")
    
    # Get Android namespace prefix (default to group_id)
    print()
    namespace_input = input(f"Android namespace [{group_id}]: ").strip()
    namespace_prefix = namespace_input if namespace_input else group_id
    
    if namespace_prefix != group_id:
        print(f"⚠️  Warning: namespace_prefix differs from group_id!")
        print(f"   Group ID: {group_id}")
        print(f"   Namespace: {namespace_prefix}")
    else:
        print(f"✓ Android namespace: {namespace_prefix}")
    
    print()
    print("=" * 50)
    print("📋 Configuration Summary")
    print("=" * 50)
    print()
    print(f"Project Type:       {project_type}")
    if domain:
        print(f"Company Domain:     {domain}")
    print(f"Organization:       {organization}")
    print(f"Repository:         {repository}")
    print(f"Project Name:       {project_name}")
    print(f"Maven Group ID:     {group_id}")
    print(f"Android Namespace:  {namespace_prefix}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("❌ Setup cancelled by user")
        sys.exit(1)
