plugins {
    alias(libs.plugins.kotlinMultiplatform)
}

kotlin {
    jvm()

    sourceSets {
        commonMain.dependencies {
            implementation(project(":libraries:example-library"))
        }
    }
}

tasks.register<JavaExec>("run") {
    group = "application"
    description = "Run the JVM CLI sample"
    classpath = kotlin.jvm().compilations.getByName("main").output.allOutputs +
            kotlin.jvm().compilations.getByName("main").runtimeDependencyFiles
    mainClass.set("JvmMainKt")
}
