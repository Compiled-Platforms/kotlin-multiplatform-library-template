"""Minimal tests for gradle_runner (run_gradle with dry_run, resolve_library_tasks)."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from src.gradle_runner import run_gradle, resolve_library_tasks


class TestRunGradle:
    """Tests for run_gradle."""

    def test_dry_run_returns_zero(self, tmp_path):
        rc = run_gradle(["help"], cwd=tmp_path, dry_run=True)
        assert rc == 0

    def test_dry_run_accepts_cwd(self, tmp_path):
        rc = run_gradle(["tasks"], cwd=tmp_path, dry_run=True)
        assert rc == 0


class TestResolveLibraryTasks:
    """Tests for resolve_library_tasks (mocked subprocess)."""

    def test_empty_task_names_returns_empty(self, tmp_path):
        assert resolve_library_tasks(tmp_path, [":libraries:example-library"], []) == []

    def test_empty_library_projects_returns_empty(self, tmp_path):
        assert resolve_library_tasks(tmp_path, [], ["jvmTest"]) == []

    def test_filters_by_library_prefix_and_task_name(self, tmp_path):
        output = """
:libraries:example-library:jvmTest - Run unit tests
:libraries:example-library:build - Build
:samples:example-library:jvmTest - Run sample tests
:libraries:other-lib:jvmTest - Run unit tests
        """
        with patch("src.gradle_runner.subprocess.run") as m:
            m.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=output, stderr=""
            )
            result = resolve_library_tasks(
                tmp_path,
                [":libraries:example-library"],
                ["jvmTest"],
            )
        assert result == [":libraries:example-library:jvmTest"]

    def test_returns_multiple_matching_tasks(self, tmp_path):
        output = """
:libraries:example-library:jvmTest - Run
:libraries:example-library:testAndroid - Run
:libraries:example-library:build - Build
        """
        with patch("src.gradle_runner.subprocess.run") as m:
            m.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=output, stderr=""
            )
            result = resolve_library_tasks(
                tmp_path,
                [":libraries:example-library"],
                ["jvmTest", "testAndroid"],
            )
        assert result == [
            ":libraries:example-library:jvmTest",
            ":libraries:example-library:testAndroid",
        ]

    def test_raises_on_nonzero_exit_code(self, tmp_path):
        with patch("src.gradle_runner.subprocess.run") as m:
            m.return_value = subprocess.CompletedProcess(
                args=[], returncode=1, stdout="", stderr="No JDK found"
            )
            with pytest.raises(RuntimeError) as exc_info:
                resolve_library_tasks(
                    tmp_path,
                    [":libraries:example-library"],
                    ["jvmTest"],
                )
        assert "exit 1" in str(exc_info.value)
        assert "No JDK found" in str(exc_info.value)

    def test_ignores_malformed_lines(self, tmp_path):
        output = """
:libraries:example-library:jvmTest - Run
no dash here
:lib:short - Skip
:libraries:example-library:jvmTest - Duplicate
        """
        with patch("src.gradle_runner.subprocess.run") as m:
            m.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=output, stderr=""
            )
            result = resolve_library_tasks(
                tmp_path,
                [":libraries:example-library"],
                ["jvmTest"],
            )
        assert result == [":libraries:example-library:jvmTest"]
