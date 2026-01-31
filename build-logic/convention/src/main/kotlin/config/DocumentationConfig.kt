package config

import org.gradle.api.Project
import org.gradle.kotlin.dsl.configure

/**
 * Configures documentation generation (Dokka).
 * Responsibility: API documentation setup and source linking.
 */
object DocumentationConfig {
    
    fun configure(project: Project) {
        project.extensions.configure<org.jetbrains.dokka.gradle.DokkaExtension> {
            // Configure publication-level settings
            dokkaPublications.configureEach {
                moduleName.set(project.name)
                // Suppress obvious functions (toString, equals, hashCode, etc.)
                suppressObviousFunctions.set(true)
            }
            
            // Configure source linking to GitHub
            dokkaSourceSets.configureEach {
                sourceLink {
                    localDirectory.set(project.projectDir.resolve("src"))
                    remoteUrl("https://github.com/Compiled-Platforms/kotlin-multiplatform-library-template/tree/main/${project.path.replace(":", "/")}/src")
                    remoteLineSuffix.set("#L")
                }
            }
        }
    }
}
