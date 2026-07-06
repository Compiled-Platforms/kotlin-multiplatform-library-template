---
name: ci-releases
description: Design and operate CI release pipelines — tag-based releases, semantic versioning, changelog generation, automated publishing, rollback support, release validation, artifact versioning, SBOM, and provenance. Use when setting up or modifying release workflows.
---

# CI Releases

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Principles

- Releases are produced by CI, not by developer machines. A release that can only be produced locally is a liability.
- Every release must be reproducible from source. Given the same source revision and build configuration, the pipeline must produce identical artifacts.
- Releases are immutable. A published artifact must never be modified or overwritten.
- Every release artifact must be traceable to the exact commit, pipeline run, and build configuration that produced it.

## Release Strategy

- Define whether releases are manual, scheduled, tag-based, continuous, or release-candidate based before building the pipeline.
- The release strategy should match the risk level of the artifact. Higher risk warrants more explicit release gates.
- Production releases should require an explicit, auditable release decision.
- Pre-releases must be clearly separated from stable releases in versioning, naming, and distribution channels.

## Release Pipeline Design

- The release pipeline is separate from the build/test pipeline. Merging code and releasing code are distinct operations.
- Trigger releases from an explicit signal: a version tag, a manual dispatch, or a GitHub Release creation. Never auto-release from every merge.
- The release pipeline must run the full validation suite before publishing.
- Publishing is the last step, after all validation passes. Never publish a partially validated artifact.

## Tag-Based Releases

- Use version tags (e.g., `v1.2.3`) as the authoritative trigger for releases.
- Protect version tags — only CI or authorized maintainers should be able to create them.
- The tag must point to a commit that has already passed CI on the main branch.
- Never release from a branch. Releases are cut from main (or a dedicated release branch) only.

## Release Candidates

- Build release candidates once and promote them after validation. Do not rebuild between candidate validation and final release.
- Release candidates should use pre-release versions (e.g., `1.2.3-rc.1`).
- Final release artifacts must be traceable to the validated release candidate.
- Validate release candidates in a production-equivalent environment before promotion.

## Release Approval

- Define who can approve a release and codify that in the pipeline.
- Approval must happen after validation and before publishing.
- High-risk releases should require stronger approval than low-risk releases.
- All approval decisions must be auditable — who approved, when, and for what.

## Semantic Versioning

- Follow semantic versioning strictly: MAJOR.MINOR.PATCH.
  - MAJOR: breaking API change
  - MINOR: new backward-compatible functionality
  - PATCH: backward-compatible bug fix
- Automate version determination from commit history where possible (e.g., conventional commits).
- Never manually edit version numbers in source files as the primary version source — derive them from tags.
- Validate that the version being released is greater than the last published version.

## Artifact Promotion

- Build once, promote everywhere. Do not rebuild separately for each environment or registry.
- Promotion moves the same verified artifact through staging, production, and public distribution.
- Promote by immutable artifact identity (digest, content hash), not by mutable tags or names.
- Never promote an artifact that has not been validated.

## Changelog Generation

- Generate changelogs automatically from commit history using conventional commit messages.
- Include the changelog in the GitHub Release description.
- Changelogs must be human-readable. Group by type (features, fixes, breaking changes).
- Do not include internal or chore commits in the user-facing changelog.

## Automated Publishing

- Publishing credentials must never touch developer machines. All publishing goes through CI.
- Use OIDC or scoped tokens for publishing. Avoid long-lived static credentials.
- Publish all artifacts for a release through one coordinated release process.
- Verify the published artifact is accessible and correct after publishing — do not assume success.

## Partial Release Handling

- Define what happens if publishing succeeds for some targets and fails for others, before it happens.
- Detect partial releases immediately and alert the team.
- Prefer idempotent publishing steps that are safe to retry without producing duplicate or corrupted state.
- Never silently continue after a failed publish target.

## Signing

- Sign release artifacts where the target ecosystem supports it.
- Signing keys must be protected and available only to trusted release workflows.
- Verify signatures before promotion or distribution.
- Document signature verification instructions for consumers where applicable.

## Release Validation

- After publishing, run a smoke test that consumes the published artifact from its public location.
- Validate artifact integrity using checksums or signatures.
- Confirm that the version is discoverable via the registry's API.
- Alert on failure immediately — a partially released version is worse than no release.

## Release Evidence

- Every release must preserve: source revision, workflow run, validation results, quality gate results, checksums, signatures, SBOM, provenance, changelog, and published artifact locations.
- Release evidence must be retained longer than normal CI logs.
- A release must be fully auditable without rerunning the pipeline.

## Rollback Support

- Define a rollback procedure before you need it. Document it.
- For package registries that support yanking or deprecating, do so immediately for a bad release — never leave a broken version as the latest.
- For deployed services, maintain the ability to redeploy the previous version within minutes.
- Test the rollback procedure periodically. An untested rollback is not a rollback.

## Hotfix Releases

- Define a hotfix release path before it is needed.
- Hotfixes must still run required validation — urgency does not justify bypassing release controls.
- Hotfix releases must be traceable to the fix commit and the affected production version.
- After the hotfix, merge the fix forward to avoid divergence.

## Artifact Versioning

- Artifact names must include the version. Never publish an unversioned artifact.
- Include build metadata in artifact names for pre-release or CI builds (e.g., `1.2.3-SNAPSHOT`, `1.2.3+build.42`).
- Separate release artifacts from CI artifacts. Release artifacts are immutable and retained indefinitely.

## Multi-Platform Consistency

- All platform artifacts for the same version must come from the same source revision.
- Validate that all expected platform artifacts were produced before publishing any of them.
- Do not publish a version until all required platform artifacts are complete.
- If platforms release independently, versioning must make that explicit.

## Deprecation / Yanking / EOL

- Define when a released version may be deprecated, yanked, hidden, or marked end-of-life.
- Deprecation must communicate the replacement version and the reason.
- Never delete artifacts when deprecation or yanking is sufficient. Deleting breaks consumers who pinned the version.
- Keep release metadata available even for deprecated or EOL versions.

## Release Branches

- Use release branches only when supporting maintained historical versions.
- Release branches must have clear ownership and defined support windows.
- Fixes must be merged forward to avoid divergence between maintained versions.
- Avoid long-lived release branches unless the maintenance policy explicitly requires them.

## SBOM & Provenance

- Generate a Software Bill of Materials (SBOM) for every release artifact.
- Publish the SBOM alongside the artifact so consumers can audit dependencies.
- Generate SLSA provenance attestations where supported to prove the artifact was built by CI from the expected source.
- Store provenance in a location that survives the pipeline run (attach to the GitHub Release, publish to registry).
