package config

import dev.detekt.gradle.extensions.DetektExtension
import org.gradle.api.Project
import org.gradle.kotlin.dsl.configure

/**
 * Configures code quality tools (Detekt).
 * Responsibility: Static analysis and code quality checks.
 */
object CodeQualityConfig {
    
    fun configure(project: Project) {
        project.extensions.configure<DetektExtension> {
            buildUponDefaultConfig.set(true)
            allRules.set(false)
            
            // Use centralized Detekt configuration
            config.setFrom(project.files("${project.rootProject.projectDir}/config/detekt/detekt.yaml"))
            
            // Configure source paths for all KMP targets
            source.setFrom(
                "src/commonMain/kotlin",
                "src/jvmMain/kotlin",
                "src/androidMain/kotlin",
                "src/iosMain/kotlin",
                "src/linuxX64Main/kotlin"
            )
        }
    }
}
