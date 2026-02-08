#!/usr/bin/env python3
"""
Path → platform → Gradle task resolution for KMP source sets.
Single responsibility: map paths to platforms and platforms to task lists. No git, no subprocess.
"""

import re
from pathlib import Path


def get_library_project_paths(repo_root: Path) -> list[str]:
    """
    Return Gradle project paths for all library modules (libraries/* with build.gradle.kts).
    Used to scope CI to library builds only, excluding samples.
    """
    libraries_dir = repo_root / "libraries"
    if not libraries_dir.is_dir():
        return []
    result = []
    for path in libraries_dir.iterdir():
        if path.is_dir() and (path / "build.gradle.kts").exists():
            result.append(f":libraries:{path.name}")
    return sorted(result)


def scope_tasks_to_libraries(
    tasks: list[str], library_projects: list[str]
) -> list[str]:
    """
    Prefix each task with each library project path so only library projects are built.
    E.g. ["build"] with [":libraries:example-library"] -> [":libraries:example-library:build"].
    If library_projects is empty, returns tasks unchanged (no scoping).
    """
    if not library_projects or not tasks:
        return tasks
    return [f"{proj}:{task}" for proj in library_projects for task in tasks]


# Path patterns: source set dir -> platform key(s).
# Aligned with KotlinMultiplatformSourceSetConventions (Kotlin Gradle Plugin API).
SRC_SET_PATTERNS = [
    (re.compile(r"/src/commonMain/"), {"jvm"}),
    (re.compile(r"/src/commonTest/"), {"jvm"}),
    (re.compile(r"/src/jvmMain/"), {"jvm"}),
    (re.compile(r"/src/jvmTest/"), {"jvm"}),
    (re.compile(r"/src/androidMain/"), {"android"}),
    (re.compile(r"/src/androidTest/"), {"android"}),
    (re.compile(r"/src/androidUnitTest/"), {"android"}),
    (re.compile(r"/src/androidHostTest/"), {"android"}),
    (re.compile(r"/src/androidInstrumentedTest/"), {"android"}),
    (re.compile(r"/src/androidNativeMain/"), {"android", "ios", "linuxX64", "mingwX64"}),
    (re.compile(r"/src/androidNativeTest/"), {"android", "ios", "linuxX64", "mingwX64"}),
    (re.compile(r"/src/androidNativeArm32Main/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeArm32Test/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeArm64Main/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeArm64Test/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeX64Main/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeX64Test/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeX86Main/"), {"androidNative"}),
    (re.compile(r"/src/androidNativeX86Test/"), {"androidNative"}),
    (re.compile(r"/src/appleMain/"), {"ios"}),
    (re.compile(r"/src/appleTest/"), {"ios"}),
    (re.compile(r"/src/iosMain/"), {"ios"}),
    (re.compile(r"/src/iosTest/"), {"ios"}),
    (re.compile(r"/src/iosArm64Main/"), {"ios"}),
    (re.compile(r"/src/iosArm64Test/"), {"ios"}),
    (re.compile(r"/src/iosSimulatorArm64Main/"), {"ios"}),
    (re.compile(r"/src/iosSimulatorArm64Test/"), {"ios"}),
    (re.compile(r"/src/iosX64Main/"), {"ios"}),
    (re.compile(r"/src/iosX64Test/"), {"ios"}),
    (re.compile(r"/src/macosMain/"), {"macos"}),
    (re.compile(r"/src/macosTest/"), {"macos"}),
    (re.compile(r"/src/macosArm64Main/"), {"macos"}),
    (re.compile(r"/src/macosArm64Test/"), {"macos"}),
    (re.compile(r"/src/macosX64Main/"), {"macos"}),
    (re.compile(r"/src/macosX64Test/"), {"macos"}),
    (re.compile(r"/src/tvosMain/"), {"tvos"}),
    (re.compile(r"/src/tvosTest/"), {"tvos"}),
    (re.compile(r"/src/tvosArm64Main/"), {"tvos"}),
    (re.compile(r"/src/tvosArm64Test/"), {"tvos"}),
    (re.compile(r"/src/tvosSimulatorArm64Main/"), {"tvos"}),
    (re.compile(r"/src/tvosSimulatorArm64Test/"), {"tvos"}),
    (re.compile(r"/src/tvosX64Main/"), {"tvos"}),
    (re.compile(r"/src/tvosX64Test/"), {"tvos"}),
    (re.compile(r"/src/watchosMain/"), {"watchos"}),
    (re.compile(r"/src/watchosTest/"), {"watchos"}),
    (re.compile(r"/src/watchosArm32Main/"), {"watchos"}),
    (re.compile(r"/src/watchosArm32Test/"), {"watchos"}),
    (re.compile(r"/src/watchosArm64Main/"), {"watchos"}),
    (re.compile(r"/src/watchosArm64Test/"), {"watchos"}),
    (re.compile(r"/src/watchosDeviceArm64Main/"), {"watchos"}),
    (re.compile(r"/src/watchosDeviceArm64Test/"), {"watchos"}),
    (re.compile(r"/src/watchosSimulatorArm64Main/"), {"watchos"}),
    (re.compile(r"/src/watchosSimulatorArm64Test/"), {"watchos"}),
    (re.compile(r"/src/watchosX64Main/"), {"watchos"}),
    (re.compile(r"/src/watchosX64Test/"), {"watchos"}),
    (re.compile(r"/src/jsMain/"), {"js"}),
    (re.compile(r"/src/jsTest/"), {"js"}),
    (re.compile(r"/src/wasmJsMain/"), {"wasmJs"}),
    (re.compile(r"/src/wasmJsTest/"), {"wasmJs"}),
    (re.compile(r"/src/webMain/"), {"js", "wasmJs"}),
    (re.compile(r"/src/webTest/"), {"js", "wasmJs"}),
    (re.compile(r"/src/wasmWasiMain/"), {"wasmWasi"}),
    (re.compile(r"/src/wasmWasiTest/"), {"wasmWasi"}),
    (re.compile(r"/src/linuxMain/"), {"linuxX64"}),
    (re.compile(r"/src/linuxTest/"), {"linuxX64"}),
    (re.compile(r"/src/linuxX64Main/"), {"linuxX64"}),
    (re.compile(r"/src/linuxX64Test/"), {"linuxX64"}),
    (re.compile(r"/src/linuxArm64Main/"), {"linuxArm64"}),
    (re.compile(r"/src/linuxArm64Test/"), {"linuxArm64"}),
    (re.compile(r"/src/mingwMain/"), {"mingwX64"}),
    (re.compile(r"/src/mingwTest/"), {"mingwX64"}),
    (re.compile(r"/src/mingwX64Main/"), {"mingwX64"}),
    (re.compile(r"/src/mingwX64Test/"), {"mingwX64"}),
    (re.compile(r"/src/nativeMain/"), {"ios", "linuxX64", "mingwX64"}),
    (re.compile(r"/src/nativeTest/"), {"ios", "linuxX64", "mingwX64"}),
]

