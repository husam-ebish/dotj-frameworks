# DJ-062 .j Packages: Java architecture and contracts

Provide dependency resolution, package acquisition and Java artifact management with explicit NuGet interoperability scope.

Product type: Developer/package tool. Proposed Java package root: `org.dotj.packages`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-packages-01 | PackageId, PackageVersion, ArtifactManifest | Artifact identity metadata and archives |
| dotj-packages-02 | VersionRange, DependencyGraph, ResolutionResult | Version resolution and dependency graph |
| dotj-packages-03 | PackageSource, RestorePlan, ContentCache | Feeds restore cache and offline mode |
| dotj-packages-04 | PackPlan, SignatureRecord, PublishRequest | Packing signing publishing and provenance |
| dotj-packages-05 | PackageCommand, LockFile, VulnerabilityRecord | CLI SDK integration and maintenance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Native .j artifacts are JARs; consuming NuGet metadata does not make DLLs executable. Package identity and version rules need separate compatibility profiles.

## Feature contracts and invariants

### WP-01: Artifact identity metadata and archives

Contract vocabulary: `PackageId`, `PackageVersion`, `ArtifactManifest`.

Define native Java artifact coordinates and dependency metadata. Separate JAR/module semantics from NuGet compatibility. Validate archive paths signatures hashes and content types.

Required observable invariant: NuGet packages are not treated as executable Java artifacts; traversal fails; immutable content identity is recorded.

### WP-02: Version resolution and dependency graph

Contract vocabulary: `VersionRange`, `DependencyGraph`, `ResolutionResult`.

Define range prerelease conflict and target compatibility rules. Resolve deterministically from locked source snapshots. Report conflicts and missing packages with dependency paths.

Required observable invariant: Same input lock yields same graph; incompatible constraints fail explicitly; optional/platform dependencies remain traceable.

### WP-03: Feeds restore cache and offline mode

Contract vocabulary: `PackageSource`, `RestorePlan`, `ContentCache`.

Implement selected NuGet protocol adapters separately from native feeds. Verify digests before atomic cache publication. Define source priority credential scope and offline behavior.

Required observable invariant: Corrupt downloads never enter cache; offline restore performs no network calls; credentials cannot cross feed origins.

### WP-04: Packing signing publishing and provenance

Contract vocabulary: `PackPlan`, `SignatureRecord`, `PublishRequest`.

Build reproducible Java archives and optional NuGet wrappers. Keep signing keys external and verify signatures under explicit policy. Stage publishing with idempotent identity checks.

Required observable invariant: Repacking locked inputs produces explainable output; conflicting immutable versions fail; publication metadata preserves source/license provenance.

### WP-05: CLI SDK integration and maintenance

Contract vocabulary: `PackageCommand`, `LockFile`, `VulnerabilityRecord`.

Provide standalone CLI before SDK integration. Version lockfiles and migration rules. Map audit/advisory behavior without inventing vulnerability clearance.

Required observable invariant: Standalone restore works without registry or SDK; lock upgrades are reviewable; a successful restore is not a security certification.

## Bootstrap and dependency boundaries

HTTP client, ZIP/JAR, cryptographic verification and XML/JSON.

Proposed .j dependencies: core,json. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NuGet client usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `PackageId` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: NuGet packages are not treated as executable Java artifacts; traversal fails; immutable content identity is recorded. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
