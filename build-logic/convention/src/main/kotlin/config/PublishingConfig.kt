package config

import org.gradle.api.Project
import org.gradle.api.publish.PublishingExtension
import org.gradle.kotlin.dsl.configure
import java.io.ByteArrayOutputStream

/**
 * Configures Maven publishing to multiple repository types.
 * Responsibility: Publishing repository configuration and credentials management.
 */
object PublishingConfig {
    
    fun configure(project: Project) {
        // Configure base publishing settings
        project.extensions.configure<com.vanniktech.maven.publish.MavenPublishBaseExtension> {
            // Configure repositories based on project.yml
            configureRepositories(project)
            
            // Only sign if not explicitly disabled (for local testing)
            if (project.findProperty("skipSigning") != "true") {
                signAllPublications()
            }
        }
    }
    
    private fun configureRepositories(project: Project) {
        val publishingConfig = readPublishingConfig(project)
        
        // Configure Maven Central through vanniktech plugin
        if (publishingConfig["maven_central"] == true) {
            project.extensions.configure<com.vanniktech.maven.publish.MavenPublishBaseExtension> {
                // Use default Maven Central configuration
                publishToMavenCentral()
            }
        }
        
        // Configure additional repositories through Gradle publishing extension
        project.afterEvaluate {
            extensions.findByType(PublishingExtension::class.java)?.apply {
                configureGitHubPackages(project, publishingConfig)
                configureCustomMaven(project, publishingConfig)
                configureJFrog(project, publishingConfig)
                configureCloudSmith(project, publishingConfig)
            }
        }
    }
    
    private fun PublishingExtension.configureGitHubPackages(
        project: Project,
        config: Map<String, Boolean>
    ) {
        if (config["github_packages"] != true) return
        
        val owner = project.findProperty("publishing.githubPackages.owner")?.toString() ?: return
        val repo = project.findProperty("publishing.githubPackages.repository")?.toString() ?: return
        
        repositories {
            maven {
                name = "GitHubPackages"
                url = project.uri("https://maven.pkg.github.com/$owner/$repo")
                credentials {
                    username = project.findProperty("gpr.user")?.toString()
                        ?: System.getenv("GITHUB_ACTOR")
                    password = project.findProperty("gpr.token")?.toString()
                        ?: System.getenv("GITHUB_TOKEN")
                }
            }
        }
    }
    
    private fun PublishingExtension.configureCustomMaven(
        project: Project,
        config: Map<String, Boolean>
    ) {
        if (config["custom_maven"] != true) return
        
        val releasesUrl = project.findProperty("publishing.customMaven.releasesUrl")?.toString() ?: return
        val snapshotsUrl = project.findProperty("publishing.customMaven.snapshotsUrl")?.toString() ?: return
        val repoName = project.findProperty("publishing.customMaven.name")?.toString() ?: "CustomMaven"
        
        repositories {
            maven {
                name = repoName.replace(" ", "")
                url = project.uri(
                    if (project.version.toString().endsWith("SNAPSHOT")) snapshotsUrl
                    else releasesUrl
                )
                credentials {
                    username = project.findProperty("customMaven.username")?.toString()
                        ?: System.getenv("CUSTOM_MAVEN_USERNAME")
                    password = project.findProperty("customMaven.password")?.toString()
                        ?: System.getenv("CUSTOM_MAVEN_PASSWORD")
                }
            }
        }
    }
    
    private fun PublishingExtension.configureJFrog(
        project: Project,
        config: Map<String, Boolean>
    ) {
        if (config["jfrog"] != true) return
        
        val jfrogUrl = project.findProperty("publishing.jfrog.url")?.toString() ?: return
        
        repositories {
            maven {
                name = "JFrog"
                url = project.uri(jfrogUrl)
                credentials {
                    username = project.findProperty("jfrog.username")?.toString()
                        ?: System.getenv("JFROG_USERNAME")
                    password = project.findProperty("jfrog.password")?.toString()
                        ?: System.getenv("JFROG_PASSWORD")
                        ?: System.getenv("JFROG_API_KEY")
                }
            }
        }
    }
    
    private fun PublishingExtension.configureCloudSmith(
        project: Project,
        config: Map<String, Boolean>
    ) {
        if (config["cloudsmith"] != true) return
        
        val owner = project.findProperty("publishing.cloudsmith.owner")?.toString() ?: return
        val repo = project.findProperty("publishing.cloudsmith.repository")?.toString() ?: return
        
        repositories {
            maven {
                name = "CloudSmith"
                url = project.uri("https://maven.cloudsmith.io/$owner/$repo/")
                credentials {
                    username = project.findProperty("cloudsmith.username")?.toString()
                        ?: System.getenv("CLOUDSMITH_USERNAME")
                        ?: owner
                    password = project.findProperty("cloudsmith.apiKey")?.toString()
                        ?: System.getenv("CLOUDSMITH_API_KEY")
                }
            }
        }
    }
    
    /**
     * Read publishing configuration from project.yml using Python script.
     * Returns a map of repository names to their enabled status.
     */
    private fun readPublishingConfig(project: Project): Map<String, Boolean> {
        return try {
            val script = project.rootProject.file("scripts/get-publishing-config.py")
            if (!script.exists()) {
                return emptyMap()
            }
            
            val output = ByteArrayOutputStream()
            project.providers.exec {
                commandLine("python3", script.absolutePath, "--list-enabled")
                standardOutput = output
                isIgnoreExitValue = true
            }.result.get()
            
            output.toString().trim()
                .lines()
                .filter { it.isNotBlank() }
                .associateWith { true }
        } catch (e: Exception) {
            // If script fails, disable all publishing
            emptyMap()
        }
    }
}
