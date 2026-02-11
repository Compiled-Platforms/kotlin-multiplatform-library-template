"""Integration tests for test_platforms.py wiring (parallel vs single vs full build)."""

import sys
from pathlib import Path
from unittest.mock import patch

# Ensure scripts dir is on path so we can import test_platforms.
_scripts_dir = Path(__file__).resolve().parent.parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))


def test_dry_run_multiple_platforms_shows_per_platform_lines(repo_root, capsys):
    """With changed files that touch jvm and ios, dry-run prints one line per platform."""
    import test_platforms as tp
    paths = [
        "libraries/foo/src/commonMain/kotlin/F.kt",
        "libraries/foo/src/iosMain/kotlin/F.kt",
    ]
    with patch.object(tp, "get_touched_files", return_value=paths):
        with patch.object(tp, "get_repo_root", return_value=repo_root):
            with patch.object(sys, "argv", ["test_platforms.py", "--dry-run"]):
                code = tp.main()
    assert code == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out
    assert "jvm" in out
    assert "ios" in out


def test_dry_run_single_platform_uses_single_invocation(repo_root, capsys):
    """With only jvm changes, dry-run prints one would-run line (no per-platform)."""
    import test_platforms as tp
    paths = ["libraries/foo/src/commonMain/kotlin/F.kt"]
    with patch.object(tp, "get_touched_files", return_value=paths):
        with patch.object(tp, "get_repo_root", return_value=repo_root):
            with patch.object(sys, "argv", ["test_platforms.py", "--dry-run"]):
                code = tp.main()
    assert code == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out
    assert "jvmTest" in out or "build" in out


def test_empty_platforms_returns_error(repo_root, capsys):
    """--platforms= or --platforms=,  (empty) yields exit 1."""
    import test_platforms as tp
    with patch.object(tp, "get_touched_files", return_value=[]):
        with patch.object(tp, "get_repo_root", return_value=repo_root):
            with patch.object(sys, "argv", ["test_platforms.py", "--platforms="]):
                code = tp.main()
    assert code == 1
    err = capsys.readouterr().err
    assert "no valid platforms" in err.lower()
