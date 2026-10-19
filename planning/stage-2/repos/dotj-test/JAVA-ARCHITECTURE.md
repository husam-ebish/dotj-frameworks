# DJ-051 .j Test: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Implement NUnit-style fixtures, parameterized tests, constraints and execution policies.

Product type: JVM test framework/tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-test-01 | TestSuite, TestCase, TestAttribute, Category | Test model discovery and attributes |
| dotj-test-02 | Constraint, ConstraintResult, ActualValue | Constraint assertions and diagnostics |
| dotj-test-03 | LifecyclePlan, ExecutionContext, TestResult | Setup teardown and execution context |
| dotj-test-04 | CaseSource, ParallelScope, WorkerSession | Parameterized parallel and isolated execution |
| dotj-test-05 | EngineProtocol, ResultXml, ExtensionPoint | Runner reporting extensions and bootstrap |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# attributes and generic fixtures map to Java annotation/type-token policies; apartment-state tests remain platform-specific.

## Feature contracts and invariants

### WP-01: Test model discovery and attributes

Internal analysis vocabulary (not permission to rename the public API): `TestSuite`, `TestCase`, `TestAttribute`, `Category`.

Map NUnit-style fixture parameterization categories and setup metadata. Define inheritance and generic fixture adaptations for Java. Build stable test identities and deterministic discovery.

Required observable invariant: Invalid fixture combinations produce explicit errors; category filters are reproducible; discovery does not execute test bodies.

### WP-02: Constraint assertions and diagnostics

Internal analysis vocabulary (not permission to rename the public API): `Constraint`, `ConstraintResult`, `ActualValue`.

Implement composable constraint syntax and deferred evaluation. Define collection string numeric and exception comparisons. Preserve rich failure messages without repeated side effects.

Required observable invariant: Actual-value suppliers execute according to contract; compound constraints report meaningful subfailures; tolerance semantics are explicit.

### WP-03: Setup teardown and execution context

Internal analysis vocabulary (not permission to rename the public API): `LifecyclePlan`, `ExecutionContext`, `TestResult`.

Specify one-time/per-test setup order through inheritance. Handle async lifecycle failures and multiple cleanup errors. Scope output culture and test-local context.

Required observable invariant: Failed setup has documented teardown behavior; context cannot leak across parallel tests; original failures survive cleanup exceptions.

### WP-04: Parameterized parallel and isolated execution

Internal analysis vocabulary (not permission to rename the public API): `CaseSource`, `ParallelScope`, `WorkerSession`.

Enumerate combinatorial/range/case-source data deterministically. Define fixture-level concurrency and nonparallel regions. Use process isolation for uncooperative timeout cases.

Required observable invariant: Case explosion has explicit limits; nonparallel rules are enforced; timed-out processes cannot corrupt runner state.

### WP-05: Runner reporting extensions and bootstrap

Internal analysis vocabulary (not permission to rename the public API): `EngineProtocol`, `ResultXml`, `ExtensionPoint`.

Separate framework from runner/engine and external adapters. Emit versioned result schema and stable exit codes. Bootstrap without xUnit/JUnit dependency then port regressions.

Required observable invariant: Framework can run under a minimal owned harness; crashed tests have distinct results; external engine sources remain separately tracked.

## Bootstrap and dependency boundaries

Reflection, classloaders, executors and XML.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NUnit usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `TestSuite` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Invalid fixture combinations produce explicit errors; category filters are reproducible; discovery does not execute test bodies. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Required SDK integration

Supply this product's qualified adapters/assets to [the SDK and distribution plan](../../10-SDK-AND-DISTRIBUTION-PLAN.md), using the [named integration tasks](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md). Exact .NET API and command names/concepts remain mandatory. Core enables the independent bootstrap; compiler/build/test tools provide real execution adapters; containers and platform frameworks qualify their own runtime/publish capabilities before the SDK advertises them.
