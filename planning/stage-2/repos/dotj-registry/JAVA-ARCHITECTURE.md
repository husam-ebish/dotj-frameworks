# DJ-063 .j Registry: Java architecture and contracts

Host searchable package metadata and artifacts with publishing, moderation and account workflows.

Product type: Web/package infrastructure. Proposed Java package root: `org.dotj.registry`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-registry-01 | FeedResource, PackageRecord, SearchIndex | Feed protocol and package index |
| dotj-registry-02 | UploadSession, BlobKey, PublicationState | Upload validation and storage transactions |
| dotj-registry-03 | ApiCredential, PackageOwnership, AuditEvent | Authentication authorization and moderation |
| dotj-registry-04 | SearchQuery, FeedUi, IndexJob | Search UI jobs and ecosystem integration |
| dotj-registry-05 | StorageSnapshot, RecoveryPlan, ProtocolFixture | Operations backup compatibility and licensing |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

NuGet Gallery is a service with protocol contracts, not a JVM package repository by default. Define Java feeds and optional NuGet routes independently.

## Feature contracts and invariants

### WP-01: Feed protocol and package index

Contract vocabulary: `FeedResource`, `PackageRecord`, `SearchIndex`.

Implement selected NuGet v3 endpoints and native Java feed contract. Separate metadata indexes from immutable content. Define version/listing/deprecation visibility rules.

Required observable invariant: Published content hashes match responses; unlisted versions obey protocol semantics; Java artifacts and NuGet packages remain distinguishable.

### WP-02: Upload validation and storage transactions

Contract vocabulary: `UploadSession`, `BlobKey`, `PublicationState`.

Validate archive metadata size digest and ownership. Commit content/index publication atomically or reconcile partial states. Keep storage providers behind explicit consistency contracts.

Required observable invariant: Interrupted uploads never appear as valid packages; duplicate identical uploads are idempotent; conflicting bytes at one identity are rejected.

### WP-03: Authentication authorization and moderation

Contract vocabulary: `ApiCredential`, `PackageOwnership`, `AuditEvent`.

Define upload/delete/list/admin permissions. Scope credentials to actions and package ownership. Record revocation retention and administrative changes.

Required observable invariant: Revoked keys cannot publish; owners cannot overwrite unrelated packages; audit records exclude raw secrets.

### WP-04: Search UI jobs and ecosystem integration

Contract vocabulary: `SearchQuery`, `FeedUi`, `IndexJob`.

Build authenticated administration and escaped public metadata views. Index asynchronously with freshness/version markers. Integrate package client and background processing through optional adapters.

Required observable invariant: Search lag is visible; hostile README/metadata cannot execute script; registry bootstraps without relying on its own published packages.

### WP-05: Operations backup compatibility and licensing

Contract vocabulary: `StorageSnapshot`, `RecoveryPlan`, `ProtocolFixture`.

Map gallery/catalog/search dependencies and external repositories. Test restore backup index rebuild and feed client compatibility. Specify quotas retention and operational metrics.

Required observable invariant: Restored registry reconciles metadata with blobs; claimed endpoints pass client fixtures; cloud-storage guarantees are not assumed universally.

## Bootstrap and dependency boundaries

Owned web/data stack and filesystem/object-storage SPI.

Proposed .j dependencies: web,packages,postgresql,auth. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NuGet Gallery usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `FeedResource` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Published content hashes match responses; unlisted versions obey protocol semantics; Java artifacts and NuGet packages remain distinguishable. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
