pluginManagement {
    includeBuild("build-logic")
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "kotlin-multiplatform-library-template"

// Include BOM (Bill of Materials)
include(":bom")

// Auto-discover all library modules in the libraries/ directory
file("libraries").listFiles()?.forEach { libraryDir ->
    if (libraryDir.isDirectory && file("${libraryDir.path}/build.gradle.kts").exists()) {
        val libraryName = libraryDir.name
        include(":libraries:$libraryName")
    }
}

// Auto-discover all sample applications (1-level and 2-level deep)
file("samples").listFiles()?.forEach { sampleDir ->
    if (sampleDir.isDirectory) {
        // Check if this directory itself is a sample (has build.gradle.kts)
        if (file("${sampleDir.path}/build.gradle.kts").exists()) {
            include(":samples:${sampleDir.name}")
        } else {
            // Otherwise, check for nested samples
            sampleDir.listFiles()?.forEach { nestedSampleDir ->
                if (nestedSampleDir.isDirectory && file("${nestedSampleDir.path}/build.gradle.kts").exists()) {
                    include(":samples:${sampleDir.name}:${nestedSampleDir.name}")
                }
            }
        }
    }
}

// You can also manually include specific modules if needed:
// include(":libraries:my-custom-library")
// include(":samples:my-custom-sample")