TEST_SOURCE_SET_PATTERN = re.compile(r"/src/\w+Test/")

FULL_BUILD_PATTERNS = [
    re.compile(r"build\.gradle\.kts$"),
    re.compile(r"settings\.gradle\.kts$"),
    re.compile(r"gradle\.properties$"),
    re.compile(r"^gradle/"),
    re.compile(r"^build-logic/"),
]

COMPILE_TASKS_BY_PLATFORM = {
    "jvm": ["compileKotlinJvm"],
    "android": ["compileDebugKotlinAndroidMain"],
    "androidNative": ["compileKotlinAndroidNativeArm64"],
    "ios": ["compileKotlinIosSimulatorArm64"],
    "macos": ["compileKotlinMacosArm64"],
    "tvos": ["compileKotlinTvosSimulatorArm64"],
    "watchos": ["compileKotlinWatchosSimulatorArm64"],
    "js": ["compileKotlinJs"],
    "wasmJs": ["compileKotlinWasmJs"],
    "wasmWasi": ["compileKotlinWasmWasi"],
    "linuxX64": ["compileKotlinLinuxX64"],
    "linuxArm64": ["compileKotlinLinuxArm64"],
    "mingwX64": ["compileKotlinMingwX64"],
}

TEST_TASKS_BY_PLATFORM = {
    "jvm": ["jvmTest"],
    "android": ["testDebugUnitTest"],
    "androidNative": ["compileKotlinAndroidNativeArm64"],
    "ios": ["compileKotlinIosSimulatorArm64"],
    "macos": ["compileKotlinMacosArm64"],
    "tvos": ["compileKotlinTvosSimulatorArm64"],
    "watchos": ["compileKotlinWatchosSimulatorArm64"],
    "js": ["compileKotlinJs"],
    "wasmJs": ["compileKotlinWasmJs"],
    "wasmWasi": ["compileKotlinWasmWasi"],
    "linuxX64": ["compileKotlinLinuxX64"],
    "linuxArm64": ["compileKotlinLinuxArm64"],
    "mingwX64": ["compileKotlinMingwX64"],
}


