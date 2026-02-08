#!/usr/bin/env python3
"""
Tests for platform_core (path → platform → task resolution).

Run from repo root: PYTHONPATH=scripts pytest scripts/tests/test_platform_core.py -v
"""

import pytest
from src.platform_core import (
    is_test_path,
    platforms_for_path,
    platforms_for_changed_files,
    gradle_test_tasks,
    gradle_test_tasks_by_platform,
    gradle_compile_tasks,
    get_library_project_paths,
    scope_tasks_to_libraries,
)


class TestPlatformsForPath:
    """Tests for path -> platform classification."""

    def test_common_main_returns_jvm(self):
        assert platforms_for_path("libraries/foo/src/commonMain/kotlin/Foo.kt") == {"jvm"}

    def test_common_test_returns_jvm(self):
        assert platforms_for_path("libraries/foo/src/commonTest/kotlin/FooTest.kt") == {"jvm"}

    def test_jvm_main_returns_jvm(self):
        assert platforms_for_path("libraries/foo/src/jvmMain/kotlin/JvmFoo.kt") == {"jvm"}

    def test_jvm_test_returns_jvm(self):
        assert platforms_for_path("libraries/foo/src/jvmTest/kotlin/JvmFooTest.kt") == {"jvm"}

    def test_android_main_returns_android(self):
        assert platforms_for_path("libraries/foo/src/androidMain/kotlin/AndroidFoo.kt") == {"android"}

    def test_android_test_returns_android(self):
        assert platforms_for_path("libraries/foo/src/androidTest/kotlin/AndroidFooTest.kt") == {"android"}

    def test_android_host_test_returns_android(self):
        assert platforms_for_path("libraries/foo/src/androidHostTest/kotlin/HostTest.kt") == {"android"}

    def test_android_unit_test_returns_android(self):
        assert platforms_for_path("libraries/foo/src/androidUnitTest/kotlin/AndroidFooTest.kt") == {"android"}

    def test_ios_main_returns_ios(self):
        assert platforms_for_path("libraries/foo/src/iosMain/kotlin/IosFoo.kt") == {"ios"}

    def test_ios_test_returns_ios(self):
        assert platforms_for_path("libraries/foo/src/iosTest/kotlin/IosFooTest.kt") == {"ios"}

    def test_js_main_returns_js(self):
        assert platforms_for_path("libraries/foo/src/jsMain/kotlin/JsFoo.kt") == {"js"}

    def test_wasm_js_main_returns_wasm_js(self):
        assert platforms_for_path("libraries/foo/src/wasmJsMain/kotlin/WasmFoo.kt") == {"wasmJs"}

    def test_wasm_js_test_returns_wasm_js(self):
        assert platforms_for_path("libraries/foo/src/wasmJsTest/kotlin/WasmFooTest.kt") == {"wasmJs"}

    def test_linux_x64_main_returns_linux_x64(self):
        assert platforms_for_path("libraries/foo/src/linuxX64Main/kotlin/LinuxFoo.kt") == {"linuxX64"}

    def test_linux_x64_test_returns_linux_x64(self):
        assert platforms_for_path("libraries/foo/src/linuxX64Test/kotlin/LinuxFooTest.kt") == {"linuxX64"}

    def test_mingw_x64_main_returns_mingw_x64(self):
        assert platforms_for_path("libraries/foo/src/mingwX64Main/kotlin/WindowsFoo.kt") == {"mingwX64"}

    def test_mingw_x64_test_returns_mingw_x64(self):
        assert platforms_for_path("libraries/foo/src/mingwX64Test/kotlin/WindowsFooTest.kt") == {"mingwX64"}

    def test_native_main_returns_all_native(self):
        assert platforms_for_path("libraries/foo/src/nativeMain/kotlin/NativeFoo.kt") == {
            "ios", "linuxX64", "mingwX64"
        }

    def test_native_test_returns_all_native(self):
        assert platforms_for_path("libraries/foo/src/nativeTest/kotlin/NativeFooTest.kt") == {
            "ios", "linuxX64", "mingwX64"
        }

    def test_apple_main_returns_ios(self):
        assert platforms_for_path("libraries/foo/src/appleMain/kotlin/AppleFoo.kt") == {"ios"}

    def test_apple_test_returns_ios(self):
        assert platforms_for_path("libraries/foo/src/appleTest/kotlin/AppleFooTest.kt") == {"ios"}

    def test_linux_main_returns_linux_x64(self):
        assert platforms_for_path("libraries/foo/src/linuxMain/kotlin/LinuxFoo.kt") == {"linuxX64"}

    def test_linux_test_returns_linux_x64(self):
        assert platforms_for_path("libraries/foo/src/linuxTest/kotlin/LinuxFooTest.kt") == {"linuxX64"}

    def test_mingw_main_returns_mingw_x64(self):
        assert platforms_for_path("libraries/foo/src/mingwMain/kotlin/MingwFoo.kt") == {"mingwX64"}

    def test_mingw_test_returns_mingw_x64(self):
        assert platforms_for_path("libraries/foo/src/mingwTest/kotlin/MingwFooTest.kt") == {"mingwX64"}

    def test_android_native_main_returns_android_and_native(self):
        assert platforms_for_path("libraries/foo/src/androidNativeMain/kotlin/AndroidNativeFoo.kt") == {
            "android", "ios", "linuxX64", "mingwX64"
        }

    def test_android_native_test_returns_android_and_native(self):
        assert platforms_for_path("libraries/foo/src/androidNativeTest/kotlin/AndroidNativeFooTest.kt") == {
            "android", "ios", "linuxX64", "mingwX64"
        }

    def test_web_main_returns_js_and_wasm_js(self):
        assert platforms_for_path("libraries/foo/src/webMain/kotlin/WebFoo.kt") == {"js", "wasmJs"}

    def test_web_test_returns_js_and_wasm_js(self):
        assert platforms_for_path("libraries/foo/src/webTest/kotlin/WebFooTest.kt") == {"js", "wasmJs"}

    def test_common_and_android_main_returns_both_main(self):
        paths = [
            "libraries/foo/src/commonMain/kotlin/Foo.kt",
            "libraries/foo/src/androidMain/kotlin/AndroidFoo.kt",
        ]
        assert platforms_for_changed_files(paths) == ({"jvm", "android"}, set())

    def test_build_gradle_triggers_full_build(self):
        assert platforms_for_path("libraries/foo/build.gradle.kts") is None

    def test_root_build_gradle_triggers_full_build(self):
        assert platforms_for_path("build.gradle.kts") is None

    def test_settings_gradle_triggers_full_build(self):
        assert platforms_for_path("settings.gradle.kts") is None

    def test_gradle_properties_triggers_full_build(self):
        assert platforms_for_path("gradle.properties") is None

    def test_gradle_dir_triggers_full_build(self):
        assert platforms_for_path("gradle/libs.versions.toml") is None

    def test_build_logic_triggers_full_build(self):
        assert platforms_for_path("build-logic/convention/build.gradle.kts") is None

    def test_unrelated_path_returns_empty_set(self):
        assert platforms_for_path("README.md") == set()

    def test_path_without_leading_slash_still_matches(self):
        assert platforms_for_path("libraries/foo/src/commonMain/kotlin/Foo.kt") == {"jvm"}


