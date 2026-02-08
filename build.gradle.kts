// Root build file for the Kotlin Multiplatform Monorepo
// Convention plugins are defined in build-logic/

plugins {
    // Apply plugins with false to avoid classloader conflicts with build-logic
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.android.kotlin.multiplatform.library) apply false
    alias(libs.plugins.jetbrainsCompose) apply false
    alias(libs.plugins.composeCompiler) apply false
    alias(libs.plugins.vanniktech.mavenPublish) apply false
    alias(libs.plugins.detekt) apply false
    alias(libs.plugins.mokkery) apply false
    alias(libs.plugins.dokka)
    alias(libs.plugins.binaryCompatibilityValidator)
    alias(libs.plugins.kover)
}

// Repositories are configured in settings.gradle.kts via dependencyResolutionManagement.

// Configure Dokka V2 for multi-module documentation
extensions.configure<org.jetbrains.dokka.gradle.DokkaExtension> {
    moduleName.set("Kotlin Multiplatform Libraries")
}

// Configure Binary Compatibility Validator
extensions.configure<kotlinx.validation.ApiValidationExtension> {
    // Ignore internal packages and test projects from API validation
    ignoredPackages.addAll(listOf("internal", "benchmarks"))
    ignoredProjects.addAll(listOf("bom")) // BOM has no API

    // Projects in samples/ are not libraries, exclude them
    project.subprojects.forEach { subproject ->
        if (subproject.path.startsWith(":samples:")) {
            ignoredProjects.add(subproject.name)
        }
    }

    // Mark any @InternalApi annotations as non-public
    nonPublicMarkers.add("com.compiledplatforms.kmp.library.InternalApi")

    // Enable experimental Kotlin/Native (KLib) ABI validation
    @OptIn(kotlinx.validation.ExperimentalBCVApi::class)
    klib {
        enabled = true
        // Set to false for cross-platform builds (e.g., Linux host can't validate iOS)
        strictValidation = false
    }
}

// Configure Kover for code coverage aggregation
dependencies {
    // Add library projects to coverage aggregation
    subprojects.forEach { subproject ->
        if (subproject.path.startsWith(":libraries:")) {
            kover(subproject)
        }
    }
}

kover {
    reports {
        // Configure report filters
        filters {
            excludes {
                // Exclude common generated code patterns
                classes("*.BuildConfig")
                classes("*.ComposableSingletons*")
                classes("*_Factory")
                classes("*_MembersInjector")

                // Exclude internal packages
                packages("*.internal")
                packages("*.internal.*")
            }
        }
    }
}
