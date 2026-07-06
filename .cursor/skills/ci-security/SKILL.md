---
name: ci-security
description: Secure CI pipelines — secret management, token permissions, OIDC authentication, supply chain security, signed artifacts, trusted publishing, and dependency verification. Use when configuring permissions, handling secrets, adding third-party actions, or setting up artifact signing.
---

# CI Security

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Principles

- CI pipelines are privileged execution environments. Treat them accordingly.
- Least privilege is not optional. Every excess permission is an attack surface.
- Secrets must never appear in logs, artifacts, or environment dumps under any circumstances.
- Trust is earned, not assumed. Verify third-party code before executing it.
- Security checks should fail closed when confidence cannot be established.
- CI security exceptions must be documented, time-bound, and reviewed regularly.

## Trust Boundaries

- Define trust boundaries explicitly between: repository code, CI infrastructure, external services, runners, and deployment environments.
- Treat fork PRs and external contributions as untrusted. Never run untrusted code with trusted credentials or elevated permissions.
- Require explicit authorization when crossing trust boundaries — do not let trust flow implicitly through job dependencies.
- Security-sensitive workflows must avoid automatic execution from untrusted events (e.g., `pull_request_target` from forks without review gates).
- Publishing jobs require the highest trust level. Release artifacts must be generated only from trusted branches or tags.

## Token Permissions

- Set the minimum required permissions at the workflow level. Default to read-only.
- Override permissions at the job level only for jobs that require elevated access.
- Never use a personal access token when a scoped token or OIDC credential will suffice.
- Rotate tokens regularly. Treat long-lived tokens as a liability.
- Audit token usage after any pipeline change that touches permissions.

## OIDC Authentication

- Prefer OIDC over long-lived static credentials wherever the target service supports it.
- OIDC tokens are short-lived and scoped to the specific workflow run — they cannot be extracted and reused.
- Configure the OIDC trust relationship with tight conditions: specific repository, branch, and workflow.
- Never use overly broad OIDC conditions (e.g., any repository, any branch) — this defeats the purpose.

## Credential Lifecycle

- Prefer short-lived credentials over long-lived ones wherever possible.
- Every credential should have a documented owner, purpose, and rotation policy.
- Remove unused credentials promptly. Unused credentials are dormant attack surface.
- Periodically review all credentials in use — verify they are still needed, still scoped correctly, and still owned.

## Secret Management

- Never log secrets. Audit all steps that might expose environment variables.
- Never pass secrets through command-line arguments — they appear in process listings.
- Pass secrets through environment variables scoped to the specific step that needs them.
- Never store secrets in artifacts, caches, or any persistent storage.
- Rotate secrets immediately if they are suspected to have been exposed.
- Audit which workflows have access to which secrets regularly.

## Build Isolation

- Every CI job must execute in an isolated environment. Never rely on state from a previous run.
- Separate trusted and untrusted workloads — do not run them in the same environment.
- Clean up temporary files, credentials, and sensitive data at the end of every job.
- For self-hosted runners, use ephemeral environments that are destroyed after each job.

## Supply Chain Security

- Pin all third-party actions to a specific commit SHA, not a version tag. Tags are mutable; SHAs are not.
- Review the source of every third-party action before use. Understand what it does and what permissions it requires.
- Prefer actions from verified publishers or official organization accounts.
- Minimize the number of third-party actions in use. Every external dependency is a trust decision.
- Dependency updates (including action version bumps) must go through code review. Automated bumps must not auto-merge.
- Monitor third-party actions for known vulnerabilities or compromises.

## Third-Party Trust

- Evaluate every third-party action, dependency, or service before introducing it.
- Grant third-party tools only the permissions they actually need.
- Prefer pinned, actively maintained, and reviewed dependencies over convenient but unvetted ones.
- Remove unused third-party integrations. Unused integrations retain permissions and represent unnecessary risk.

## Signed Artifacts

- Sign release artifacts to allow consumers to verify authenticity and integrity.
- Use a signing key with a clear, documented provenance. Know who owns it and how it is protected.
- Verify signatures in downstream pipelines before consuming artifacts.
- Publish public keys or certificates in a well-known, stable location.

## Trusted Publishing

- Use trusted publishing mechanisms (e.g., PyPI Trusted Publishers, Maven Central OIDC) to publish packages without long-lived credentials.
- Restrict trusted publishing to specific workflows and branches — never allow publishing from arbitrary branches.
- Validate the published artifact after publishing to confirm it matches the source.

## Dependency Verification

- Verify checksums or signatures of downloaded dependencies before use.
- Use lock files for all package managers. Never install from floating version ranges in CI.
- Enable dependency verification in build tools where available.
- Fail the build if verification fails — never continue with unverified dependencies.

## Artifact Integrity

- Include a content hash in artifact names or metadata to enable integrity verification.
- Generate and publish a Software Bill of Materials (SBOM) for release artifacts.
- Generate build provenance attestations where supported (e.g., SLSA provenance).
- Store provenance alongside artifacts so consumers can verify build conditions.

## Auditability

- Security-sensitive actions must be attributable to a specific workflow, job, and identity.
- Changes to security configuration (permissions, secrets, branch protection, signing keys) must be reviewed and traceable.
- Preserve enough audit data — logs, provenance, artifact metadata — for incident investigation.
- Avoid security controls that cannot be verified. An unverifiable control provides false confidence.

## Runner Security

- Avoid self-hosted runners for public repositories — untrusted code could compromise the runner environment.
- For self-hosted runners, run each job in an ephemeral, isolated environment. Never reuse runner state across jobs.
- Restrict which repositories and workflows can use self-hosted runners.
- Keep runner software and OS images patched and up to date.

## Incident Response

- Define incident response procedures before they are needed. Document them.
- When a secret is compromised: fail immediately, alert the team, and initiate rotation or revocation.
- When a release artifact is compromised: yank or deprecate it from the registry, notify consumers, and publish a clean replacement.
- When a runner is compromised: isolate it immediately, rotate any credentials it had access to, and investigate what it touched.
- When a dependency is compromised: remove it, assess blast radius, rebuild and republish affected artifacts.
- Preserve logs, provenance records, and artifact metadata throughout the investigation.
- After any security incident, conduct a post-mortem and update CI security controls accordingly.
