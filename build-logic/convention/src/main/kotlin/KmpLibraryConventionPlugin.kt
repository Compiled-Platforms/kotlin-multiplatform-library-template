import config.AndroidLibraryConfig
import config.CodeQualityConfig
import config.DocumentationConfig
import config.KotlinMultiplatformConfig
import config.PublishingConfig
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalogsExtension
import org.gradle.kotlin.dsl.getByType

/**
 * Convention plugin for Kotlin Multiplatform libraries.
 * 
 * Responsibility: Coordinates plugin application and delegates configuration
 * to focused, single-responsibility configuration classes.
 * 
 * Configuration is handled by:
 * - [KotlinMultiplatformConfig] - KMP targets and source sets
 * - [AndroidLibraryConfig] - Android-specific configuration
 * - [CodeQualityConfig] - Detekt static analysis
 * - [DocumentationConfig] - Dokka API documentation
 * - [PublishingConfig] - Maven publishing to multiple repositories
 */
class KmpLibraryConventionPlugin : Plugin<Project> {
    
    override fun apply(target: Project) {
        with(target) {
            // Apply required plugins
            applyPlugins()
            
            // Access version catalog for dependency management
            val libs = extensions.getByType<VersionCatalogsExtension>().named("libs")
            
            // Delegate configuration to focused components
            KotlinMultiplatformConfig.configure(this, libs)
            AndroidLibraryConfig.configure(this, libs)
            CodeQualityConfig.configure(this)
            DocumentationConfig.configure(this)
            PublishingConfig.configure(this)
        }
    }
    
    private fun Project.applyPlugins() {
        pluginManager.apply {
            apply("org.jetbrains.kotlin.multiplatform")
            apply("com.android.kotlin.multiplatform.library")
            apply("com.vanniktech.maven.publish")
            apply("dev.detekt")
            apply("org.jetbrains.dokka")
            apply("org.jetbrains.kotlinx.kover")
        }
    }
}
