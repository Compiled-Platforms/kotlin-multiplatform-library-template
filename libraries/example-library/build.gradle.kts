plugins {
    id("convention.library")
}

group = "io.github.kotlin"
version = "1.0.0"

description = "An example Kotlin Multiplatform library"

kotlin {
    sourceSets {
        commonMain.dependencies {
            // Add your multiplatform dependencies here
        }
    }
}

// Maven publishing configuration
mavenPublishing {
    coordinates(group.toString(), "example-library", version.toString())
    
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
            url = "https://github.com/your-org/your-repo/"
            connection = "scm:git:git://github.com/your-org/your-repo.git"
            developerConnection = "scm:git:ssh://git@github.com/your-org/your-repo.git"
        }
    }
}
