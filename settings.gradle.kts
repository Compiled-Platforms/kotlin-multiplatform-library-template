pluginManagement {
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

rootProject.name = "kotlin-multiplatform-monorepo"

// Include BOM (Bill of Materials)
include(":bom")

// Auto-discover all library modules in the libraries/ directory
file("libraries").listFiles()?.forEach { libraryDir ->
    if (libraryDir.isDirectory && file("${libraryDir.path}/build.gradle.kts").exists()) {
        val libraryName = libraryDir.name
        include(":libraries:$libraryName")
    }
}

// Auto-discover all sample applications in the samples/ directory
file("samples").listFiles()?.forEach { sampleDir ->
    if (sampleDir.isDirectory && file("${sampleDir.path}/build.gradle.kts").exists()) {
        val sampleName = sampleDir.name
        include(":samples:$sampleName")
    }
}

// You can also manually include specific modules if needed:
// include(":libraries:my-custom-library")
// include(":samples:my-custom-sample")