plugins {
    id("java-platform")
    alias(libs.plugins.vanniktech.mavenPublish)
}

group = "com.compiledplatforms.kmp.library"
version = "1.0.0"  // BOM has its own independent version

description = "Bill of Materials for Kotlin Multiplatform libraries"

// Manually specify which library versions are tested and compatible together
// Update these when you release new compatible versions
dependencies.constraints {
    // Add your libraries here with their specific versions
    api("com.compiledplatforms.kmp.library:example-library:1.0.0")

    // When you add more libraries, add them here with their versions:
    // api("com.compiledplatforms.kmp.library:another-library:2.3.0")
    // api("com.compiledplatforms.kmp.library:third-library:1.5.0")
}

// Maven publishing configuration
mavenPublishing {
    // Multi-repository publishing based on project.yml
    // Same as libraries - supports Maven Central, GitHub Packages, Custom Maven, JFrog, CloudSmith

    // Only sign if not explicitly disabled (for local testing)
    if (project.findProperty("skipSigning") != "true") {
        signAllPublications()
    }

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
            url = "https://github.com/compiledplatforms/kotlin-multiplatform-library-template/"
            connection = "scm:git:git://github.com/compiledplatforms/kotlin-multiplatform-library-template.git"
            developerConnection = "scm:git:ssh://git@github.com/compiledplatforms/kotlin-multiplatform-library-template.git"
        }
    }
}

// Configure Maven Central via vanniktech plugin
// Reads from project.yml: publishing.repositories.maven_central.enabled
if (rootProject.findProperty("publishing.mavenCentral.enabled")?.toString()?.toBoolean() == true) {
    mavenPublishing {
        publishToMavenCentral()
    }
}

// Configure additional repositories based on project.yml
afterEvaluate {
    publishing {
        repositories {
            // GitHub Packages
            if (rootProject.findProperty("publishing.githubPackages.enabled")?.toString()?.toBoolean() == true) {
                val owner = rootProject.findProperty("publishing.githubPackages.owner")?.toString()
                val repo = rootProject.findProperty("publishing.githubPackages.repository")?.toString()
                if (owner != null && repo != null) {
                    maven {
                        name = "GitHubPackages"
                        url = uri("https://maven.pkg.github.com/$owner/$repo")
                        credentials {
                            username = findProperty("gpr.user")?.toString() ?: System.getenv("GITHUB_ACTOR")
                            password = findProperty("gpr.token")?.toString() ?: System.getenv("GITHUB_TOKEN")
                        }
                    }
                }
            }

            // Custom Maven (Nexus/Artifactory)
            if (rootProject.findProperty("publishing.customMaven.enabled")?.toString()?.toBoolean() == true) {
                val releasesUrl = rootProject.findProperty("publishing.customMaven.releasesUrl")?.toString()
                val snapshotsUrl = rootProject.findProperty("publishing.customMaven.snapshotsUrl")?.toString()
                val repoName = rootProject.findProperty("publishing.customMaven.name")?.toString() ?: "CustomMaven"
                if (releasesUrl != null && snapshotsUrl != null) {
                    maven {
                        name = repoName.replace(" ", "")
                        url = uri(if (version.toString().endsWith("SNAPSHOT")) snapshotsUrl else releasesUrl)
                        credentials {
                            username = findProperty("customMaven.username")?.toString() ?: System.getenv("CUSTOM_MAVEN_USERNAME")
                            password = findProperty("customMaven.password")?.toString() ?: System.getenv("CUSTOM_MAVEN_PASSWORD")
                        }
                    }
                }
            }

            // JFrog Artifactory
            if (rootProject.findProperty("publishing.jfrog.enabled")?.toString()?.toBoolean() == true) {
                val jfrogUrl = rootProject.findProperty("publishing.jfrog.url")?.toString()
                if (jfrogUrl != null) {
                    maven {
                        name = "JFrog"
                        url = uri(jfrogUrl)
                        credentials {
                            username = findProperty("jfrog.username")?.toString() ?: System.getenv("JFROG_USERNAME")
                            password = findProperty("jfrog.password")?.toString()
                                ?: System.getenv("JFROG_PASSWORD")
                                ?: System.getenv("JFROG_API_KEY")
                        }
                    }
                }
            }

            // CloudSmith
            if (rootProject.findProperty("publishing.cloudsmith.enabled")?.toString()?.toBoolean() == true) {
                val owner = rootProject.findProperty("publishing.cloudsmith.owner")?.toString()
                val repo = rootProject.findProperty("publishing.cloudsmith.repository")?.toString()
                if (owner != null && repo != null) {
                    maven {
                        name = "CloudSmith"
                        url = uri("https://maven.cloudsmith.io/$owner/$repo/")
                        credentials {
                            username = findProperty("cloudsmith.username")?.toString()
                                ?: System.getenv("CLOUDSMITH_USERNAME")
                                ?: owner
                            password = findProperty("cloudsmith.apiKey")?.toString()
                                ?: System.getenv("CLOUDSMITH_API_KEY")
                        }
                    }
                }
            }
        }
    }
}
