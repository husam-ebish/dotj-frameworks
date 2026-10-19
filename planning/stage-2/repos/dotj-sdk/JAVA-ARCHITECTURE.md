# DJ-002 .j SDK: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide coherent Java project creation, restore, build, run, test, publish and workload orchestration with .j tools.

Product type: Developer tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-sdk-01 | SdkCommand, ProjectDescriptor, ToolchainLock, CommandResult | Command and project contract |
| dotj-sdk-02 | ToolchainResolver.resolve, WorkloadManifest, PlatformRequirement | Toolchain and workload resolution |
| dotj-sdk-03 | BuildInvocation, RestoreGraph, TestRunRequest | Restore build and test orchestration |
| dotj-sdk-04 | PublishProfile, RuntimeLayout, WorkloadPack | Publish and deployment bundles |
| dotj-sdk-05 | ProjectImporter, MigrationDiagnostic, SdkCompatibilityManifest | Compatibility import and upgrades |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Translate project and workload concepts rather than executing arbitrary .NET SDK targets; define exit codes, diagnostics and version resolution explicitly.

## Feature contracts and invariants

### WP-01: Command and project contract

Internal analysis vocabulary (not permission to rename the public API): `SdkCommand`, `ProjectDescriptor`, `ToolchainLock`, `CommandResult`.

Define new/restore/build/run/test/publish command arguments and exit codes. Specify project discovery, working-directory rules and config precedence. Define structured diagnostics and noninteractive behavior.

Required observable invariant: Unknown options fail deterministically; project ambiguity produces a useful diagnostic; commands preserve spaces/Unicode in paths; machine output never mixes progress text with JSON results.

### WP-02: Toolchain and workload resolution

Internal analysis vocabulary (not permission to rename the public API): `ToolchainResolver.resolve`, `WorkloadManifest`, `PlatformRequirement`.

Resolve exact installed compiler/runtime versions from locked manifests. Validate workload platform/architecture prerequisites and package checksums. Define side-by-side installation and rollback ownership.

Required observable invariant: SDK selection follows the qualified global.json policy; disable requires an exact SDK and no policy permits an unrequested silent substitution; failed workload install leaves the previous workload usable; architecture mismatches fail before execution.

### WP-03: Restore build and test orchestration

Internal analysis vocabulary (not permission to rename the public API): `BuildInvocation`, `RestoreGraph`, `TestRunRequest`.

Integrate packages/build/templates through versioned process or library contracts. Propagate cancellation and diagnostics while preserving child-process ownership. Define offline mode and independent bootstrap fallback.

Required observable invariant: Offline build succeeds with complete cache and fails with named missing artifacts otherwise; cancellation terminates owned children; SDK can be rebuilt without an installed dotj-sdk.

### WP-04: Publish and deployment bundles

Internal analysis vocabulary (not permission to rename the public API): `PublishProfile`, `RuntimeLayout`, `WorkloadPack`.

Define library/application/runtime-image publication layouts. Integrate jlink/jpackage or platform packagers only through declared tool adapters. Produce checksummed provenance and dependency manifests.

Required observable invariant: Clean publish outputs contain only declared inputs; startup probes validate runtime layout; native/mobile publication fails clearly when its backend is not proven.

### WP-05: Compatibility import and upgrades

Internal analysis vocabulary (not permission to rename the public API): `ProjectImporter`, `MigrationDiagnostic`, `SdkCompatibilityManifest`.

Classify .NET project properties as translated, unsupported or externally executed. Define migration reports and Java-native project schema upgrades. Maintain workload/version compatibility between SDK and lower tools.

Required observable invariant: Importer never executes arbitrary .NET targets by default; unsupported properties remain visible; schema upgrades are repeatable and retain the original project for review.

## Bootstrap and dependency boundaries

ProcessBuilder, ToolProvider, file APIs and JAR tooling; installed javac/jar bootstrap the toolchain.

Proposed .j dependencies: build,templates,packages. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET SDK usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `SdkCommand` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unknown options fail deterministically; project ambiguity produces a useful diagnostic; commands preserve spaces/Unicode in paths; machine output never mixes progress text with JSON results. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I01`: Reference baseline and exact compatibility contracts; five named tasks and five designed cases in the integration plan.
- `SDK-I06`: End-to-end CLI orchestration and real test runners; five named tasks and five designed cases in the integration plan.
- `SDK-I07`: SDK bundles, global.json and installation transactions; five named tasks and five designed cases in the integration plan.
- `SDK-I08`: Publish profiles and deployable runtime outputs; five named tasks and five designed cases in the integration plan.
- `SDK-I09`: Tool, workload and IDE integration; five named tasks and five designed cases in the integration plan.
- `SDK-I11`: Portable CI, signing and release distribution; five named tasks and five designed cases in the integration plan.
- `SDK-I12`: All-product SDK qualification and agent handoff; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.
