plugins {
    alias(libs.plugins.kotlinMultiplatform)
}

kotlin {
    jvm()
    
    sourceSets {
        commonMain.dependencies {
            // Use the library as a project dependency to ensure it's always in sync
            implementation(project(":libraries:example-library"))
        }
    }
    
    // Configure JVM binary for running the sample
    jvm().compilations.getByName("main") {
        compileTaskProvider.configure {
            compilerOptions {
                freeCompilerArgs.add("-Xmain-class=JvmMainKt")
            }
        }
    }
}

// Task to run the sample
tasks.register<JavaExec>("run") {
    group = "application"
    description = "Run the sample application"
    classpath = kotlin.jvm().compilations.getByName("main").output.allOutputs + 
                kotlin.jvm().compilations.getByName("main").runtimeDependencyFiles
    mainClass.set("JvmMainKt")
}
