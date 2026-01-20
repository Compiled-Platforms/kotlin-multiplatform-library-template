plugins {
    `kotlin-dsl`
}

repositories {
    google()
    mavenCentral()
    gradlePluginPortal()
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-gradle-plugin:2.2.20")
    implementation("com.android.tools.build:gradle:8.13.0")
    implementation("com.vanniktech:gradle-maven-publish-plugin:0.34.0")
}
