"""Tests for parallel_runner (single-process runner and cancellation)."""

import threading
import time
from unittest.mock import patch

import pytest

from src import parallel_runner
from src.parallel_runner import run_parallel_gradle, run_single_gradle


class TestRunSingleGradle:
    """Tests for run_single_gradle."""

    def test_success_returns_true_and_zero(self, repo_root):
        success, code = run_single_gradle(["help"], repo_root)
        assert success is True
        assert code == 0

    def test_failure_returns_false_and_nonzero(self, repo_root):
        success, code = run_single_gradle(["noSuchTask12345"], repo_root)
        assert success is False
        assert code != 0

    def test_process_can_be_terminated_from_other_thread(self, repo_root):
        procs = []
        result_holder = []

        def run():
            success, code = run_single_gradle(
                ["tasks"],
                repo_root,
                register_process=lambda p: procs.append(p),
            )
            result_holder.append((success, code))

        t = threading.Thread(target=run)
        t.start()
        time.sleep(1.0)
        assert len(procs) == 1
        procs[0].terminate()
        t.join(timeout=10)
        assert not t.is_alive()
        assert procs[0].poll() is not None


class TestRunParallelGradle:
    """Tests for run_parallel_gradle (bounded concurrency, fail-fast)."""

    def test_all_succeed_returns_zero(self, repo_root):
        work = [("a", ["help"]), ("b", ["help"])]
        code, failed_platform = run_parallel_gradle(work, repo_root, max_concurrency=2)
        assert code == 0
        assert failed_platform is None

    def test_first_failure_returns_nonzero_and_terminates_others(self, repo_root):
        work = [
            ("ok", ["help"]),
            ("fail", ["noSuchTask12345"]),
            ("ok2", ["help"]),
        ]
        code, failed_platform = run_parallel_gradle(work, repo_root, max_concurrency=3)
        assert code != 0
        assert failed_platform is not None

    def test_bounded_concurrency_at_most_max_workers(self, repo_root):
        real_run = run_single_gradle
        concurrency_lock = threading.Lock()
        current = 0
        max_seen = [0]

        def counting_run(*args, **kwargs):
            with concurrency_lock:
                nonlocal current
                current += 1
                max_seen[0] = max(max_seen[0], current)
            try:
                return real_run(*args, **kwargs)
            finally:
                with concurrency_lock:
                    current -= 1

        work = [("p1", ["help"]), ("p2", ["help"]), ("p3", ["help"])]
        with patch.object(parallel_runner, "run_single_gradle", counting_run):
            run_parallel_gradle(work, repo_root, max_concurrency=2)
        assert max_seen[0] <= 2

    def test_dry_run_returns_zero_and_prints(self, repo_root, capsys):
        work = [("jvm", ["jvmTest"]), ("ios", ["compileKotlinIosSimulatorArm64"])]
        code, failed_platform = run_parallel_gradle(
            work, repo_root, max_concurrency=2, dry_run=True
        )
        assert code == 0
        assert failed_platform is None
        out = capsys.readouterr().out
        assert "[dry-run]" in out
        assert "jvm" in out
        assert "ios" in out

    def test_empty_work_returns_zero(self, repo_root):
        code, failed_platform = run_parallel_gradle(
            [], repo_root, max_concurrency=2
        )
        assert code == 0
        assert failed_platform is None
