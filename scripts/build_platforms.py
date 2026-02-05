#!/usr/bin/env python3
"""
Run Gradle compile tasks for platforms where main code changed.
Single responsibility: execute build (compile) only.
"""

import argparse
import sys
from pathlib import Path

# So "from src.xxx" works when run as python3 scripts/build_platforms.py from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.touched_files import get_repo_root, get_touched_files
from src.platform_core import platforms_for_changed_files, gradle_compile_tasks
from src.gradle_runner import run_gradle


def run(main_platforms: set[str], dry_run: bool = False) -> int:
    """Run compile tasks for the given platforms. Returns Gradle exit code."""
    tasks = gradle_compile_tasks(main_platforms)
    return run_gradle(tasks, cwd=get_repo_root(), dry_run=dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run build for platforms where main code changed"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print tasks only, do not run")
    parser.add_argument("--base", default="origin/main", help="Base ref for touched files (added/updated/deleted)")
    args = parser.parse_args()

    paths = get_touched_files(args.base)
    if not paths:
        return run_gradle(["build"], cwd=get_repo_root(), dry_run=args.dry_run)

    result = platforms_for_changed_files(paths)
    if result is None:
        return 0

    main_platforms, _test_platforms = result

    if not main_platforms:
        return 0

    return run(main_platforms, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
