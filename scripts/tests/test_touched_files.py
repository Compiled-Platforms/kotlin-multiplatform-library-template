"""Minimal tests for touched_files (get_repo_root, get_touched_files)."""

import pytest
from pathlib import Path

from src.touched_files import get_repo_root, get_touched_files


class TestGetRepoRoot:
    """Tests for get_repo_root."""

    def test_returns_path(self):
        root = get_repo_root()
        assert isinstance(root, Path)
        assert root.is_absolute() or root == Path.cwd()

    def test_contains_gradle_wrapper_when_in_repo(self):
        root = get_repo_root()
        if (root / "gradlew").exists():
            assert (root / "gradlew").is_file()


class TestGetTouchedFiles:
    """Tests for get_touched_files."""

    def test_accepts_base_ref_and_optional_repo_root(self):
        result = get_touched_files("origin/main")
        assert isinstance(result, list)
        assert all(isinstance(p, str) for p in result)

    def test_with_explicit_repo_root(self):
        root = get_repo_root()
        result = get_touched_files("origin/main", repo_root=root)
        assert isinstance(result, list)
