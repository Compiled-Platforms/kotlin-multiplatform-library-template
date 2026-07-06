---
name: ci-workflow
description: Design and architect CI pipelines — workflow structure, job design, dependency graphs, matrix strategies, conditional execution, and monorepo/multi-repo CI patterns. Use when creating or refactoring CI workflows, designing job dependencies, or structuring pipeline stages.
---

# CI Workflow Design

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Pipeline Architecture

- A pipeline is a directed acyclic graph of jobs. Design the graph explicitly — don't let it grow by accident.
- Stages should flow: validate → build → test → package → deploy. Do not bypass required validation stages to reduce execution time.
- Each stage gates the next. Only work that passes a stage proceeds to the next.
- Keep the critical path short. The wall-clock time of a pipeline is determined by its longest sequential chain.
- Pipelines should produce artifacts, not side effects. Side effects (publishing, deployment, notifications) belong in dedicated downstream workflows or stages. This keeps earlier stages deterministic and enables build-once, deploy-many.

## Workflow Design

- One workflow = one concern. A workflow that builds, tests, publishes, and notifies is four workflows.
- "Concern" is architectural, not the number of jobs. Examples of concerns: PR Validation, Nightly Validation, Release, Deployment, Dependency Updates.
- Trigger selection is part of the design. Choose events (`push`, `pull_request`, `workflow_dispatch`, `schedule`) based on what the workflow actually needs to know.
- Use path filters to prevent workflows from running when no relevant files changed.
- Use branch filters to restrict workflows to branches where they make sense.
- Prefer `pull_request` triggers over `push` for feedback workflows — they run before code reaches the base branch.
- Scheduled workflows must have owners. If no one is watching a scheduled run, it should not exist.

## Job Design

- Each job must have a single, clearly named responsibility.
- Job names must describe what the job does, not where it runs.
- Jobs that can run independently must not be serialized. Unnecessary `needs` relationships are a performance defect.
- Jobs should declare only the dependencies they actually require.
- Jobs should communicate only through declared outputs, artifacts, or caches. Never rely on implicit shared state between jobs.
- Keep jobs small enough that a failure message points to the cause without requiring log archaeology.

## Step Design

- When applicable, steps should generally follow: setup → validate → execute → report.
- Each step must have a clear, descriptive name. Avoid default names like "Run" or "Execute".
- Validate inputs and preconditions in early steps before invoking expensive tools.
- Steps that can fail without blocking the job must use `continue-on-error: true` at the step level, never at the job level for reusable workflow calls.
- Never suppress errors silently. If a step uses `continue-on-error`, document why.

## Dependency Graph Optimization

- Map out the dependency graph before writing any workflow YAML.
- Identify which jobs can run in parallel and which must be sequential.
- Every dependency edge should have a clear business or technical justification. Dependency creep serializes pipelines silently.
- Fan-out early: kick off all independent jobs as soon as their inputs are ready.
- Fan-in late: only aggregate results when all parallel branches have completed.
- Avoid diamond dependencies where possible — they increase coordination overhead.

## Fan-Out / Fan-In

- Fan-out: a single upstream job triggers multiple independent downstream jobs in parallel.
- Fan-in: a downstream job waits for multiple upstream jobs via `needs: [job-a, job-b, ...]`.
- Use fan-out for: platform-specific builds, test sharding, multi-target compilation.
- Use fan-in for: aggregated reports, release gates, publishing that requires all platforms.

## Matrix Strategies

- Use matrices to run the same work across multiple dimensions (OS, language version, target platform).
- Keep matrix dimensions orthogonal — each axis should vary independently.
- Prefer splitting fundamentally different work into separate jobs rather than expanding a matrix. A matrix should represent the same work across varying dimensions, not a mix of build types, docs, and benchmarks in one grid.
- Exclude invalid combinations explicitly rather than letting them fail at runtime.
- Fail-fast on matrices when any failure invalidates the others. Disable fail-fast when failures are independent.
- Avoid large matrices on expensive runners — cost scales multiplicatively.

## Conditional Execution

- Gate expensive jobs behind cheap validation jobs using `needs` + `if`.
- Use `if: always()` only for cleanup or reporting steps that must run regardless of outcome.
- Avoid complex inline expressions in `if:` conditions — extract them to job outputs for readability.
- Skip entire jobs when their inputs haven't changed using path filters or explicit conditions.

## Concurrency

- Only one workflow should modify a shared resource (registry, environment, deployment target) at a time. Serialize access with concurrency groups.
- Cancel in-progress runs for the same branch when a new push arrives. Wasted compute on obsolete runs is avoidable.
- Allow concurrent execution when jobs are independent — do not apply concurrency limits where they are not needed.
- Serialize deployments to the same environment. Concurrent deployments to the same target cause race conditions.
- Use concurrency to reduce wasted compute. Do not use it to enforce business logic — that belongs in job conditions.
- When a workflow handles both `pull_request` and `push` triggers, use a conditional group key: group by `github.ref` for pull requests (so rapid pushes cancel the stale run) and by `github.run_id` for push events to protected branches (so every push completes and no validated commit range is skipped). Example: `group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && github.ref || github.run_id }}`

## Monorepo CI

- In a monorepo, not every job should run for every change. Use path filters per workflow.
- Structure workflows by affected module, not by language or tool.
- Shared infrastructure changes (build-logic, CI config, root build files) should trigger a full pipeline run.
- Module-specific changes should trigger only that module's build and test jobs.
- Shared modules should expose affected-module information so downstream workflows can make deterministic execution decisions without duplicating change detection logic.
- Provide a way to run the full pipeline manually for release validation.

## Multi-Repository CI

- Define the contract between repositories explicitly — which artifacts, which versions, which events trigger downstream pipelines.
- Use immutable artifact references (commit SHA, content hash) when triggering cross-repo builds.
- Avoid polling for cross-repo changes — use webhook events or repository dispatch.
- Document inter-repository dependencies so pipeline ownership is clear.
