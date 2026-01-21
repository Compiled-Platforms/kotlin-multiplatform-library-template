#!/usr/bin/env python3

"""
Script to create a new Kotlin Multiplatform library in the monorepo
"""

import sys
from pathlib import Path


def print_error(message: str) -> None:
    """Print error message"""
    print(f"❌ {message}")


def print_success(message: str) -> None:
    """Print success message"""
    print(f"✅ {message}")


def to_display_name(library_name: str) -> str:
    """Convert kebab-case to Title Case"""
    return ' '.join(word.capitalize() for word in library_name.split('-'))


def to_package_name(library_name: str) -> str:
    """Convert kebab-case to package name"""
    return library_name.replace('-', '.')


def create_library(library_name: str) -> None:
    """Create a new library with the given name"""
    library_dir = Path('libraries') / library_name
    
    # Check if library already exists
    if library_dir.exists():
        print_error(f"Error: Library '{library_name}' already exists at {library_dir}")
        sys.exit(1)
    
    print(f"🚀 Creating new library: {library_name}")
    
    # Create directory structure
    print("📁 Creating directory structure...")
    source_sets = [
        'commonMain/kotlin',
        'commonTest/kotlin',
        'jvmMain/kotlin',
        'jvmTest/kotlin',
        'androidMain/kotlin',
        'androidHostTest/kotlin',
        'iosMain/kotlin',
        'iosTest/kotlin',
        'linuxX64Main/kotlin',
        'linuxX64Test/kotlin',
    ]
    
    for source_set in source_sets:
        (library_dir / 'src' / source_set).mkdir(parents=True, exist_ok=True)
    
    # Create build.gradle.kts
    print("📝 Creating build.gradle.kts...")
    display_name = to_display_name(library_name)
    build_gradle = f'''plugins {{
    id("convention.library")
}}

group = "com.compiledplatforms.kmp.library"  // TODO: Update to your group
version = "1.0.0"

description = "TODO: Add description of your library"

kotlin {{
    sourceSets {{
        commonMain.dependencies {{
            // Add your multiplatform dependencies here
        }}
    }}
}}

mavenPublishing {{
    coordinates(group.toString(), "{library_name}", version.toString())
    
    pom {{
        name = "{display_name}"
        description = "TODO: Add detailed description"
        inceptionYear = "2026"
        url = "https://github.com/your-org/your-repo/"
        
        licenses {{
            license {{
                name = "The Apache Software License, Version 2.0"
                url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
                distribution = "repo"
            }}
        }}
        
        developers {{
            developer {{
                id = "yourusername"
                name = "Your Name"
                url = "https://github.com/yourusername"
            }}
        }}
        
        scm {{
            url = "https://github.com/your-org/your-repo/"
            connection = "scm:git:git://github.com/your-org/your-repo.git"
            developerConnection = "scm:git:ssh://git@github.com/your-org/your-repo.git"
        }}
    }}
}}
'''
    (library_dir / 'build.gradle.kts').write_text(build_gradle)
    
    # Create sample source file
    print("📄 Creating sample source file...")
    package_name = to_package_name(library_name)
    hello_world = f'''package com.compiledplatforms.kmp.library.{package_name}

/**
 * A simple greeting function.
 */
fun greet(name: String): String {{
    return "Hello, $name from {display_name}!"
}}
'''
    (library_dir / 'src' / 'commonMain' / 'kotlin' / 'HelloWorld.kt').write_text(hello_world)
    
    # Create sample test file
    print("🧪 Creating sample test file...")
    hello_world_test = f'''package com.compiledplatforms.kmp.library.{package_name}

import kotlin.test.Test
import kotlin.test.assertEquals

class HelloWorldTest {{
    @Test
    fun testGreet() {{
        val result = greet("World")
        assertEquals("Hello, World from {display_name}!", result)
    }}
}}
'''
    (library_dir / 'src' / 'commonTest' / 'kotlin' / 'HelloWorldTest.kt').write_text(hello_world_test)
    
    # Create README
    print("📖 Creating README...")
    readme = f'''# {display_name}

TODO: Add description of your library

## Installation

### Gradle (Kotlin DSL)

```kotlin
dependencies {{
    implementation("com.compiledplatforms.kmp.library:{library_name}:1.0.0")
}}
```

### Gradle (Groovy)

```groovy
dependencies {{
    implementation 'com.compiledplatforms.kmp.library:{library_name}:1.0.0'
}}
```

## Usage

```kotlin
import com.compiledplatforms.kmp.library.{package_name}.greet

fun main() {{
    println(greet("World"))
}}
```

## Features

TODO: List key features

## License

TODO: Add license information
'''
    (library_dir / 'README.md').write_text(readme)
    
    # Success message
    print()
    print_success(f"Library '{library_name}' created successfully!")
    print()
    print(f"📂 Location: {library_dir}")
    print()
    print("Next steps:")
    print(f"  1. Update group, version, and description in {library_dir}/build.gradle.kts")
    print(f"  2. Implement your library in {library_dir}/src/commonMain/kotlin/")
    print(f"  3. Add tests in {library_dir}/src/commonTest/kotlin/")
    print(f"  4. Build your library: ./gradlew :libraries:{library_name}:build")
    print(f"  5. Test your library: ./gradlew :libraries:{library_name}:test")
    print()


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python scripts/create-library.py <library-name>")
        print("Example: python scripts/create-library.py my-awesome-library")
        sys.exit(1)
    
    library_name = sys.argv[1]
    
    # Validate library name
    if not library_name.replace('-', '').replace('_', '').isalnum():
        print_error("Error: Library name should only contain letters, numbers, hyphens, and underscores")
        sys.exit(1)
    
    create_library(library_name)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_error("Cancelled by user")
        sys.exit(1)
