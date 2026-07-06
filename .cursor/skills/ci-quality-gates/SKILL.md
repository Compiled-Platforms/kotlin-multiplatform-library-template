---
name: ci-quality-gates
description: Configure and maintain CI quality gates — formatting, linting, static analysis, dependency/secret/license scanning, security scanning, binary size checks, performance regression detection, and API compatibility validation. Use when adding or improving automated quality checks in a pipeline.
---

# CI Quality Gates

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Gate Philosophy

- Every quality gate should answer a single, objective question.
- A gate should be deterministic — the same input must always produce the same result.
- A gate should be independently executable and independently maintainable.
- A failure in one gate should not prevent independent gates from producing results whenever practical.
- Every gate should have a clearly defined owner.
- Remove gates that no longer provide meaningful value. An unused or ignored gate is noise.

## Quality Gate Lifecycle

- Introduce new gates in advisory mode when appropriate, then promote them to blocking once they are stable and trusted.
- Review gates periodically to ensure they continue to provide value.
- Remove obsolete or redundant gates promptly.
- Changes to blocking gates should be communicated to the team before enforcement begins.

## Failure Policy

- Every failing gate must block only when its failure represents a genuine quality risk.
- Failures must clearly identify the root cause and the action required to resolve them.
- Avoid cascading failures that obscure the first failure — report the root cause, not symptoms.
- Never retry deterministic failures automatically. Retrying a reproducible failure wastes time and hides the problem.
- Quality gates should fail closed for quality violations and fail explicitly for infrastructure problems. Never report an infrastructure failure as a quality failure.

## Flaky Gates

- Quality gates must be deterministic and repeatable.
- Flaky gates are defects in the CI system, not acceptable background noise.
- Never normalize flaky gates by silently retrying or ignoring intermittent failures.
- Remove or quarantine unreliable gates until they are fixed.
- Track flaky gate frequency as an engineering metric. A rising flaky rate signals systemic CI health issues.

## Gate Scope

- Run only the gates relevant to the change whenever correctness is preserved.
- Lightweight gates (formatting, lint) should run on every pull request.
- Expensive gates (full security scans, integration tests, benchmarks) may be limited to protected branches, nightly builds, or release pipelines.
- Release pipelines must execute every required release gate regardless of change scope.

## Baselines

- Baselines are temporary tools for managing existing technical debt, not permanent fixtures.
- Baselines should only prevent legacy issues from blocking progress on new work.
- New issues must never enter the baseline automatically. Every baseline addition requires explicit review.
- Reduce baselines over time. The goal is to remove them entirely.
- This applies equally to lint, static analysis, security findings, and performance regressions.

## Validation Pipeline

Run validation in this order to fail as fast as possible:

1. **Formatting** — instant, no compilation required
2. **Linting / static analysis** — fast, catches structural issues
3. **Compilation** — prerequisite for test execution and artifact-based gates; confirms the code is syntactically and semantically valid
4. **Unit tests** — fast, high signal
5. **Integration tests** — slower, broader scope
6. **Security / dependency scanning** — can be parallelized with tests
7. **API compatibility** — requires a built artifact
8. **Performance regression** — requires a built artifact and baseline

## Reporting

- Report quality gate results directly in pull requests whenever possible.
- Summarize failures before detailed logs — lead with what failed and what action is required.
- Report only actionable information. Noise in gate output trains reviewers to ignore it.
- Avoid duplicate reporting across multiple tools covering the same concern.
- Historical trends belong in dashboards, not pull request comments.

## Formatting

- Enforce formatting automatically in CI. Never rely on developers to remember.
- Use a formatter that is deterministic and produces the same output regardless of environment.
- Format checks must run before any build or test — they are the cheapest possible gate.
- Fail the pipeline if formatting is not applied. Provide the command to fix it in the error output.

## Linting

- Lint rules must be agreed upon and version-controlled. Never rely on IDE defaults.
- Lint configuration lives in the repository, not in developer environments.
- Pin the linter version. Different versions of the same linter can produce different results.
- Treat lint warnings as errors in CI. Warnings that are never enforced accumulate and lose meaning.

## Static Analysis

- Run static analysis on every PR. Do not defer it to scheduled runs only.
- Configure static analysis to fail on new issues, not just existing ones. Use a baseline file for legacy debt.
- Static analysis findings must be actionable — configure rules that the team will actually respond to.
- Suppress a finding only with a documented reason. Blanket suppressions defeat the purpose.

## Dependency Scanning

- Scan all resolved production dependencies for known vulnerabilities on every build.
- Fail the pipeline on high-severity vulnerabilities. Warn on medium. Track low severity separately.
- Keep the vulnerability database up to date — a scan against a stale database provides false confidence.
- Generate a Software Bill of Materials (SBOM) for release builds.

## Secret Scanning

- Scan every commit for accidentally committed secrets before the pipeline runs any other work.
- Secret scanning must run on the diff, not just the current state — a secret that was added and removed is still a leak.
- If a secret is detected, fail immediately, alert the team, and initiate secret rotation or revocation as appropriate.
- Use a baseline to suppress known false positives. Review and prune the baseline regularly.

## License Compliance

- Scan dependency licenses on every build. Fail on licenses incompatible with the project's license.
- Maintain an approved license list. New licenses require explicit review before approval.
- Generate a license report for release builds.

## Security Scanning

- Run SAST on every PR for security-sensitive code paths.
- Run container image scanning when container images are built.
- Run infrastructure-as-code scanning when IaC files change.
- Integrate findings into the PR review process — findings must be addressed, not ignored.

## Binary Size Checks

- Define size budgets per artifact type rather than using a single global threshold. Different artifacts naturally have different acceptable sizes.
- Fail the build if an artifact exceeds its budget.
- Compare size against the expected baseline for the artifact type, not just the previous build — previous build comparisons can be noisy.
- Report size delta on every PR so reviewers are aware of size impact.
- Track size over time to identify gradual growth before it becomes a problem.

## Performance Regression Checks

- Establish a performance baseline from the main branch.
- Run performance regression checks on every relevant PR. Full benchmark suites may run on protected branches, scheduled builds, or release pipelines.
- Compare performance only for workloads representative of production usage. Optimizing synthetic benchmarks that don't reflect real usage provides false confidence.
- Fail or warn when performance degrades beyond a defined threshold.
- Store benchmark results as artifacts for trend analysis.
- Never compare against a baseline from a different machine class or configuration.

## API Compatibility

- Run binary compatibility validation on every PR for published libraries.
- API compatibility checks should validate only intentionally published APIs. Internal APIs must not become part of the compatibility contract.
- API compatibility checks should verify both backward compatibility and intentional removals documented by versioning policy. The gate enforces the versioning contract, not just the absence of breakage.
- Fail the build if a PR introduces a breaking API change without the appropriate version bump.
- Generate and commit API dump files as part of the build process.
- Treat API compatibility as a hard gate for release builds — never publish a breaking change without a major version bump.
