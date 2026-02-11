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


def resolve_library_tasks(
    cwd: Path, library_projects: list[str], task_names: list[str]
) -> list[str]:
    """
    Return full task paths (e.g. :libraries:core:jvmTest) that exist in Gradle,
    are under one of library_projects, and whose task name is in task_names.
    Uses `gradlew tasks --all` so no source-dir list is maintained.
    """
    if not task_names or not library_projects:
        return []
    lib_prefixes = tuple(f"{lp.lstrip(':')}:" for lp in library_projects)
    task_set = set(task_names)
    result = subprocess.run(
        ["./gradlew", "--daemon", "tasks", "--all", "--no-configuration-cache", "-q"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        msg = f"gradlew tasks --all failed (exit {result.returncode})"
        if stderr:
            msg += f": {stderr[:500]}" + ("..." if len(stderr) > 500 else "")
        raise RuntimeError(msg)
    out = (result.stdout or "") + (result.stderr or "")
    tasks = []
    for line in out.splitlines():
        if " - " not in line:
            continue
        path, _ = line.split(" - ", 1)
        path = path.strip().lstrip(":")
        if not path or path.count(":") < 2:
            continue
        if not any(path.startswith(prefix) for prefix in lib_prefixes):
            continue
        name = path.split(":")[-1]
        if name not in task_set:
            continue
        tasks.append(":" + path)
    return sorted(set(tasks))
