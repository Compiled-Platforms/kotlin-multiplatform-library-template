"""Pytest conftest: ensure scripts dir is on sys.path so tests can import from src."""
import sys
from pathlib import Path

import pytest

_scripts_dir = Path(__file__).resolve().parent.parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))


@pytest.fixture(scope="session")
def repo_root():
    """Repo root path with gradlew; skip if not available."""
    try:
        from src.touched_files import get_repo_root
        root = get_repo_root()
        if not (root / "gradlew").exists():
            pytest.skip("gradlew not found at repo root")
        return root
    except Exception as e:
        pytest.skip(f"repo root unavailable: {e}")
