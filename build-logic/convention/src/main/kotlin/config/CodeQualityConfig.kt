package config

import dev.detekt.gradle.extensions.DetektExtension
import org.gradle.api.Project
import org.gradle.api.plugins.ExtraPropertiesExtension
import org.gradle.kotlin.dsl.configure

/**
 * Configures code quality tools (Detekt).
 * Responsibility: Static analysis and code quality checks.
 * Source paths are limited to this library's kmp.targets.
 */
object CodeQualityConfig {

    @Suppress("UNCHECKED_CAST")
    private fun getTargets(project: Project): Set<String> {
        val extraProperties = project.extensions.findByType(ExtraPropertiesExtension::class.java)
            ?: throw IllegalStateException(
                "ExtraPropertiesExtension not found. Ensure KotlinMultiplatformConfig.configure() has been applied before CodeQualityConfig."
            )
        return extraProperties.get("kmpTargets") as? Set<String>
            ?: throw IllegalStateException(
                "kmpTargets property not set. Ensure KotlinMultiplatformConfig.configure() sets 'kmpTargets' before CodeQualityConfig."
            )
    }

    fun configure(project: Project) {
        val targets = getTargets(project)
        val sourcePaths = mutableListOf("src/commonMain/kotlin", "src/commonTest/kotlin")
        if (targets.contains("android")) sourcePaths.add("src/androidMain/kotlin")
        if (targets.contains("jvm")) sourcePaths.add("src/jvmMain/kotlin")
        if (targets.contains("ios")) sourcePaths.add("src/iosMain/kotlin")
        if (targets.contains("linux")) sourcePaths.add("src/linuxX64Main/kotlin")

        project.extensions.configure<DetektExtension> {
            buildUponDefaultConfig.set(true)
            allRules.set(false)
            config.setFrom(project.files("${project.rootProject.projectDir}/config/detekt/detekt.yaml"))
            source.setFrom(sourcePaths.map { project.file(it) }.filter { it.exists() })
        }
    }
}
