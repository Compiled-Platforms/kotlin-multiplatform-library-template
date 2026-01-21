# Dependency Report

**Generated**: 2026-01-20 18:46:36

This document lists all dependencies defined in `gradle/libs.versions.toml`.

## Versions

| Name | Version |
|------|---------|
| **Agp** | `8.13.0` |
| **Android Compilesdk** | `36` |
| **Android Minsdk** | `24` |
| **Binarycompatibilityvalidator** | `0.18.1` |
| **Detekt** | `2.0.0-alpha.1` |
| **Dokka** | `2.1.0` |
| **Kotest** | `6.1.0` |
| **Kotlin** | `2.3.0` |
| **Kotlinx Coroutines** | `1.10.2` |
| **Kotlinx Datetime** | `0.6.1` |
| **Kotlinx Serialization** | `1.8.0` |
| **Kover** | `0.9.4` |
| **Mokkery** | `3.1.1` |
| **Turbine** | `1.2.1` |
| **Vanniktechmavenpublish** | `0.34.0` |

## Libraries

| Library | Module | Version |
|---------|--------|---------|
| **Android Gradle Plugin** | `com.android.tools.build:gradle` | → `agp` |
| **Binary Compatibility Validator** | `org.jetbrains.kotlinx:binary-compatibility-validator-gradle-plugin` | → `binaryCompatibilityValidator` |
| **Detekt Gradle Plugin** | `dev.detekt:detekt-gradle-plugin` | → `detekt` |
| **Dokka Gradle Plugin** | `org.jetbrains.dokka:dokka-gradle-plugin` | → `dokka` |
| **Kotest Assertions Core** | `io.kotest:kotest-assertions-core` | → `kotest` |
| **Kotest Property** | `io.kotest:kotest-property` | → `kotest` |
| **Kotlin Gradle Plugin** | `org.jetbrains.kotlin:kotlin-gradle-plugin` | → `kotlin` |
| **Kotlin Test** | `org.jetbrains.kotlin:kotlin-test` | → `kotlin` |
| **Kotlinx Coroutines Core** | `org.jetbrains.kotlinx:kotlinx-coroutines-core` | → `kotlinx-coroutines` |
| **Kotlinx Coroutines Test** | `org.jetbrains.kotlinx:kotlinx-coroutines-test` | → `kotlinx-coroutines` |
| **Kotlinx Datetime** | `org.jetbrains.kotlinx:kotlinx-datetime` | → `kotlinx-datetime` |
| **Kotlinx Serialization Json** | `org.jetbrains.kotlinx:kotlinx-serialization-json` | → `kotlinx-serialization` |
| **Mokkery Runtime** | `dev.mokkery:mokkery-runtime` | → `mokkery` |
| **Turbine** | `app.cash.turbine:turbine` | → `turbine` |
| **Vanniktech Maven Publish Plugin** | `com.vanniktech:gradle-maven-publish-plugin` | → `vanniktechMavenPublish` |

## Plugins

| Plugin | ID | Version |
|--------|----|---------| 
| **Android Kotlin Multiplatform Library** | `com.android.kotlin.multiplatform.library` | → `agp` |
| **Binarycompatibilityvalidator** | `org.jetbrains.kotlinx.binary-compatibility-validator` | → `binaryCompatibilityValidator` |
| **Detekt** | `dev.detekt` | → `detekt` |
| **Dokka** | `org.jetbrains.dokka` | → `dokka` |
| **Kotlinmultiplatform** | `org.jetbrains.kotlin.multiplatform` | → `kotlin` |
| **Kotlinx Serialization** | `org.jetbrains.kotlin.plugin.serialization` | → `kotlin` |
| **Kover** | `org.jetbrains.kotlinx.kover` | → `kover` |
| **Mokkery** | `dev.mokkery` | → `mokkery` |
| **Vanniktech Mavenpublish** | `com.vanniktech.maven.publish` | → `vanniktechMavenPublish` |

---

## Version References

Entries marked with `→ version-name` reference the version defined in the `[versions]` section.

## Updating Dependencies

See [Dependency Updates](docs/docs/development/dependency-updates.md) for information on keeping dependencies up-to-date.
