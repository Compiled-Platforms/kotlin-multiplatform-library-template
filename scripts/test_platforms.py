#!/usr/bin/env python3
"""
Run Gradle test tasks for platforms affected by changed files.

When multiple platforms are affected, runs one Gradle invocation per platform
in parallel (bounded by --max-concurrency). First failure terminates the rest
(fail-fast) and the script exits with that failure.
"""

import argparse
import sys
from pathlib import Path

# So "from src.xxx" works when run as python3 scripts/test_platforms.py from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.touched_files import get_repo_root, get_touched_files
from src.platform_core import (
    platforms_for_changed_files,
    gradle_test_tasks_by_platform,
)
from src.gradle_runner import run_gradle
from src.parallel_runner import run_parallel_gradle, DEFAULT_MAX_CONCURRENCY


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run tests for platforms affected by changed files"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print tasks only, do not run")
    parser.add_argument("--base", default="origin/main", help="Base ref for touched files (added/updated/deleted)")
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=DEFAULT_MAX_CONCURRENCY,
        help="Max parallel Gradle runs when testing multiple platforms; fail-fast on first failure (default: %(default)s)",
    )
    args = parser.parse_args()

    cwd = get_repo_root()
    paths = get_touched_files(args.base)
    if not paths:
        return run_gradle(["build"], cwd=cwd, dry_run=args.dry_run)

    result = platforms_for_changed_files(paths)
    if result is None:
        # Gradle config changed; validate with JVM build only (no native)
        return run_gradle(["jvmTest"], cwd=cwd, dry_run=args.dry_run)

    main_platforms, test_platforms = result
    platforms_to_test = main_platforms | test_platforms

    if not platforms_to_test:
        # Touched files don't affect any platform (e.g. scripts only); validate with JVM only
        return run_gradle(["jvmTest"], cwd=cwd, dry_run=args.dry_run)

    work = gradle_test_tasks_by_platform(platforms_to_test)
    if len(work) == 1:
        _name, tasks = work[0]
        return run_gradle(tasks, cwd=cwd, dry_run=args.dry_run)
    code, failed_platform = run_parallel_gradle(
        work, cwd=cwd, max_concurrency=args.max_concurrency, dry_run=args.dry_run
    )
    if code != 0 and failed_platform:
        print(f"First failing platform: {failed_platform}", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
