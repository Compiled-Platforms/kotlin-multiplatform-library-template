#!/bin/bash

# Kotlin Multiplatform Library Template Setup Script
# This script helps you customize the template with your own values

set -e

echo "🚀 Kotlin Multiplatform Library Template Setup"
echo "=============================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "settings.gradle.kts" ]; then
    echo -e "${RED}Error: This script must be run from the root of the project${NC}"
    exit 1
fi

# Check if template has already been set up
if [ ! -f ".template" ]; then
    echo -e "${YELLOW}Warning: This appears to be a fresh template${NC}"
else
    echo -e "${YELLOW}Note: Template has already been configured once${NC}"
    read -p "Do you want to reconfigure? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled"
        exit 0
    fi
fi

echo ""
echo "Please provide the following information:"
echo ""

# Get group ID
read -p "📦 Enter your Maven group ID (e.g., com.example.libraries): " GROUP_ID
if [ -z "$GROUP_ID" ]; then
    echo -e "${RED}Error: Group ID cannot be empty${NC}"
    exit 1
fi

# Get project name
read -p "📝 Enter your project name (e.g., my-kmp-libraries): " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: Project name cannot be empty${NC}"
    exit 1
fi

# Get GitHub org/user
read -p "🐙 Enter your GitHub username or organization: " GITHUB_ORG
if [ -z "$GITHUB_ORG" ]; then
    echo -e "${RED}Error: GitHub username/organization cannot be empty${NC}"
    exit 1
fi

# Get developer info
read -p "👤 Enter developer name (for POM files): " DEVELOPER_NAME
if [ -z "$DEVELOPER_NAME" ]; then
    echo -e "${RED}Error: Developer name cannot be empty${NC}"
    exit 1
fi

read -p "🔗 Enter developer GitHub username: " DEVELOPER_USERNAME
if [ -z "$DEVELOPER_USERNAME" ]; then
    echo -e "${RED}Error: Developer username cannot be empty${NC}"
    exit 1
fi

echo ""
echo "Summary of changes:"
echo "-------------------"
echo "Group ID: com.compiledplatforms.kmp.library → $GROUP_ID"
echo "Project Name: kotlin-multiplatform-library-template → $PROJECT_NAME"
echo "GitHub Org: compiledplatforms → $GITHUB_ORG"
echo "Developer Name: Developer Name → $DEVELOPER_NAME"
echo "Developer Username: developer → $DEVELOPER_USERNAME"
echo ""

read -p "Proceed with these changes? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled"
    exit 0
fi

echo ""
echo "🔧 Applying changes..."

# Backup current state
echo "📋 Creating backup..."
BACKUP_DIR=".setup-backup-$(date +%s)"
mkdir -p "$BACKUP_DIR"
cp -r settings.gradle.kts README.md buildSrc libraries bom samples scripts "$BACKUP_DIR/" 2>/dev/null || true

# Function to replace in file
replace_in_file() {
    local file=$1
    local old=$2
    local new=$3
    
    if [ -f "$file" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|$old|$new|g" "$file"
        else
            # Linux
            sed -i "s|$old|$new|g" "$file"
        fi
    fi
}

# Replace group ID in all files
echo "📦 Updating group ID..."
find . -type f \( -name "*.gradle.kts" -o -name "*.kt" -o -name "*.md" -o -name "*.sh" \) \
    -not -path "*/build/*" \
    -not -path "*/.gradle/*" \
    -not -path "*/.git/*" \
    -not -path "*/.setup-backup-*/*" \
    -exec grep -l "com\.compiledplatforms\.kmp\.library" {} \; | while read -r file; do
    replace_in_file "$file" "com\.compiledplatforms\.kmp\.library" "$GROUP_ID"
done

# Replace project name
echo "📝 Updating project name..."
replace_in_file "settings.gradle.kts" "kotlin-multiplatform-library-template" "$PROJECT_NAME"
find . -type f \( -name "*.md" -o -name "*.gradle.kts" \) \
    -not -path "*/build/*" \
    -not -path "*/.gradle/*" \
    -not -path "*/.git/*" \
    -not -path "*/.setup-backup-*/*" \
    -exec grep -l "kotlin-multiplatform-library-template" {} \; | while read -r file; do
    replace_in_file "$file" "kotlin-multiplatform-library-template" "$PROJECT_NAME"
done

# Replace GitHub org
echo "🐙 Updating GitHub URLs..."
find . -type f \( -name "*.gradle.kts" -o -name "*.md" \) \
    -not -path "*/build/*" \
    -not -path "*/.gradle/*" \
    -not -path "*/.git/*" \
    -not -path "*/.setup-backup-*/*" \
    -exec grep -l "compiledplatforms" {} \; | while read -r file; do
    replace_in_file "$file" "compiledplatforms" "$GITHUB_ORG"
done

# Replace developer info in POM files
echo "👤 Updating developer information..."
find . -type f -name "*.gradle.kts" \
    -not -path "*/build/*" \
    -not -path "*/.gradle/*" \
    -not -path "*/.git/*" \
    -not -path "*/.setup-backup-*/*" \
    -exec grep -l "Developer Name" {} \; | while read -r file; do
    replace_in_file "$file" "Developer Name" "$DEVELOPER_NAME"
done

find . -type f -name "*.gradle.kts" \
    -not -path "*/build/*" \
    -not -path "*/.gradle/*" \
    -not -path "*/.git/*" \
    -not -path "*/.setup-backup-*/*" \
    -exec grep -l "id = \"developer\"" {} \; | while read -r file; do
    replace_in_file "$file" "id = \"developer\"" "id = \"$DEVELOPER_USERNAME\""
    replace_in_file "$file" "url = \"https://github.com/developer\"" "url = \"https://github.com/$DEVELOPER_USERNAME\""
done

# Update namespace in convention plugin
echo "🔧 Updating Android namespaces..."
NAMESPACE_BASE=$(echo "$GROUP_ID" | sed 's/\./\\./g')
find buildSrc -type f -name "*.gradle.kts" -exec grep -l "com\.compiledplatforms\.kmp\.library" {} \; | while read -r file; do
    replace_in_file "$file" "com\.compiledplatforms\.kmp\.library" "$GROUP_ID"
done

# Mark as configured
echo "configured" > .template

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review the changes with: git diff"
echo "2. Test the build: ./gradlew build"
echo "3. Remove the example library if not needed: rm -rf libraries/example-library"
echo "4. Create your first library: ./scripts/create-library.sh"
echo "5. Update README.md with your project details"
echo ""
echo "Backup saved to: $BACKUP_DIR"
echo "You can remove it after verifying everything works correctly."
echo ""
