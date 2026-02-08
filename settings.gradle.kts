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

// Auto-discover sample applications: samples/<name> or samples/<group>/<name>
file("samples").listFiles()?.forEach { firstDir ->
    if (!firstDir.isDirectory) return@forEach
    val buildAtFirst = file("${firstDir.path}/build.gradle.kts").exists()
    if (buildAtFirst) {
        include(":samples:${firstDir.name}")
    } else {
        firstDir.listFiles()?.forEach { secondDir ->
            if (secondDir.isDirectory && file("${secondDir.path}/build.gradle.kts").exists()) {
                include(":samples:${firstDir.name}:${secondDir.name}")
            }
        }
    }
}

// You can also manually include specific modules if needed:
// include(":libraries:my-custom-library")
// include(":samples:my-custom-sample")