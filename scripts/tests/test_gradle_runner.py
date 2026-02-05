"""Minimal tests for gradle_runner (run_gradle with dry_run)."""

import pytest
from pathlib import Path

from src.gradle_runner import run_gradle


class TestRunGradle:
    """Tests for run_gradle."""

    def test_dry_run_returns_zero(self, tmp_path):
        rc = run_gradle(["help"], cwd=tmp_path, dry_run=True)
        assert rc == 0

    def test_dry_run_accepts_cwd(self, tmp_path):
        rc = run_gradle(["tasks"], cwd=tmp_path, dry_run=True)
        assert rc == 0
