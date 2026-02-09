package config

import com.android.build.api.dsl.KotlinMultiplatformAndroidLibraryTarget
import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalog
import org.gradle.api.plugins.ExtraPropertiesExtension
import org.gradle.kotlin.dsl.configure
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

/**
 * Configures the Android target within KMP using the
 * com.android.kotlin.multiplatform.library plugin (AGP 9.0+).
 *
 * The plugin registers an `android` extension on `KotlinMultiplatformExtension`.
 * In a convention plugin there are no generated accessors, so we look it up by name.
 *
 * See: https://developer.android.com/kotlin/multiplatform/plugin
 */
object AndroidLibraryConfig {

    @Suppress("UNCHECKED_CAST")
    private fun hasAndroidTarget(project: Project): Boolean {
        val extraProperties = project.extensions.findByType(ExtraPropertiesExtension::class.java)
            ?: return false
        val targets = extraProperties.get("kmpTargets") as? Set<*> ?: return false
        return targets.any { it.toString() == "Android" || it.toString().lowercase() == "android" }
    }

    fun configure(project: Project, libs: VersionCatalog) {
        if (!hasAndroidTarget(project)) return

        project.extensions.configure<KotlinMultiplatformExtension> {
            val android = extensions.findByName("android") as? KotlinMultiplatformAndroidLibraryTarget
                ?: return@configure

            android.apply {
                namespace = "com.compiledplatforms.kmp.library.${project.name.replace("-", ".")}"
                compileSdk = libs.findVersion("android-compileSdk").get().toString().toInt()
                minSdk = libs.findVersion("android-minSdk").get().toString().toInt()

                compilerOptions {
                    jvmTarget.set(JvmTarget.JVM_11)
                }

                val consumerRulesFile = project.file("consumer-rules.pro")
                if (consumerRulesFile.exists()) {
                    @Suppress("UnstableApiUsage")
                    (this as com.android.build.api.dsl.KotlinMultiplatformAndroidLibraryExtension)
                        .optimization.consumerKeepRules.apply {
                            publish = true
                            file(consumerRulesFile)
                        }
                }

                withHostTestBuilder {}.configure {}
                withDeviceTestBuilder {
                    sourceSetTreeName = "test"
                }

                compilations.configureEach {
                    compileTaskProvider.configure {
                        compilerOptions {
                            jvmTarget.set(JvmTarget.JVM_11)
                        }
                    }
                }
            }
        }
    }
}
