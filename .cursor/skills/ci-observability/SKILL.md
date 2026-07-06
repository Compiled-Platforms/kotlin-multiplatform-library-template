---
name: ci-observability
description: Make CI pipelines observable and debuggable — pipeline metrics, cost and success rate tracking, failure analysis, log navigation, local reproduction, runner diagnostics, and artifact inspection. Use when investigating CI failures, improving pipeline visibility, or setting up monitoring.
---

# CI Observability

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Principles

- A pipeline that fails without explanation wastes more time than it saves.
- Observability is not optional — it is the mechanism by which pipelines are trusted and improved.
- Every failure must be diagnosable from the logs alone, without access to the runner or re-running the job.
- Metrics without action are noise. Collect what you will respond to.

## Observability Scope

- Observability must support both real-time failure diagnosis and long-term pipeline improvement.
- CI output should answer: what ran, why it ran, what changed, what failed, and what to do next.
- Observability should reduce investigation time, not just increase available data. More data is not the goal — faster resolution is.

## Ownership

- Every workflow must have an owner responsible for failures, alerts, dashboards, and maintenance.
- Alerts must route to the responsible owner, not a generic shared channel.
- Unknown ownership is an observability defect. A pipeline without an owner has no one to fix it.

## Pipeline Metrics

Track these metrics at minimum:

- **Success rate** per workflow, per branch. Declining success rate on main is a blocking issue.
- **Total runtime** per workflow run. Increasing runtime indicates drift or new bottlenecks.
- **Job runtime** per job. Track trends to catch regressions.
- **Queue time** — time between trigger and first job start. High queue time indicates runner capacity issues.
- **Cache hit rate** per cache key. Low hit rate means caches are being invalidated too frequently or not seeded correctly.
- **Cancellation rate** and skipped-job rate — to detect wasted or misconfigured execution.
- **Failure categories** — classify failures as: test failure, build failure, infrastructure failure, timeout, dependency failure, or security failure. Mixing categories obscures root causes.

## Cost Metrics

- Track CI spend per workflow, per repository, and per team.
- Identify the most expensive workflows and optimize them first.
- Set budget alerts. An unexpected cost spike often indicates a misconfiguration (e.g., a loop, a missing cancel condition).
- Report cost per PR or per developer periodically to build cost awareness.

## Dashboards & Trends

- Dashboards should show trends, not just current status. A green dashboard that was red last week is meaningful.
- Track failure rate by workflow, job, branch, and failure category.
- Track runtime trends for critical-path jobs.
- Track flaky gate frequency over time.
- Track queue time and runner saturation over time.
- Historical trends belong in dashboards, not pull request comments.

## Traceability

- Every CI run must be traceable to: the triggering event, commit, branch, actor, workflow version, and runner.
- Every artifact must link back to the workflow run, job, source revision, and build configuration that produced it.
- Every deployment or published output must be traceable to the CI run that created it.
- Traceability must be preserved through the full pipeline, including cross-job and cross-workflow boundaries.

## Run Summaries

- Every workflow should produce a concise run summary.
- Summaries should include: status, duration, changed scope, skipped jobs, failed jobs, and artifact links.
- Failure summaries must appear before detailed logs.
- Summaries should distinguish skipped, cancelled, failed, and blocked work clearly.

## Signal Quality

- Prefer actionable signals over noisy output. Noise trains observers to ignore alerts.
- Remove or suppress repeated non-actionable warnings.
- Avoid duplicate failure reports from multiple tools covering the same concern.
- Logs must make the first meaningful failure easy to find.

## Log Design

- Every step must have a clear, descriptive name. A log full of "Run" steps is unnavigable.
- Use step grouping and log folding to separate phases within a job. Keep the collapsed view clean.
- Print a summary at the end of complex steps: what ran, what passed, what failed, and counts.
- Never print secrets, tokens, or credentials in logs under any circumstances.
- For long-running steps, print progress indicators so it is clear the step is alive.
- Emit structured output (JSON, key=value) for machine-readable data consumed by downstream steps.

## Failure Analysis

- Failures must identify the root cause, not just the symptom. "Tests failed" is not actionable. "3 tests failed in FooTest: see lines 42-67" is.
- Preserve the first failure clearly. Later cascading failures must not obscure the root cause.
- When a job fails, upload diagnostic artifacts (test reports, logs, heap dumps) automatically.
- Annotate failures inline on the PR diff when the CI platform supports it.
- Distinguish between deterministic failures (code bug) and transient failures (infrastructure) in error output.
- For flaky tests, tag them explicitly rather than silently retrying — silent retries hide reliability problems.

## Failure Triage Process

When investigating a CI failure:

1. Identify whether the failure is new or pre-existing.
2. Determine whether it is deterministic or transient (retry once to check).
3. Locate the first failing step and read its output in full.
4. Check recent changes to the failing workflow and any files it depends on.
5. Reproduce locally before attempting a fix (see Local Reproduction below).
6. Fix the root cause, not the symptom.

## Local Reproduction

- CI commands should be executable locally. Prefer `./gradlew test` over complex YAML-only logic.
- Document the commands needed to reproduce each pipeline stage in the repository README or CI documentation.
- When a CI failure cannot be reproduced locally, document the environment differences that might explain it.
- Use local runner tools to run workflows locally when the failure is environment-specific.
- Never merge a fix for a CI failure that you have not reproduced or understood.

## Runner Diagnostics

- When a job behaves unexpectedly, capture runner state: OS version, available disk, memory, installed tools.
- Log the tool versions used at the start of jobs that depend on specific versions.
- For self-hosted runners, maintain a health dashboard. Unhealthy runners must be taken out of rotation immediately.
- Check runner logs when jobs hang without producing output — the issue is often at the infrastructure level.

## Artifact Inspection

- Upload build outputs, test reports, and logs as artifacts on failure.
- Structure artifact directories so related files are grouped (e.g., `test-results/`, `coverage/`, `logs/`).
- Name artifacts to include context: job name, run number, platform.
- Retain failure artifacts long enough for investigation — set a retention policy.
- For release pipelines, retain all artifacts until the release is confirmed healthy.

## Data Retention

- Define retention policies for logs, artifacts, test reports, metrics, and release evidence.
- Retain release artifacts, provenance records, and security evidence longer than routine PR diagnostics.
- Retention policies should balance investigation needs, compliance requirements, storage cost, and privacy.
- Document retention policies explicitly — do not rely on platform defaults.

## Alerting

- Alert on main branch pipeline failures immediately. A broken main blocks everyone.
- Alert on sustained success rate degradation (e.g., below 90% over 24 hours).
- Alert on unexpected cost spikes.
- Alerts must be actionable, routed to the responsible owner, and severity-based.
- Alert fatigue is a CI reliability problem. An alert that fires too often will be ignored.
