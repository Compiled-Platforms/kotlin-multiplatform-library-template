package config

import com.android.build.api.dsl.androidLibrary
import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalog
import org.gradle.api.plugins.ExtraPropertiesExtension
import org.gradle.kotlin.dsl.configure
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

/**
 * Configures Android library settings within KMP.
 * Responsibility: Android-specific configuration and R8 consumer rules.
 * Only runs if "android" is in the library's kmp.targets (see KotlinMultiplatformConfig).
 */
object AndroidLibraryConfig {

    @Suppress("UNCHECKED_CAST")
    private fun hasAndroidTarget(project: Project): Boolean {
        val extraProperties = project.extensions.findByType(ExtraPropertiesExtension::class.java)
            ?: throw IllegalStateException(
                "ExtraPropertiesExtension not found. Ensure KotlinMultiplatformConfig.configure() has been applied before AndroidLibraryConfig."
            )
        val targets = extraProperties.get("kmpTargets") as? Set<*>
            ?: throw IllegalStateException(
                "kmpTargets property not set. Ensure KotlinMultiplatformConfig.configure() sets 'kmpTargets' before AndroidLibraryConfig."
            )
        return targets.contains("android")
    }

    fun configure(project: Project, libs: VersionCatalog) {
        if (!hasAndroidTarget(project)) return

        project.extensions.configure<KotlinMultiplatformExtension> {
            androidLibrary {
                // Generate namespace from project name
                namespace = "com.compiledplatforms.kmp.library.${project.name.replace("-", ".")}"
                
                // SDK versions from version catalog
                compileSdk = libs.findVersion("android-compileSdk").get().toString().toInt()
                minSdk = libs.findVersion("android-minSdk").get().toString().toInt()
                
                // Enable Java compilation support
                withJava()
                
                // Configure test builders
                withHostTestBuilder {}.configure {}
                withDeviceTestBuilder {
                    sourceSetTreeName = "test"
                }
                
                // Configure compilation options
                compilations.configureEach {
                    compileTaskProvider.configure {
                        compilerOptions {
                            jvmTarget.set(JvmTarget.JVM_11)
                        }
                    }
                }
            }
            // Publish only release variant for Android (Kotlin target, not androidLibrary block)
            targets.withType(org.jetbrains.kotlin.gradle.plugin.mpp.KotlinAndroidTarget::class.java).configureEach {
                publishLibraryVariants("release")
            }
        }
        
        // Configure R8 consumer rules after evaluation
        configureR8ConsumerRules(project)
    }
    
    private fun configureR8ConsumerRules(project: Project) {
        project.afterEvaluate {
            extensions.findByType(com.android.build.gradle.LibraryExtension::class.java)?.apply {
                val consumerRulesFile = project.file("consumer-rules.pro")
                if (consumerRulesFile.exists()) {
                    defaultConfig {
                        consumerProguardFiles(consumerRulesFile)
                    }
                }
            }
        }
    }
}
