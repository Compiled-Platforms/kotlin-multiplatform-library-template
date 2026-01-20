plugins {
    id("convention.library")
}

// Group and version are inherited from gradle.properties (GROUP and VERSION_NAME)

description = "An example Kotlin Multiplatform library"

kotlin {
    sourceSets {
        commonMain.dependencies {
            // Add your multiplatform dependencies here
        }
    }
}

// Maven publishing configuration
// Group, version, and artifactId are automatically inherited:
// - group from gradle.properties (GROUP)
// - version from gradle.properties (VERSION_NAME)
// - artifactId from project name (example-library)
mavenPublishing {
    pom {
        name = "Example Library"
        description = "An example Kotlin Multiplatform library demonstrating the monorepo structure"
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
                id = "developer"
                name = "Developer Name"
                url = "https://github.com/developer"
            }
        }
        
        scm {
            url = "https://github.com/compiledplatforms/kotlin-multiplatform-library-template/"
            connection = "scm:git:git://github.com/compiledplatforms/kotlin-multiplatform-library-template.git"
            developerConnection = "scm:git:ssh://git@github.com/compiledplatforms/kotlin-multiplatform-library-template.git"
        }
    }
}
