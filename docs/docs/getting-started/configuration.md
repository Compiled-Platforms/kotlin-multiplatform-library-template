# Configuration

## Version Catalog

All dependencies and plugin versions are managed in `gradle/libs.versions.toml`:

```toml title="gradle/libs.versions.toml"
[versions]
kotlin = "2.2.20"
detekt = "2.0.0-alpha.1"

[libraries]
kotlin-test = { module = "org.jetbrains.kotlin:kotlin-test", version.ref = "kotlin" }

[plugins]
kotlinMultiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
detekt = { id = "dev.detekt", version.ref = "detekt" }
```

## Convention Plugin

Shared configuration is defined in `buildSrc/src/main/kotlin/convention.library.gradle.kts`. This applies to all libraries automatically.

### Customizing Targets

Add or remove targets in the convention plugin:

```kotlin
kotlin {
    jvm()
    
    androidLibrary { /* ... */ }
    
    // Add more targets
    js(IR) {
        browser()
        nodejs()
    }
    
    iosX64()
    iosArm64()
    iosSimulatorArm64()
    linuxX64()
}
```

### Library-Specific Configuration

Override settings in individual library `build.gradle.kts`:

```kotlin
group = "com.example"
version = "1.0.0"

kotlin {
    sourceSets {
        commonMain.dependencies {
            // Add library-specific dependencies
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
        }
    }
}
```

## Detekt Configuration

Code quality rules are configured in `config/detekt/detekt.yaml`. Customize rules:

```yaml
style:
  MaxLineLength:
    maxLineLength: 120
    
complexity:
  LongMethod:
    threshold: 60
```

## Maven Publishing

Configure publishing details in your library's `build.gradle.kts`:

```kotlin
mavenPublishing {
    coordinates(group.toString(), "library-name", version.toString())
    
    pom {
        name = "Library Display Name"
        description = "Library description"
        url = "https://github.com/your-org/your-repo/"
        
        licenses {
            license {
                name = "The Apache Software License, Version 2.0"
                url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
            }
        }
        
        developers {
            developer {
                id = "yourusername"
                name = "Your Name"
                url = "https://github.com/yourusername"
            }
        }
    }
}
```

## Next Steps

- [Development Setup](../development/setup.md) - Development environment setup
- [Creating Libraries](../development/creating-libraries.md) - Advanced topics
