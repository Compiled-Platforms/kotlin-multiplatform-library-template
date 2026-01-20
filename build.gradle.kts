// Root build file for the Kotlin Multiplatform Monorepo
// Convention plugins are defined in build-logic/

plugins {
    // Apply plugins with false to avoid classloader conflicts with build-logic
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.android.kotlin.multiplatform.library) apply false
    alias(libs.plugins.vanniktech.mavenPublish) apply false
    alias(libs.plugins.detekt) apply false
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
