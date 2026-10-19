# DJ-054 .j Coverage: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Measure Java line/branch coverage and produce interoperable reports.

Product type: JVM instrumentation/tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-coverage-01 | ClassModel, ProbeId, InstrumentationPlan | Instrumentation and JVM bytecode model |
| dotj-coverage-02 | SourceSpan, BranchId, LineCoverage | Source mapping and coverage semantics |
| dotj-coverage-03 | CoverageSession, ProbeBuffer, MergeKey | Collection merging and process lifecycle |
| dotj-coverage-04 | CoverageFilter, CoverageReport, ThresholdPolicy | Filters reports and CI integration |
| dotj-coverage-05 | SemanticFixture, AgentCompatibility, OverheadResult | Instrumentation qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

IL/PDB rewriting becomes bytecode/LineNumberTable analysis; async/generated Java code needs distinct exclusion rules.

## Feature contracts and invariants

### WP-01: Instrumentation and JVM bytecode model

Internal analysis vocabulary (not permission to rename the public API): `ClassModel`, `ProbeId`, `InstrumentationPlan`.

Inventory CLR IL/PDB operations requiring JVM equivalents. Define classfile parser/writer ownership and verifier constraints. Insert probes without changing program semantics.

Required observable invariant: Instrumented classes pass verification; constructors/exceptions/synchronized blocks behave equivalently; unsupported bytecode versions fail explicitly.

### WP-02: Source mapping and coverage semantics

Internal analysis vocabulary (not permission to rename the public API): `SourceSpan`, `BranchId`, `LineCoverage`.

Map bytecode debug tables to Java source lines/methods. Define branch denominator and synthetic/generated-code handling. Separate CLR coverage import from native Java collection.

Required observable invariant: Reported totals reconcile with declared denominator; missing debug info is visible; IL branches are not relabeled JVM branches.

### WP-03: Collection merging and process lifecycle

Internal analysis vocabulary (not permission to rename the public API): `CoverageSession`, `ProbeBuffer`, `MergeKey`.

Collect across threads forks and shutdown paths. Merge using class/source identity rather than filename alone. Handle crash/partial data without false zero coverage.

Required observable invariant: Duplicate sessions do not double-count; changed classes cannot merge silently; incomplete runs are marked incomplete.

### WP-04: Filters reports and CI integration

Internal analysis vocabulary (not permission to rename the public API): `CoverageFilter`, `CoverageReport`, `ThresholdPolicy`.

Define include/exclude generated-code and test-assembly filters. Export explicitly supported report formats. Integrate SDK/test runners through optional adapters.

Required observable invariant: Filters are explainable; report totals match raw data; threshold failures distinguish missing data from insufficient coverage.

### WP-05: Instrumentation qualification

Internal analysis vocabulary (not permission to rename the public API): `SemanticFixture`, `AgentCompatibility`, `OverheadResult`.

Run differential programs with/without instrumentation. Test other agents classloaders modules and retransformation. Measure probe overhead against fixed workloads.

Required observable invariant: No claimed support without verifier/semantic evidence; incompatible agents are diagnosed; no JaCoCo substitution supplies coverage implementation.

## Bootstrap and dependency boundaries

java.lang.instrument, standard class-file API and classloaders.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Coverlet usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ClassModel` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Instrumented classes pass verification; constructors/exceptions/synchronized blocks behave equivalently; unsupported bytecode versions fail explicitly. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
