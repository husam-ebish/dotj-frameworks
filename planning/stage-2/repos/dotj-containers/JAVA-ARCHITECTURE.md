# DJ-011 .j Containers: Java architecture and contracts

Produce reproducible .j runtime, SDK and application container image families.

Product type: Container/packaging project. This product delivers image recipes, manifests and verification tooling; it does not require a Java library or JPMS artifact. Rows below identify planning workstream units, not mandatory JAR modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-containers-01 | ImageRole, JdkBinaryLock, BaseImageLock | Image families and binary inputs |
| dotj-containers-02 | LayerPlan, RuntimeModuleSet, ImageManifest | Reproducible image assembly |
| dotj-containers-03 | ContainerLaunchContract, HealthProbe, ShutdownPolicy | Runtime behavior and hardening |
| dotj-containers-04 | PlatformManifest, NativeInventory, SmokeMatrix | Architecture and Windows tracks |
| dotj-containers-05 | Sbom, RebuildRecord, ImageSupportPolicy | Publishing and patch maintenance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve image-role and deployment capabilities, not .NET image contents or tags. Pin image digests and JDK binary checksums.

## Feature contracts and invariants

### WP-01: Image families and binary inputs

Contract vocabulary: `ImageRole`, `JdkBinaryLock`, `BaseImageLock`.

Define runtime SDK and application image responsibilities. Pin base digests JDK vendor version and checksums. Inventory redistribution and architecture constraints.

Required observable invariant: Every image can be traced to immutable inputs; no floating base tag is used in reproducibility claims; unsupported platforms remain explicit.

### WP-02: Reproducible image assembly

Contract vocabulary: `LayerPlan`, `RuntimeModuleSet`, `ImageManifest`.

Generate stable layers and normalized file ownership. Define jlink eligibility and fallback full-runtime images. Separate build secrets from committed layers.

Required observable invariant: Two clean builds have explainable digest differences or identical output; registry credentials never occur in layers; service-provider modules survive linking.

### WP-03: Runtime behavior and hardening

Contract vocabulary: `ContainerLaunchContract`, `HealthProbe`, `ShutdownPolicy`.

Run as a documented non-root identity. Forward signals and bound graceful shutdown. Exercise read-only root temporary storage CA and timezone behavior.

Required observable invariant: SIGTERM reaches application lifecycle; writable paths are declared; TLS and timezone fixtures pass on each advertised image.

### WP-04: Architecture and Windows tracks

Contract vocabulary: `PlatformManifest`, `NativeInventory`, `SmokeMatrix`.

Build and test each architecture on a compatible executor. Record native library and libc dependencies. Keep Windows container support as a separately gated family.

Required observable invariant: Manifest entries refer only to tested images; native loading failures are attributable; Linux evidence is never used as proof of Windows support.

### WP-05: Publishing and patch maintenance

Contract vocabulary: `Sbom`, `RebuildRecord`, `ImageSupportPolicy`.

Generate SBOM and provenance per image digest. Define vulnerability triage and rebuild triggers. Stage signed manifests and promotion rollback procedures.

Required observable invariant: Published digest retains its verification record; rebuilds update dependency locks; rollback selects a known immutable manifest.

## Bootstrap and dependency boundaries

Installed JDK/jlink, OCI-compatible build tools and Linux base images as build/platform dependencies.

Proposed .j dependencies: sdk. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET container images usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ImageRole` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Every image can be traced to immutable inputs; no floating base tag is used in reproducibility claims; unsupported platforms remain explicit. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