class TestIsTestPath:
    """Tests for test vs main path detection."""

    def test_common_test_is_test(self):
        assert is_test_path("libraries/foo/src/commonTest/kotlin/FooTest.kt") is True

    def test_common_main_is_not_test(self):
        assert is_test_path("libraries/foo/src/commonMain/kotlin/Foo.kt") is False

    def test_jvm_test_is_test(self):
        assert is_test_path("libraries/foo/src/jvmTest/kotlin/JvmTest.kt") is True

    def test_android_unit_test_is_test(self):
        assert is_test_path("libraries/foo/src/androidUnitTest/kotlin/Test.kt") is True


class TestPlatformsForChangedFiles:
    """Tests for aggregating (main_platforms, test_platforms) from paths."""

    def test_empty_list_returns_both_empty(self):
        assert platforms_for_changed_files([]) == (set(), set())

    def test_single_common_main_returns_jvm_main_only(self):
        assert platforms_for_changed_files(
            ["libraries/a/src/commonMain/kotlin/X.kt"]
        ) == ({"jvm"}, set())

    def test_single_common_test_returns_jvm_test_only(self):
        assert platforms_for_changed_files(
            ["libraries/a/src/commonTest/kotlin/XTest.kt"]
        ) == (set(), {"jvm"})

    def test_any_full_build_path_returns_none(self):
        assert platforms_for_changed_files([
            "libraries/a/src/commonMain/kotlin/X.kt",
            "build.gradle.kts",
        ]) is None

    def test_combined_main_platforms(self):
        assert platforms_for_changed_files([
            "libraries/a/src/commonMain/kotlin/X.kt",
            "libraries/a/src/iosMain/kotlin/Ios.kt",
        ]) == ({"jvm", "ios"}, set())

    def test_main_and_test_same_platform_returns_both(self):
        assert platforms_for_changed_files([
            "libraries/a/src/commonMain/kotlin/X.kt",
            "libraries/a/src/commonTest/kotlin/XTest.kt",
        ]) == ({"jvm"}, {"jvm"})


