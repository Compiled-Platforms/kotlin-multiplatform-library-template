#!/usr/bin/env python3
"""
Run Gradle with a given task list.
Single responsibility: execute ./gradlew; no path or platform logic.
"""

import subprocess
from pathlib import Path


def run_gradle(tasks: list[str], cwd: Path, dry_run: bool = False) -> int:
    """Run ./gradlew with the given tasks. Caller provides cwd. Return exit code."""
    cmd = ["./gradlew", "--daemon"] + tasks
    if dry_run:
        print(f"[dry-run] would run: {' '.join(cmd)}")
        return 0
    return subprocess.run(cmd, cwd=cwd).returncode
