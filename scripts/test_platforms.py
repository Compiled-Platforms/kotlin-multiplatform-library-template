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
    get_library_project_paths,
    scope_tasks_to_libraries,
    platforms_for_changed_files,
    gradle_test_tasks_by_platform,
)
from src.gradle_runner import run_gradle, resolve_library_tasks
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
    parser.add_argument(
        "--platforms",
        type=str,
        default=None,
        metavar="PLATFORMS",
        help="Comma-separated platforms to test (e.g. jvm,android). If set, only these run; others (e.g. ios, wasmJs) are skipped. Omit to test all affected platforms.",
    )
    args = parser.parse_args()

    cwd = get_repo_root()
    library_projects = get_library_project_paths(cwd)

    paths = get_touched_files(args.base)
    if not paths:
        if args.platforms:
            allowed = {p.strip().lower() for p in args.platforms.split(",") if p.strip()}
            work = gradle_test_tasks_by_platform(allowed)
            task_names = [t for _name, tlist in work for t in tlist]
            tasks = resolve_library_tasks(cwd, library_projects, task_names)
            if not tasks:
                print(f"No library tasks for platform(s): {', '.join(sorted(allowed))}", file=sys.stderr)
                return 0
        else:
            tasks = scope_tasks_to_libraries(["build"], library_projects)
        return run_gradle(tasks, cwd=cwd, dry_run=args.dry_run)

    result = platforms_for_changed_files(paths)
    if result is None:
        # Gradle config changed; validate with JVM build only (no native)
        tasks = scope_tasks_to_libraries(["jvmTest"], library_projects)
        return run_gradle(tasks, cwd=cwd, dry_run=args.dry_run)

    main_platforms, test_platforms = result
    platforms_to_test = main_platforms | test_platforms

    if args.platforms:
        allowed = {p.strip().lower() for p in args.platforms.split(",") if p.strip()}
        platforms_to_test = platforms_to_test & allowed
        if not platforms_to_test:
            platforms_to_test = allowed
        if not platforms_to_test:
            print("No platforms to run (--platforms did not match any).", file=sys.stderr)
            return 1

    if not platforms_to_test:
        # Touched files don't affect any platform (e.g. scripts only); validate with JVM only
        tasks = scope_tasks_to_libraries(["jvmTest"], library_projects)
        return run_gradle(tasks, cwd=cwd, dry_run=args.dry_run)

    work = gradle_test_tasks_by_platform(platforms_to_test)
    all_task_names = [t for _name, tlist in work for t in tlist]
    resolved = resolve_library_tasks(cwd, library_projects, all_task_names) if all_task_names else []
    work = [
        (name, [t for t in resolved if t.split(":")[-1] in tlist])
        for name, tlist in work
    ]
    work = [(name, tasks) for name, tasks in work if tasks]
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
