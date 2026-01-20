#!/bin/bash

# Script to create a new Kotlin Multiplatform library in the monorepo

set -e

# Check if library name is provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/create-library.sh <library-name>"
    echo "Example: ./scripts/create-library.sh my-awesome-library"
    exit 1
fi

LIBRARY_NAME=$1
LIBRARY_DIR="libraries/$LIBRARY_NAME"

# Check if library already exists
if [ -d "$LIBRARY_DIR" ]; then
    echo "❌ Error: Library '$LIBRARY_NAME' already exists at $LIBRARY_DIR"
    exit 1
fi

echo "🚀 Creating new library: $LIBRARY_NAME"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$LIBRARY_DIR/src/commonMain/kotlin"
mkdir -p "$LIBRARY_DIR/src/commonTest/kotlin"
mkdir -p "$LIBRARY_DIR/src/jvmMain/kotlin"
mkdir -p "$LIBRARY_DIR/src/jvmTest/kotlin"
mkdir -p "$LIBRARY_DIR/src/androidMain/kotlin"
mkdir -p "$LIBRARY_DIR/src/androidHostTest/kotlin"
mkdir -p "$LIBRARY_DIR/src/iosMain/kotlin"
mkdir -p "$LIBRARY_DIR/src/iosTest/kotlin"
mkdir -p "$LIBRARY_DIR/src/linuxX64Main/kotlin"
mkdir -p "$LIBRARY_DIR/src/linuxX64Test/kotlin"

# Create build.gradle.kts
echo "📝 Creating build.gradle.kts..."
cat > "$LIBRARY_DIR/build.gradle.kts" << 'EOF'
plugins {
    id("convention.library")
}

group = "io.github.kotlin"  // TODO: Update to your group
version = "1.0.0"

description = "TODO: Add description of your library"

kotlin {
    sourceSets {
        commonMain.dependencies {
            // Add your multiplatform dependencies here
        }
    }
}

mavenPublishing {
    coordinates(group.toString(), "LIBRARY_NAME", version.toString())
    
    pom {
        name = "LIBRARY_DISPLAY_NAME"
        description = "TODO: Add detailed description"
        inceptionYear = "2026"
        url = "https://github.com/your-org/your-repo/"
        
        licenses {
            license {
                name = "The Apache Software License, Version 2.0"
                url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
                distribution = "repo"
            }
        }
        
        developers {
            developer {
                id = "yourusername"
                name = "Your Name"
                url = "https://github.com/yourusername"
            }
        }
        
        scm {
            url = "https://github.com/your-org/your-repo/"
            connection = "scm:git:git://github.com/your-org/your-repo.git"
            developerConnection = "scm:git:ssh://git@github.com/your-org/your-repo.git"
        }
    }
}
EOF

# Replace placeholders
sed -i.bak "s/LIBRARY_NAME/$LIBRARY_NAME/g" "$LIBRARY_DIR/build.gradle.kts"
rm "$LIBRARY_DIR/build.gradle.kts.bak"

# Convert library name to display name (kebab-case to Title Case)
DISPLAY_NAME=$(echo "$LIBRARY_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/LIBRARY_DISPLAY_NAME/$DISPLAY_NAME/g" "$LIBRARY_DIR/build.gradle.kts"
else
    sed -i "s/LIBRARY_DISPLAY_NAME/$DISPLAY_NAME/g" "$LIBRARY_DIR/build.gradle.kts"
fi

# Create a sample source file
echo "📄 Creating sample source file..."
PACKAGE_NAME=$(echo "$LIBRARY_NAME" | sed 's/-/./g')
cat > "$LIBRARY_DIR/src/commonMain/kotlin/HelloWorld.kt" << EOF
package io.github.kotlin.$PACKAGE_NAME

/**
 * A simple greeting function.
 */
fun greet(name: String): String {
    return "Hello, \$name from $DISPLAY_NAME!"
}
EOF

# Create a sample test file
echo "🧪 Creating sample test file..."
cat > "$LIBRARY_DIR/src/commonTest/kotlin/HelloWorldTest.kt" << EOF
package io.github.kotlin.$PACKAGE_NAME

import kotlin.test.Test
import kotlin.test.assertEquals

class HelloWorldTest {
    @Test
    fun testGreet() {
        val result = greet("World")
        assertEquals("Hello, World from $DISPLAY_NAME!", result)
    }
}
EOF

# Create README for the library
echo "📖 Creating README..."
cat > "$LIBRARY_DIR/README.md" << EOF
# $DISPLAY_NAME

TODO: Add description of your library

## Installation

### Gradle (Kotlin DSL)

\`\`\`kotlin
dependencies {
    implementation("io.github.kotlin:$LIBRARY_NAME:1.0.0")
}
\`\`\`

### Gradle (Groovy)

\`\`\`groovy
dependencies {
    implementation 'io.github.kotlin:$LIBRARY_NAME:1.0.0'
}
\`\`\`

## Usage

\`\`\`kotlin
import io.github.kotlin.$PACKAGE_NAME.greet

fun main() {
    println(greet("World"))
}
\`\`\`

## Features

TODO: List key features

## License

TODO: Add license information
EOF

echo ""
echo "✅ Library '$LIBRARY_NAME' created successfully!"
echo ""
echo "📂 Location: $LIBRARY_DIR"
echo ""
echo "Next steps:"
echo "  1. Update group, version, and description in $LIBRARY_DIR/build.gradle.kts"
echo "  2. Implement your library in $LIBRARY_DIR/src/commonMain/kotlin/"
echo "  3. Add tests in $LIBRARY_DIR/src/commonTest/kotlin/"
echo "  4. Build your library: ./gradlew :libraries:$LIBRARY_NAME:build"
echo "  5. Test your library: ./gradlew :libraries:$LIBRARY_NAME:test"
echo ""