class TestTestTasksForPlatforms:
    """Tests for platform set -> test task list."""

    def test_none_returns_full_build(self):
        assert gradle_test_tasks(None) == ["build"]

    def test_empty_set_returns_full_build(self):
        assert gradle_test_tasks(set()) == ["build"]

    def test_jvm_returns_jvm_test(self):
        assert gradle_test_tasks({"jvm"}) == ["jvmTest"]

    def test_android_returns_unit_test(self):
        assert gradle_test_tasks({"android"}) == ["testDebugUnitTest"]

    def test_ios_returns_ios_compile(self):
        assert gradle_test_tasks({"ios"}) == ["compileKotlinIosSimulatorArm64"]

    def test_jvm_and_android_returns_both(self):
        tasks = gradle_test_tasks({"jvm", "android"})
        assert "jvmTest" in tasks
        assert "testDebugUnitTest" in tasks
        assert len(tasks) == 2


class TestCompileTasksForPlatforms:
    """Tests for platform set -> compile task list."""

    def test_none_returns_full_build(self):
        assert gradle_compile_tasks(None) == ["build"]

    def test_empty_set_returns_full_build(self):
        assert gradle_compile_tasks(set()) == ["build"]

    def test_jvm_returns_compile_jvm(self):
        assert gradle_compile_tasks({"jvm"}) == ["compileKotlinJvm"]

    def test_android_returns_android_compile(self):
        assert gradle_compile_tasks({"android"}) == ["compileDebugKotlinAndroidMain"]

    def test_ios_returns_ios_compile(self):
        assert gradle_compile_tasks({"ios"}) == ["compileKotlinIosSimulatorArm64"]

    def test_js_returns_js_compile(self):
        assert gradle_compile_tasks({"js"}) == ["compileKotlinJs"]

    def test_wasm_js_returns_wasm_js_compile(self):
        assert gradle_compile_tasks({"wasmJs"}) == ["compileKotlinWasmJs"]

    def test_linux_x64_returns_linux_x64_compile(self):
        assert gradle_compile_tasks({"linuxX64"}) == ["compileKotlinLinuxX64"]

    def test_mingw_x64_returns_mingw_x64_compile(self):
        assert gradle_compile_tasks({"mingwX64"}) == ["compileKotlinMingwX64"]

    def test_jvm_and_android_returns_both_tasks(self):
        tasks = gradle_compile_tasks({"jvm", "android"})
        assert "compileKotlinJvm" in tasks
        assert "compileDebugKotlinAndroidMain" in tasks
        assert len(tasks) == 2

    def test_all_platforms_returns_all_compile_tasks(self):
        tasks = gradle_compile_tasks(
            {"jvm", "android", "ios", "js", "wasmJs", "linuxX64", "mingwX64"}
        )
        assert "compileKotlinJvm" in tasks
        assert "compileDebugKotlinAndroidMain" in tasks
        assert "compileKotlinIosSimulatorArm64" in tasks
        assert "compileKotlinJs" in tasks
        assert "compileKotlinWasmJs" in tasks
        assert "compileKotlinLinuxX64" in tasks
        assert "compileKotlinMingwX64" in tasks
        assert len(tasks) == 7


