plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.jetbrainsCompose)
    alias(libs.plugins.composeCompiler)
}

android {
    namespace = "com.compiledplatforms.kmp.library.fibonacci.sample"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        applicationId = "com.compiledplatforms.kmp.library.fibonacci.sample"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = libs.versions.android.compileSdk.get().toInt()
        versionCode = 1
        versionName = "1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(project(":samples:example-library:compose-multiplatform"))
    implementation(libs.androidx.activity.compose)
    implementation(libs.compose.ui.tooling.preview)
    implementation(libs.compose.ui.tooling)
}

tasks.register<Exec>("runDebug") {
    group = "application"
    description = "Install and launch the debug APK on a connected device/emulator"
    dependsOn("installDebug")

    commandLine(
        "adb", "shell", "am", "start",
        "-n", "com.compiledplatforms.kmp.library.fibonacci.sample/.MainActivity"
    )
}
