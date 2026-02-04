package config

import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalog
import org.gradle.api.plugins.ExtraPropertiesExtension
import org.gradle.kotlin.dsl.configure
import org.gradle.kotlin.dsl.dependencies
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

/**
 * Configures Kotlin Multiplatform targets and source sets.
 * Responsibility: KMP platform setup and common dependencies.
 *
 * **Per-library targets:** Each library must set `kmp.targets` in its `gradle.properties`
 * to a comma-separated list. Valid values: `android`, `jvm`, `ios`, `linux`.
 * Example: `kmp.targets=android,jvm,ios,linux`
 */
object KotlinMultiplatformConfig {

    private val VALID_TARGETS = setOf("android", "jvm", "ios", "linux")

    fun parseTargets(project: Project): Set<String> {
        val raw = project.findProperty("kmp.targets") as? String
            ?: throw org.gradle.api.GradleException(
                "Library ${project.path}: kmp.targets must be set in gradle.properties. " +
                    "Add e.g. kmp.targets=android,jvm,ios,linux (comma-separated)."
            )
        val targets = raw.split(",").map { it.trim() }.filter { it.isNotEmpty() }.toSet()
        val invalid = targets - VALID_TARGETS
        if (invalid.isNotEmpty()) {
            throw org.gradle.api.GradleException(
                "Library ${project.path}: invalid kmp.targets: ${invalid.joinToString()}. " +
                    "Valid values: ${VALID_TARGETS.joinToString()}"
            )
        }
        if (targets.isEmpty()) {
            throw org.gradle.api.GradleException(
                "Library ${project.path}: kmp.targets must specify at least one target. " +
                    "Add e.g. kmp.targets=android,jvm,ios,linux (comma-separated)."
            )
        }
        return targets
    }

    fun configure(project: Project, libs: VersionCatalog) {
        val targets = parseTargets(project)
        project.extensions.getByType(ExtraPropertiesExtension::class.java).set("kmpTargets", targets)

        project.extensions.configure<KotlinMultiplatformExtension> {
            if (targets.contains("jvm")) jvm()
            if (targets.contains("ios")) {
                iosX64()
                iosArm64()
                iosSimulatorArm64()
            }
            if (targets.contains("linux")) linuxX64()

            sourceSets.apply {
                commonMain.dependencies {
                    // Common dependencies will be added by individual libraries
                }
                commonTest.dependencies {
                    implementation(libs.findLibrary("kotlin-test").get())
                    implementation(libs.findLibrary("kotlinx-coroutines-test").get())
                    implementation(libs.findLibrary("turbine").get())
                    implementation(libs.findLibrary("mokkery-runtime").get())
                    implementation(libs.findLibrary("kotest-assertions-core").get())
                }
            }
        }
    }
}