class TestGradleTestTasksByPlatform:
    """Tests for per-platform test task list API."""

    def test_none_returns_full_build_entry(self):
        assert gradle_test_tasks_by_platform(None) == [("build", ["build"])]

    def test_empty_set_returns_full_build_entry(self):
        assert gradle_test_tasks_by_platform(set()) == [("build", ["build"])]

    def test_jvm_and_ios_returns_two_entries(self):
        result = gradle_test_tasks_by_platform({"jvm", "ios"})
        assert len(result) == 2
        by_platform = dict(result)
        assert by_platform["jvm"] == ["jvmTest"]
        assert by_platform["ios"] == ["compileKotlinIosSimulatorArm64"]

    def test_single_platform_returns_one_entry(self):
        assert gradle_test_tasks_by_platform({"jvm"}) == [("jvm", ["jvmTest"])]

    def test_unknown_platforms_only_returns_full_build(self):
        result = gradle_test_tasks_by_platform({"unknown"})
        assert result == [("build", ["build"])]

    def test_many_platforms_returns_one_entry_per_platform(self):
        result = gradle_test_tasks_by_platform({"jvm", "android", "ios"})
        assert len(result) == 3
        by_platform = dict(result)
        assert by_platform["jvm"] == ["jvmTest"]
        assert by_platform["android"] == ["testDebugUnitTest"]
        assert by_platform["ios"] == ["compileKotlinIosSimulatorArm64"]


class TestLibraryScoping:
    """Tests for library-only CI scoping."""

    def test_get_library_project_paths_empty_when_no_libraries_dir(self, tmp_path):
        assert get_library_project_paths(tmp_path) == []

    def test_get_library_project_paths_finds_libraries_with_build_gradle(self, tmp_path):
        (tmp_path / "libraries" / "example-library").mkdir(parents=True)
        (tmp_path / "libraries" / "example-library" / "build.gradle.kts").write_text("")
        assert get_library_project_paths(tmp_path) == [":libraries:example-library"]

    def test_get_library_project_paths_ignores_dirs_without_build_gradle(self, tmp_path):
        (tmp_path / "libraries" / "example-library").mkdir(parents=True)
        (tmp_path / "libraries" / "no-build").mkdir(parents=True)
        (tmp_path / "libraries" / "example-library" / "build.gradle.kts").write_text("")
        assert get_library_project_paths(tmp_path) == [":libraries:example-library"]

    def test_get_library_project_paths_sorted(self, tmp_path):
        (tmp_path / "libraries" / "b-lib").mkdir(parents=True)
        (tmp_path / "libraries" / "a-lib").mkdir(parents=True)
        (tmp_path / "libraries" / "b-lib" / "build.gradle.kts").write_text("")
        (tmp_path / "libraries" / "a-lib" / "build.gradle.kts").write_text("")
        assert get_library_project_paths(tmp_path) == [":libraries:a-lib", ":libraries:b-lib"]

    def test_scope_tasks_to_libraries_empty_projects_returns_tasks_unchanged(self):
        assert scope_tasks_to_libraries(["build"], []) == ["build"]
        assert scope_tasks_to_libraries(["jvmTest"], []) == ["jvmTest"]

    def test_scope_tasks_to_libraries_empty_tasks_returns_empty(self):
        assert scope_tasks_to_libraries([], [":libraries:example-library"]) == []

    def test_scope_tasks_to_libraries_single_library_single_task(self):
        got = scope_tasks_to_libraries(["build"], [":libraries:example-library"])
        assert got == [":libraries:example-library:build"]

    def test_scope_tasks_to_libraries_single_library_multiple_tasks(self):
        got = scope_tasks_to_libraries(
            ["compileKotlinIosSimulatorArm64", "jvmTest"],
            [":libraries:example-library"],
        )
        assert got == [
            ":libraries:example-library:compileKotlinIosSimulatorArm64",
            ":libraries:example-library:jvmTest",
        ]

    def test_scope_tasks_to_libraries_multiple_libraries(self):
        got = scope_tasks_to_libraries(
            ["build"],
            [":libraries:a-lib", ":libraries:b-lib"],
        )
        assert got == [":libraries:a-lib:build", ":libraries:b-lib:build"]
