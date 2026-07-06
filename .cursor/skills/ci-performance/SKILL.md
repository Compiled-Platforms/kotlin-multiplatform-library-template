---
name: ci-performance
description: Optimize CI pipelines for speed and cost — caching strategy, artifact reuse, parallel execution, incremental builds, selective execution, and build reuse. Use when a pipeline is too slow, too expensive, or needs efficiency improvements.
---

# CI Performance

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Principles

- Every second of CI time has a cost: developer wait time and infrastructure spend. Both matter.
- Measure before optimizing. Identify the actual bottleneck — don't guess.
- The fastest work is work that doesn't run. Skip before you speed up.
- Never trade correctness for speed. A cached result that might be wrong is worse than no cache.

## Optimization Order

Optimize in this sequence — do not skip ahead:

1. **Skip unnecessary work** — path filters, branch conditions, cancellation
2. **Remove duplicate work** — build once, reuse artifacts
3. **Shorten the critical path** — identify and attack the longest sequential chain
4. **Parallelize** — fan out independent jobs
5. **Cache** — cache expensive-to-recreate outputs
6. **Upgrade runners** — faster hardware is the last resort, not the first

Prefer structural improvements over faster hardware. Do not add caching or parallelism until the pipeline shape is correct.

## Measurement & Metrics

- Track duration per workflow, job, and step over time. Regressions must be treated as engineering regressions.
- Track queue time separately from execution time — they have different root causes.
- Track cache hit rate, cache restore time, and cache save time per cache key.
- Track artifact upload and download time.
- Track cost per workflow and cost per pull request.
- Identify the critical path for every pipeline. Optimizing off-path jobs does not reduce total pipeline time.

## Selective Execution

- Do not run jobs when their inputs haven't changed. Use path filters at the workflow level.
- Do not run jobs whose outputs are already valid. Check artifact existence before rebuilding.
- Skip downstream jobs when upstream validation fails — don't run tests if the build fails.
- Cancel in-progress pipeline runs when a new commit is pushed to the same branch.
- Run expensive jobs only for relevant changes, protected branches, release candidates, or explicit manual requests.

## Expensive Job Gating

- Gate expensive jobs behind cheap validation before executing them.
- Run smoke tests before full integration, hardware, emulator, or end-to-end test suites.
- Do not run deployment-like or packaging work until build and validation have passed.
- Prefer a fast representative subset of tests on PRs; reserve the full suite for main, nightly, or release workflows.

## Parallel Execution

- Identify all jobs that have no shared dependencies and run them concurrently.
- Split test suites across multiple jobs using sharding when total test runtime exceeds acceptable feedback time.
- Run platform-specific builds in parallel using matrix strategies.
- Use fan-out patterns to parallelize independent work as early as possible in the pipeline.

## Incremental Builds

- Configure build tools to detect and skip unchanged inputs.
- Use content-addressed caching where possible — cache keys based on input hashes, not timestamps.
- Ensure build tools write outputs atomically to avoid partial cache entries.
- Validate that incremental builds produce identical outputs to clean builds periodically.

## Incremental Testing

- Run only tests affected by changed code when the build system supports it.
- Always run the full test suite on the main branch and before releases, regardless of what changed.
- Never skip tests on release branches or release tags to save time.

## Cache Strategy

- Cache everything that is expensive to recreate: dependencies, compiled outputs, toolchains, downloaded tools.
- Cache keys must capture all inputs that affect the cached output. An incomplete key produces incorrect cache hits.
- Include OS, tool version, and a hash of the relevant lock file or config in every cache key.
- Add a fallback key that restores a partial cache when an exact match is unavailable — a warm partial cache is better than a cold start.
- Validate cache correctness periodically by running a clean build and comparing outputs.
- Invalidate caches eagerly when dependency versions change.
- Never cache outputs that include secrets, tokens, or environment-specific state.

## Cache Tradeoffs

- A cache is only useful when restore time plus save time is cheaper than recomputing the output. Measure both.
- Avoid caching small or cheap-to-recreate outputs — the overhead may exceed the savings.
- Avoid overly broad cache keys that cause stale or incorrect hits.
- Avoid overly narrow cache keys that prevent reuse across branches or jobs.
- Do not save caches from failed or partial builds unless the cache format is explicitly safe to restore from an incomplete state.

## Cache Sharing

- Share caches across branches using a common base key seeded from the default branch.
- PR branches benefit most from a cache seeded by the base branch.
- Avoid sharing caches across incompatible environments (different OS, different tool versions).

## Matrix Optimization

- Keep matrices limited to meaningful compatibility dimensions.
- Do not multiply dimensions unless every combination provides useful confidence.
- Matrices should represent the same work across varying dimensions — not a mix of build types, docs, and benchmarks in one grid.
- Run the smallest useful matrix on pull requests. Run the full matrix on main, nightly, or release workflows.
- Exclude unsupported or redundant matrix combinations explicitly rather than letting them fail at runtime.
- Avoid large matrices on expensive runners — cost scales multiplicatively.

## Dependency Installation

- Prefer lockfile-based dependency installs. Never install from floating version ranges in CI.
- Prefer package-manager-native caches over generic directory caches when available.
- Avoid reinstalling dependencies independently in multiple jobs when a shared artifact or cache is safer.
- Separate dependency resolution from build execution when it improves reuse and diagnostics.

## Repository Access

- Fetch only the history required by the job. Shallow clones are faster than full history for most CI tasks.
- Avoid full-depth checkout unless versioning, changelog, diff, or tag logic requires it.
- Use sparse checkout when a job only needs part of a large repository.
- Avoid initializing submodules unless the job requires them.

## Artifact Strategy

- Build once, upload the artifact, download in downstream jobs. Never rebuild the same artifact twice.
- Give artifacts descriptive names that include the build context (platform, variant, commit SHA).
- Set artifact retention policies. Keep release artifacts indefinitely; keep CI artifacts for days, not weeks.
- Upload artifacts from failed builds when they contain diagnostic information useful for debugging.
- Every artifact should be traceable to the exact source revision, build configuration, and pipeline that created it.

## Runner Strategy

- Use self-hosted runners when workloads are frequent, long-running, hardware-dependent, or require preinstalled toolchains that are expensive to install at job start.
- Use hosted runners when workloads are infrequent, security isolation is more important, or maintenance cost would exceed the minute savings.
- Keep self-hosted runners ephemeral where possible to avoid hidden state and cross-build contamination.
- Benchmark runner changes before standardizing them. Measure actual impact, not assumed impact.
- Use the cheapest runner class that meets the job's requirements. Right-size before upgrading.

## Cost Optimization

- Monitor spend per workflow. Identify and address workflows with disproportionate cost.
- Move non-urgent work (nightly scans, documentation generation) to scheduled workflows during off-peak hours.
- Avoid unnecessary matrix expansions on expensive runners.
- Set timeouts on all jobs to prevent runaway processes from consuming runner minutes indefinitely.
