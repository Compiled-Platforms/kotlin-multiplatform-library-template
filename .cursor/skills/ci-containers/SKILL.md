---
name: ci-containers
description: Build and manage containers in CI — Docker best practices, multi-stage builds, BuildKit, layer caching, image scanning, registry publishing, and container testing. Use when writing Dockerfiles, configuring container builds in CI, or publishing images.
---

# CI Containers

Always apply `.cursor/rules/development-process/ci.mdc` before making any CI decisions.

## Principles

- Container images are artifacts. Apply the same standards as any other build artifact: immutable, versioned, traceable.
- Smaller images are faster to pull, push, scan, and less likely to contain vulnerabilities. Minimize aggressively.
- Every layer is permanent in the image history. Never put secrets in a layer, even temporarily.
- Reproducible builds require pinned base images. A floating `latest` tag produces a different image every time.

## Dockerfile Best Practices

- Pin base images to a specific digest or immutable tag. Never use `latest`.
- Use official or verified base images from trusted registries.
- Minimize the number of layers. Group related `RUN` commands with `&&`.
- Order layers from least-frequently-changed to most-frequently-changed to maximize cache reuse.
- Run as a non-root user. Create a dedicated user for the application.
- Remove build tools, package manager caches, and temporary files in the same layer they are created.
- Use `.dockerignore` to exclude unnecessary files from the build context.

## Build Context

- Keep build contexts minimal. Large build contexts slow down builds and increase the risk of accidentally including sensitive files.
- Never send secrets, local config, credentials, caches, or generated artifacts in the Docker build context.
- `.dockerignore` is both a security and a performance control — treat it accordingly.
- Build context contents should be deterministic and reviewable. Anyone should be able to verify exactly what was included.

## Multi-Stage Builds

- Use multi-stage builds to separate build dependencies from runtime dependencies.
- The final stage should contain only what is needed to run the application — no compilers, no SDKs, no test tools.
- Name stages explicitly for readability: `FROM golang:1.22 AS builder`, `FROM gcr.io/distroless/base AS runtime`.
- Copy only specific outputs from earlier stages, not entire directories.
- Use a minimal base image for the final stage (distroless, Alpine, scratch) unless compatibility requires otherwise.

## BuildKit

- Enable BuildKit for all builds. It provides parallel layer building, improved caching, and secret mount support.
- Use `--mount=type=secret` for secrets needed during the build. Never use `ARG` or `ENV` for secrets.
- Use `--mount=type=cache` for package manager caches to speed up repeated builds without polluting the final image.
- Use `--platform` to build multi-architecture images from a single Dockerfile.

## Base Image Lifecycle

- Choose base images based on trust, support lifecycle, vulnerability profile, compatibility, and update cadence.
- Rebuild images when base images change, even if application code did not change. Vulnerability fixes in base images are not inherited automatically.
- Track base image end-of-life dates. Plan upgrades before support ends.
- Prefer minimal images, but not when they make debugging, compatibility, or security updates impractical.

## Layer Caching in CI

- Use registry-based cache backends for cache sharing across CI runners.
- Seed the cache from the main branch image so PR builds start warm.
- Use inline cache metadata only for single-runner setups — prefer registry cache for multi-runner environments.
- Invalidate the cache explicitly when base image versions change.

## Image Identity & Traceability

- Every image should include labels for: source repository, commit SHA, build timestamp, version, license, and CI run.
- Every pushed image must be traceable to: the Dockerfile, build context, base image digest, workflow run, and source revision.
- Prefer digest references when promoting or deploying images. Tags are human-facing aliases; digests are the immutable identity.

## Image Promotion

- Build once, promote by digest. Do not rebuild separately for staging and production.
- Promotion moves the same verified image through environments — it does not create a new one.
- Validation must happen before promotion to production, not after.
- Never promote an unscanned or unverified image to a production registry.

## Image Scanning

- Scan every built image before release or promotion. CI may push to a restricted staging registry before scanning when the scanner requires registry access.
- Fail the pipeline on high-severity CVEs. Warn on medium. Track low severity over time.
- Scan base images on a schedule even when the Dockerfile hasn't changed — new vulnerabilities are discovered continuously.
- Address vulnerabilities by updating the base image or dependency, not by suppressing the finding.
- Vulnerability suppressions must be documented, justified, owned, and time-bound. Review them periodically.
- Suppressions must not hide newly introduced vulnerabilities.

## SBOM & Provenance

- Generate an SBOM for every release image.
- Generate provenance or build attestations for release images.
- Store SBOMs and attestations alongside the image or in release evidence.
- Consumers should be able to verify what source, dependencies, and build process produced the image.

## Registry Publishing

- Tag images with the commit SHA for exact traceability.
- Tag images with semantic version tags for release images.
- Never overwrite an existing tag for a published release image — it breaks reproducibility for consumers.
- Use a staging registry for CI builds. Promote images to production registries only after validation.
- Clean up old CI images regularly. Accumulated images have storage cost and scanning overhead.

## Registry Security

- Registry credentials should be scoped to the minimum required repository and action.
- Publishing should require trusted branches, tags, or manual approval.
- Registries should enforce immutability for release tags where possible.
- Remove unused registry credentials and stale permissions regularly.

## Container Testing

- Test the container image as a black box — interact with it the same way a consumer would.
- Start the container in CI and run smoke tests against its exposed interface before publishing.
- Test that the container starts cleanly, responds to health checks, and handles graceful shutdown.
- Test multi-architecture images on the correct platform — an ARM image that only runs on x86 is useless.
- Use container structure tests to validate filesystem layout, file permissions, and entrypoint behavior.

## Runtime Contract

- Define the expected entrypoint, exposed ports, environment variables, volumes, health checks, and shutdown behavior.
- The image should fail fast when required configuration is missing.
- Runtime defaults should be safe for CI and local testing.
- Do not bake environment-specific configuration into the image. Configuration belongs in the environment, not the artifact.

## Resource Efficiency

- Avoid unnecessarily large build contexts, layers, and intermediate artifacts.
- Avoid rebuilding unchanged images. Check whether a valid image already exists before triggering a build.
- Avoid pushing images that will never be consumed.
- Clean up dangling layers, old cache entries, and temporary images on self-hosted runners.
