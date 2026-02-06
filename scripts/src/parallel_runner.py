#!/usr/bin/env python3
"""
Run multiple Gradle invocations in parallel with bounded concurrency and fail-fast.
Single responsibility: execute N Gradle commands; supports cancellation via Popen.
"""

import subprocess
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Default cap on concurrent Gradle processes to avoid overloading the machine.
# Gradle is resource-heavy; 3 is a reasonable balance for typical dev machines.
DEFAULT_MAX_CONCURRENCY = 3


def run_single_gradle(
    tasks: list[str],
    cwd: Path,
    *,
    register_process: Callable[[subprocess.Popen], None] | None = None,
) -> tuple[bool, int]:
    """
    Run a single Gradle command in a subprocess. Returns (success, exit_code).

    Uses Popen so the caller can terminate the process (e.g. on fail-fast).
    If register_process is provided, it is called with the Popen instance as soon
    as the process is started, so the coordinator can call terminate() on it.
    """
    cmd = ["./gradlew", "--daemon"] + tasks
    proc = subprocess.Popen(cmd, cwd=cwd)
    if register_process is not None:
        register_process(proc)
    try:
        proc.wait()
        code = proc.returncode if proc.returncode is not None else -1
        return (code == 0, code)
    except Exception:
        proc.kill()
        raise


def run_parallel_gradle(
    work_items: list[tuple[str, list[str]]],
    cwd: Path,
    max_concurrency: int,
    dry_run: bool = False,
) -> tuple[int, str | None]:
    """
    Run one Gradle command per work item in parallel, with bounded concurrency.

    work_items: list of (platform_name, task_list). cwd: repo root for all runs.
    At most max_concurrency Gradle processes run at once. On first non-zero exit,
    other in-flight processes are terminated (fail-fast); exit code is non-zero.
    dry_run: print what would be run per platform and return (0, None).
    Returns (exit_code, first_failing_platform). exit_code is 0 only if all succeeded.

    Not safe to call from multiple threads concurrently (use one runner at a time).
    """
    if dry_run:
        for name, tasks in work_items:
            print(f"[dry-run] would run {name}: ./gradlew --daemon {' '.join(tasks)}")
        return (0, None)

    lock = threading.Lock()
    active_processes: list[tuple[str, subprocess.Popen]] = []
    failed = False
    first_failing_platform: str | None = None
    first_failure_code = 0

    def run_one(item: tuple[str, list[str]]) -> None:
        nonlocal failed, first_failing_platform, first_failure_code
        platform, tasks = item
        with lock:
            if failed:
                return
        def register(p: subprocess.Popen) -> None:
            with lock:
                active_processes.append((platform, p))
        success, code = run_single_gradle(tasks, cwd, register_process=register)
        with lock:
            if not success and not failed:
                failed = True
                first_failing_platform = platform
                first_failure_code = code
                for _, p in active_processes:
                    p.terminate()

    with ThreadPoolExecutor(max_workers=max_concurrency) as executor:
        futures = [executor.submit(run_one, item) for item in work_items]
        for f in as_completed(futures):
            f.result()
    return (first_failure_code if first_failing_platform is not None else 0, first_failing_platform)
