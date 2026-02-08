plugins {
    id("convention.library")
    alias(libs.plugins.mokkery)
}

description = "Platform-specific static information with no reactive dependencies"

@OptIn(org.jetbrains.kotlin.gradle.ExperimentalWasmDsl::class)
kotlin {
    // Add JS target (browser support)
    js(IR) {
        browser {
            testTask {
                useKarma {
                    useChromeHeadless()
                }
            }
        }
    }

    // Add WasmJS target (browser support via WebAssembly)
    wasmJs {
        browser {
            testTask {
                useKarma {
                    useChromeHeadless()
                }
            }
        }
    }

    // Add Windows target
    mingwX64()

    sourceSets {
        commonMain.dependencies {
            // No dependencies - pure Kotlin library
        }

        commonTest.dependencies {
            // Test dependencies are already configured in convention plugin
        }
    }
}
