import com.android.build.api.dsl.androidLibrary
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("org.jetbrains.kotlin.multiplatform")
    id("com.android.kotlin.multiplatform.library")
    id("com.vanniktech.maven.publish")
}

kotlin {
    jvm()
    
    androidLibrary {
        namespace = "io.github.kotlin.${project.name.replace("-", ".")}"
        compileSdk = 36
        minSdk = 24

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

    sourceSets {
        commonMain.dependencies {
            // Common dependencies will be added here by individual libraries
        }

        commonTest.dependencies {
            implementation("org.jetbrains.kotlin:kotlin-test:2.2.20")
        }
    }
}

// Maven publishing configuration
mavenPublishing {
    publishToMavenCentral()
    signAllPublications()
}
