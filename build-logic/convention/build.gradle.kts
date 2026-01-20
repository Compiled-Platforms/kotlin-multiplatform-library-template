plugins {
    `kotlin-dsl`
}

group = "com.compiledplatforms.kmp.library.buildlogic"

dependencies {
    implementation(libs.kotlin.gradle.plugin)
    implementation(libs.android.gradle.plugin)
    implementation(libs.vanniktech.maven.publish.plugin)
    implementation(libs.detekt.gradle.plugin)
}

gradlePlugin {
    plugins {
        register("kmpLibrary") {
            id = "convention.library"
            implementationClass = "KmpLibraryConventionPlugin"
        }
    }
}