def is_test_path(path: str) -> bool:
    """True if path is under a test source set (e.g. commonTest, jvmTest)."""
    path_with_slash = f"/{path}" if not path.startswith("/") else path
    return bool(TEST_SOURCE_SET_PATTERN.search(path_with_slash))


def platforms_for_path(path: str) -> set[str] | None:
    """
    Return the set of platforms affected by this path, or None if path
    triggers a full build.
    """
    path_with_slash = f"/{path}" if not path.startswith("/") else path
    for pattern in FULL_BUILD_PATTERNS:
        if pattern.search(path):
            return None
    platforms = set()
    for pattern, plats in SRC_SET_PATTERNS:
        if pattern.search(path_with_slash):
            platforms |= plats
    return platforms if platforms else set()


def platforms_for_changed_files(paths: list[str]) -> tuple[set[str], set[str]] | None:
    """
    Return (main_platforms, test_platforms) for paths, or None if full build.
    main_platforms: platforms with changes under main source sets.
    test_platforms: platforms with changes under test source sets.
    """
    main_platforms = set()
    test_platforms = set()
    for path in paths:
        plats = platforms_for_path(path)
        if plats is None:
            return None
        if not plats:
            continue
        if is_test_path(path):
            test_platforms |= plats
        else:
            main_platforms |= plats
    return (main_platforms, test_platforms)


def _tasks_for_platforms(
    platforms: set[str] | None, task_map: dict[str, list[str]]
) -> list[str]:
    if platforms is None or not platforms:
        return ["build"]
    tasks = []
    seen = set()
    for p in sorted(platforms):
        if p in task_map and p not in seen:
            tasks.extend(task_map[p])
            seen.add(p)
    return tasks if tasks else ["build"]


def gradle_test_tasks(platforms: set[str] | None) -> list[str]:
    """Return Gradle task names to run tests for the given platforms."""
    return _tasks_for_platforms(platforms, TEST_TASKS_BY_PLATFORM)


def gradle_test_tasks_by_platform(
    platforms: set[str] | None,
) -> list[tuple[str, list[str]]]:
    """
    Return one (platform_name, task_list) per platform for test runs.
    Each element is one Gradle invocation. Caller can run them in parallel.

    For platforms is None or empty: returns [("build", ["build"])] so the
    caller runs a single full-build job.
    """
    if platforms is None or not platforms:
        return [("build", ["build"])]
    result = []
    for p in sorted(platforms):
        if p in TEST_TASKS_BY_PLATFORM:
            result.append((p, list(TEST_TASKS_BY_PLATFORM[p])))
    return result if result else [("build", ["build"])]


def gradle_compile_tasks(platforms: set[str] | None) -> list[str]:
    """Return Gradle task names to compile main for the given platforms."""
    return _tasks_for_platforms(platforms, COMPILE_TASKS_BY_PLATFORM)
