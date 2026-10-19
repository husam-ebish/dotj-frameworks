# DJ-002 .j SDK: Java architecture and contracts

Provide coherent Java project creation, restore, build, run, test, publish and workload orchestration with .j tools.

Product type: Developer tool. Proposed Java package root: `org.dotj.sdk`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-sdk-01 | SdkCommand, ProjectDescriptor, ToolchainLock, CommandResult | Command and project contract |
| dotj-sdk-02 | ToolchainResolver.resolve, WorkloadManifest, PlatformRequirement | Toolchain and workload resolution |
| dotj-sdk-03 | BuildInvocation, RestoreGraph, TestRunRequest | Restore build and test orchestration |
| dotj-sdk-04 | PublishProfile, RuntimeLayout, WorkloadPack | Publish and deployment bundles |
| dotj-sdk-05 | ProjectImporter, MigrationDiagnostic, SdkCompatibilityManifest | Compatibility import and upgrades |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Translate project and workload concepts rather than executing arbitrary .NET SDK targets; define exit codes, diagnostics and version resolution explicitly.

## Feature contracts and invariants

### WP-01: Command and project contract

Contract vocabulary: `SdkCommand`, `ProjectDescriptor`, `ToolchainLock`, `CommandResult`.

Define new/restore/build/run/test/publish command arguments and exit codes. Specify project discovery, working-directory rules and config precedence. Define structured diagnostics and noninteractive behavior.

Required observable invariant: Unknown options fail deterministically; project ambiguity produces a useful diagnostic; commands preserve spaces/Unicode in paths; machine output never mixes progress text with JSON results.

### WP-02: Toolchain and workload resolution

Contract vocabulary: `ToolchainResolver.resolve`, `WorkloadManifest`, `PlatformRequirement`.

Resolve exact installed compiler/runtime versions from locked manifests. Validate workload platform/architecture prerequisites and package checksums. Define side-by-side installation and rollback ownership.

Required observable invariant: Missing exact toolchain cannot silently roll forward; failed workload install leaves the previous workload usable; architecture mismatches fail before execution.

### WP-03: Restore build and test orchestration

Contract vocabulary: `BuildInvocation`, `RestoreGraph`, `TestRunRequest`.

Integrate packages/build/templates through versioned process or library contracts. Propagate cancellation and diagnostics while preserving child-process ownership. Define offline mode and independent bootstrap fallback.

Required observable invariant: Offline build succeeds with complete cache and fails with named missing artifacts otherwise; cancellation terminates owned children; SDK can be rebuilt without an installed dotj-sdk.

### WP-04: Publish and deployment bundles

Contract vocabulary: `PublishProfile`, `RuntimeLayout`, `WorkloadPack`.

Define library/application/runtime-image publication layouts. Integrate jlink/jpackage or platform packagers only through declared tool adapters. Produce checksummed provenance and dependency manifests.

Required observable invariant: Clean publish outputs contain only declared inputs; startup probes validate runtime layout; native/mobile publication fails clearly when its backend is not proven.

### WP-05: Compatibility import and upgrades

Contract vocabulary: `ProjectImporter`, `MigrationDiagnostic`, `SdkCompatibilityManifest`.

Classify .NET project properties as translated, unsupported or externally executed. Define migration reports and Java-native project schema upgrades. Maintain workload/version compatibility between SDK and lower tools.

Required observable invariant: Importer never executes arbitrary .NET targets by default; unsupported properties remain visible; schema upgrades are repeatable and retain the original project for review.

## Bootstrap and dependency boundaries

ProcessBuilder, ToolProvider, file APIs and JAR tooling; installed javac/jar bootstrap the toolchain.

Proposed .j dependencies: build,templates,packages. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET SDK usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `SdkCommand` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unknown options fail deterministically; project ambiguity produces a useful diagnostic; commands preserve spaces/Unicode in paths; machine output never mixes progress text with JSON results. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
