#!/usr/bin/env python3
"""
Discover touched file paths (git diff) and repository root.
Touched = added, updated, or deleted between base_ref and HEAD.
Single responsibility: VCS/repo discovery for pre-push scripts.
"""

import subprocess
from pathlib import Path


def get_repo_root() -> Path:
    """Return the repository root directory."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return Path.cwd()
    return Path(result.stdout.strip())


def get_touched_files(base_ref: str = "origin/main", repo_root: Path | None = None) -> list[str]:
    """Return paths that differ between base_ref and HEAD (added, updated, or deleted)."""
    cwd = repo_root if repo_root is not None else get_repo_root()
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return []
    return [p.strip() for p in result.stdout.strip().splitlines() if p.strip()]
