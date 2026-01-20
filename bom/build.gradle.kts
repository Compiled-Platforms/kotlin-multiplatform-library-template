plugins {
    id("java-platform")
    id("com.vanniktech.maven.publish")
}

group = "io.github.kotlin"
version = "1.0.0"  // BOM has its own independent version

description = "Bill of Materials for Kotlin Multiplatform libraries"

// Manually specify which library versions are tested and compatible together
// Update these when you release new compatible versions
dependencies.constraints {
    // Add your libraries here with their specific versions
    api("io.github.kotlin:example-library:1.0.0")
    
    // When you add more libraries, add them here with their versions:
    // api("io.github.kotlin:another-library:2.3.0")
    // api("io.github.kotlin:third-library:1.5.0")
}

// Maven publishing configuration
mavenPublishing {
    publishToMavenCentral()
    signAllPublications()
    
    coordinates(group.toString(), "bom", version.toString())
    
    pom {
        name = "Kotlin Multiplatform Libraries BOM"
        description = "Bill of Materials for Kotlin Multiplatform libraries - manages dependency versions"
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
