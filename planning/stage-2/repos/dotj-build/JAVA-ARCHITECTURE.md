# DJ-005 .j Build: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Create a Java build graph engine with evaluation, task execution and incremental-build capabilities.

Product type: Developer tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-build-01 | ProjectModel, PropertyBag, ItemSpec, EvaluationResult | Project evaluation |
| dotj-build-02 | BuildGraph, TargetNode, TaskInvocation, BuildResult | Target graph and scheduling |
| dotj-build-03 | TaskProvider, TaskContext, ProcessTask, ArtifactOutput | Task host and process isolation |
| dotj-build-04 | InputFingerprint, OutputManifest, CacheKey, InvalidationReason | Incremental state and cache |
| dotj-build-05 | BuildEvent, Diagnostic, BuildTrace, BootstrapManifest | Logs and reproducible integration |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

MSBuild property/item evaluation and target ordering need explicit emulation; .NET task assemblies require Java replacements or an optional external process bridge.

## Feature contracts and invariants

### WP-01: Project evaluation

Internal analysis vocabulary (not permission to rename the public API): `ProjectModel`, `PropertyBag`, `ItemSpec`, `EvaluationResult`.

Specify property/item precedence, imports, conditions and glob evaluation. Separate evaluation from target execution. Define native Java format and optional MSBuild-compatible importer.

Required observable invariant: Conditional imports and property expansion are deterministic; import cycles report chains; glob behavior is tested for Windows/Linux case differences; evaluator never executes tasks.

### WP-02: Target graph and scheduling

Internal analysis vocabulary (not permission to rename the public API): `BuildGraph`, `TargetNode`, `TaskInvocation`, `BuildResult`.

Construct dependency graph with cycle detection and target ordering. Schedule independent targets with bounded parallelism. Define failure propagation, skipped targets and cancellation.

Required observable invariant: Cycles show a reproducible path; no target runs before prerequisites; task failure prevents dependent work without cancelling unrelated work under continue mode.

### WP-03: Task host and process isolation

Internal analysis vocabulary (not permission to rename the public API): `TaskProvider`, `TaskContext`, `ProcessTask`, `ArtifactOutput`.

Define versioned Java task SPI and isolated external process execution. Specify environment/input/output ownership and secret redaction. Map .NET task assemblies to replacement requirements.

Required observable invariant: Untrusted project tasks require explicit execution policy; command arguments preserve quoting; killed tasks cannot report success; .NET assemblies are never loaded as Java tasks.

### WP-04: Incremental state and cache

Internal analysis vocabulary (not permission to rename the public API): `InputFingerprint`, `OutputManifest`, `CacheKey`, `InvalidationReason`.

Hash declared inputs, tools, environment dimensions and dependency outputs. Write cache entries atomically with content verification. Explain rebuild reasons and detect undeclared-output risks.

Required observable invariant: Changing any declared input invalidates the correct targets; interrupted writes never create valid cache hits; fresh and cached builds yield equivalent artifacts.

### WP-05: Logs and reproducible integration

Internal analysis vocabulary (not permission to rename the public API): `BuildEvent`, `Diagnostic`, `BuildTrace`, `BootstrapManifest`.

Define ordered event stream and machine-readable diagnostics. Integrate packages/code/SDK through acyclic contracts. Make build tool self-hosting transition independently reproducible.

Required observable invariant: Bootstrap javac build and self-hosted build agree on artifacts; cancellation closes child processes; clean rebuild requires no private machine state.

## Bootstrap and dependency boundaries

XML streaming, ProcessBuilder, file hashing and executors; javac/jar bootstrap without Gradle or Maven framework dependencies.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MSBuild usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ProjectModel` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Conditional imports and property expansion are deterministic; import cycles report chains; glob behavior is tested for Windows/Linux case differences; evaluator never executes tasks. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
