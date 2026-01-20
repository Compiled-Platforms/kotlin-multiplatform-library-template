import com.android.build.api.dsl.androidLibrary
import dev.detekt.gradle.Detekt
import dev.detekt.gradle.extensions.DetektExtension
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.api.artifacts.VersionCatalogsExtension
import org.gradle.kotlin.dsl.configure
import org.gradle.kotlin.dsl.dependencies
import org.gradle.kotlin.dsl.getByType
import org.gradle.kotlin.dsl.withType
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

class KmpLibraryConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) {
        with(target) {
            with(pluginManager) {
                apply("org.jetbrains.kotlin.multiplatform")
                apply("com.android.kotlin.multiplatform.library")
                apply("com.vanniktech.maven.publish")
                apply("dev.detekt")
            }

            // Access version catalog
            val libs = extensions.getByType<VersionCatalogsExtension>().named("libs")

            // Configure Kotlin Multiplatform
            extensions.configure<KotlinMultiplatformExtension> {
                jvm()

                androidLibrary {
                    namespace = "com.compiledplatforms.kmp.library.${project.name.replace("-", ".")}"
                    compileSdk = libs.findVersion("android-compileSdk").get().toString().toInt()
                    minSdk = libs.findVersion("android-minSdk").get().toString().toInt()

                    withJava() // enable java compilation support
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

                iosX64()
                iosArm64()
                iosSimulatorArm64()
                linuxX64()

                sourceSets.apply {
                    commonMain.dependencies {
                        // Common dependencies will be added here by individual libraries
                    }

                    commonTest.dependencies {
                        implementation(libs.findLibrary("kotlin-test").get())
                    }
                }
            }

            // Configure R8 consumer rules for Android after KMP configuration
            afterEvaluate {
                project.extensions.findByType(com.android.build.gradle.LibraryExtension::class.java)?.apply {
                    val consumerRulesFile = project.file("consumer-rules.pro")
                    if (consumerRulesFile.exists()) {
                        defaultConfig {
                            consumerProguardFiles(consumerRulesFile)
                        }
                    }
                }
            }

            // Configure Detekt
            extensions.configure<DetektExtension> {
                buildUponDefaultConfig.set(true)
                allRules.set(false)
                config.setFrom(files("${rootProject.projectDir}/config/detekt/detekt.yaml"))
                source.setFrom(
                    "src/commonMain/kotlin",
                    "src/jvmMain/kotlin",
                    "src/androidMain/kotlin",
                    "src/iosMain/kotlin",
                    "src/linuxX64Main/kotlin"
                )
            }

            // Configure Maven Publishing
            extensions.configure<com.vanniktech.maven.publish.MavenPublishBaseExtension> {
                publishToMavenCentral()
                signAllPublications()
            }
        }
    }
}
