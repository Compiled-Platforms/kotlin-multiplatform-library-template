import org.jetbrains.compose.desktop.application.dsl.TargetFormat
import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.android.kotlin.multiplatform.library)
    alias(libs.plugins.jetbrainsCompose)
    alias(libs.plugins.composeCompiler)
}

kotlin {
    androidLibrary {
        namespace = "com.compiledplatforms.kmp.library.fibonacci.sample.shared"
        compileSdk = libs.versions.android.compileSdk.get().toInt()
        minSdk = libs.versions.android.minSdk.get().toInt()

        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_11)
        }

        androidResources {
            enable = true
        }
    }

    jvm()

    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "ComposeApp"
            isStatic = true
            binaryOption("bundleId", "com.compiledplatforms.kmp.library.fibonacci.sample")
        }
    }

    js(IR) {
        browser()
        binaries.executable()
    }

    @OptIn(ExperimentalWasmDsl::class)
    wasmJs {
        browser()
        binaries.executable()
    }

    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.ui)
            implementation(compose.components.resources)
            implementation(compose.components.uiToolingPreview)

            implementation(project(":libraries:example-library"))
        }

        jvmMain.dependencies {
            implementation(compose.desktop.currentOs)
        }
    }
}

compose.desktop {
    application {
        mainClass = "MainKt"

        nativeDistributions {
            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)
            packageName = "com.compiledplatforms.kmp.library.fibonacci.sample"
            packageVersion = "1.0.0"
        }
    }
}

// Task to kill any leftover webpack dev server processes
tasks.register<Exec>("killWebpack") {
    group = "build"
    description = "Kill any leftover webpack dev server processes"

    commandLine("sh", "-c", "pkill -f 'webpack' 2>/dev/null || true")

    // Ignore failures if no webpack processes are running
    isIgnoreExitValue = true
}

// Make JS/WasmJS browser tasks depend on killing webpack first
tasks.matching { it.name.contains("BrowserDevelopmentRun") }.configureEach {
    dependsOn("killWebpack")
}

tasks.matching { it.name.contains("BrowserProductionRun") }.configureEach {
    dependsOn("killWebpack")
}

tasks.matching { it.name.contains("BrowserTest") }.configureEach {
    dependsOn("killWebpack")
}

// Task to run the iOS app in the simulator without opening Xcode
tasks.register<Exec>("iosSimulatorRun") {
    group = "run"
    description = "Build and run the iOS app in the simulator (use -PiosDevice=\"iPhone 16 Pro\" to specify device)"

    dependsOn("linkDebugFrameworkIosSimulatorArm64")

    val projectDir = file("iosApp/iosApp.xcodeproj")
    val appName = "iosApp"
    val bundleId = "com.compiledplatforms.kmp.library.fibonacci.sample"
    val requestedDevice = project.findProperty("iosDevice") as String? ?: ""

    commandLine(
        "sh", "-c", """
            set -e
            
            # Determine which simulator to use
            if [ -n "$requestedDevice" ]; then
                SIMULATOR_ID=${'$'}(xcrun simctl list devices available | grep "$requestedDevice" | head -1 | sed -E 's/.*\(([0-9A-F-]+)\).*/\1/')
                if [ -z "${'$'}SIMULATOR_ID" ]; then
                    echo "Error: Device '$requestedDevice' not found"
                    exit 1
                fi
                SIMULATOR_NAME="$requestedDevice"
                echo "Using requested device: $requestedDevice"
            else
                # Try to find first booted simulator
                SIMULATOR_ID=${'$'}(xcrun simctl list devices | grep "(Booted)" | head -1 | sed -E 's/.*\(([0-9A-F-]+)\).*/\1/')
                
                if [ -z "${'$'}SIMULATOR_ID" ]; then
                    # No booted simulator, use first available iPhone
                    SIMULATOR_LINE=${'$'}(xcrun simctl list devices available | grep "iPhone" | head -1)
                    SIMULATOR_ID=${'$'}(echo "${'$'}SIMULATOR_LINE" | sed -E 's/.*\(([0-9A-F-]+)\).*/\1/')
                    SIMULATOR_NAME=${'$'}(echo "${'$'}SIMULATOR_LINE" | sed -E 's/^[[:space:]]*([^(]+).*/\1/' | xargs)
                    echo "Using first available simulator: ${'$'}SIMULATOR_NAME"
                else
                    SIMULATOR_LINE=${'$'}(xcrun simctl list devices | grep "${'$'}SIMULATOR_ID")
                    SIMULATOR_NAME=${'$'}(echo "${'$'}SIMULATOR_LINE" | sed -E 's/^[[:space:]]*([^(]+).*/\1/' | xargs)
                    echo "Using already booted simulator: ${'$'}SIMULATOR_NAME"
                fi
            fi
            
            # Boot if not already booted and wait for it to be ready
            BOOT_STATUS=${'$'}(xcrun simctl list devices | grep "${'$'}SIMULATOR_ID" | grep -o "(Booted)" || echo "")
            if [ -z "${'$'}BOOT_STATUS" ]; then
                echo "Booting simulator..."
                xcrun simctl boot "${'$'}SIMULATOR_ID"
                # Wait for simulator to fully boot
                for i in {1..30}; do
                    BOOT_STATUS=${'$'}(xcrun simctl list devices | grep "${'$'}SIMULATOR_ID" | grep -o "(Booted)" || echo "")
                    if [ -n "${'$'}BOOT_STATUS" ]; then
                        echo "Simulator booted successfully"
                        sleep 2
                        break
                    fi
                    sleep 1
                done
            fi
            
            # Build for generic iOS Simulator so we don't hit SDK/destination eligibility issues.
            # We install and launch on the chosen simulator via simctl below.
            echo "Building iOS app..."
            xcodebuild -project ${projectDir.absolutePath} \
                -scheme $appName \
                -configuration Debug \
                -destination "generic/platform=iOS Simulator" \
                -derivedDataPath build/ios
            
            echo "Installing app..."
            APP_PATH=${'$'}(find build/ios/Build/Products/Debug-iphonesimulator -name "*.app" | head -1)
            xcrun simctl install "${'$'}SIMULATOR_ID" "${'$'}APP_PATH"
            
            echo "Launching app..."
            xcrun simctl launch "${'$'}SIMULATOR_ID" $bundleId
            
            echo "Opening Simulator.app..."
            open -a Simulator
        """.trimIndent()
    )
}
