package config

import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalog
import org.gradle.kotlin.dsl.configure
import org.gradle.kotlin.dsl.dependencies
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

/**
 * Configures Kotlin Multiplatform targets and source sets.
 * Responsibility: KMP platform setup and common dependencies.
 */
object KotlinMultiplatformConfig {
    
    fun configure(project: Project, libs: VersionCatalog) {
        project.extensions.configure<KotlinMultiplatformExtension> {
            // Configure JVM target
            jvm()
            
            // Configure iOS targets
            iosX64()
            iosArm64()
            iosSimulatorArm64()
            
            // Configure Linux target
            linuxX64()
            
            // Configure source sets
            sourceSets.apply {
                commonMain.dependencies {
                    // Common dependencies will be added by individual libraries
                }
                
                commonTest.dependencies {
                    // Standard test dependencies for all KMP libraries
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
