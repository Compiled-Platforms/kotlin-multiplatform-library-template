package config

import com.android.build.api.dsl.androidLibrary
import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalog
import org.gradle.kotlin.dsl.configure
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

/**
 * Configures Android library settings within KMP.
 * Responsibility: Android-specific configuration and R8 consumer rules.
 */
object AndroidLibraryConfig {
    
    fun configure(project: Project, libs: VersionCatalog) {
        // Configure Android library in KMP
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
