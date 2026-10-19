# DJ-050 .j XTest: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Implement xUnit-style discovery, lifecycle, data tests, assertions and runner integration.

Product type: JVM test framework/tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-xtest-01 | TestCaseId, Fact, Theory, DiscoveryMessage | Discovery attributes and test identity |
| dotj-xtest-02 | TestContext, FixtureScope, ExecutionResult | Fixtures lifetime and execution |
| dotj-xtest-03 | AssertionFailure, DataProvider, ComparisonPolicy | Assertions and data theories |
| dotj-xtest-04 | RunnerMessage, ExecutionCollection, ReportWriter | Runner protocols parallelism and reporting |
| dotj-xtest-05 | StandaloneRunner, CompatibilityFixture, Adapter | Bootstrap and upstream conformance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Fact/Theory metadata adapts to annotations; assembly isolation becomes classloader/process isolation with explicit fixture lifetimes.

## Feature contracts and invariants

### WP-01: Discovery attributes and test identity

Internal analysis vocabulary (not permission to rename the public API): `TestCaseId`, `Fact`, `Theory`, `DiscoveryMessage`.

Map xUnit-style test metadata into Java annotations. Separate discovery from execution and avoid static initialization. Create stable IDs including parameter cases and source identity.

Required observable invariant: Discovery is deterministic; malformed theories report discovery errors; IDs stay stable under unrelated source changes.

### WP-02: Fixtures lifetime and execution

Internal analysis vocabulary (not permission to rename the public API): `TestContext`, `FixtureScope`, `ExecutionResult`.

Define test/class/collection fixture creation and cleanup. Specify async tests timeouts skips and cancellation. Capture multiple teardown failures without losing primary error.

Required observable invariant: Fixtures dispose once; failed setup prevents test body; teardown errors remain visible beside assertion failure.

### WP-03: Assertions and data theories

Internal analysis vocabulary (not permission to rename the public API): `AssertionFailure`, `DataProvider`, `ComparisonPolicy`.

Implement assertion families with useful structural diffs. Enumerate theory data under explicit resource ownership. Define equality floating-point exception and asynchronous assertion semantics.

Required observable invariant: Failure output identifies first meaningful difference; data streams close; async exceptions are observed rather than lost.

### WP-04: Runner protocols parallelism and reporting

Internal analysis vocabulary (not permission to rename the public API): `RunnerMessage`, `ExecutionCollection`, `ReportWriter`.

Define message ordering and process isolation. Schedule collections with explicit parallelism rules. Emit machine-readable reports and stable exit codes.

Required observable invariant: A crashed worker is distinguishable from failed tests; nonparallel collections are honored; report totals reconcile with discovered/executed cases.

### WP-05: Bootstrap and upstream conformance

Internal analysis vocabulary (not permission to rename the public API): `StandaloneRunner`, `CompatibilityFixture`, `Adapter`.

Bootstrap assertions/runner with javac and plain Java mains. Port discovery fixture assertion and runner regressions. Add SDK/IDE adapters only after standalone execution works.

Required observable invariant: No JUnit engine supplies the implementation; self-tests include an independent subprocess oracle; adapter failures cannot masquerade as green tests.

## Bootstrap and dependency boundaries

Reflection/annotations, subprocesses and executors; standalone JDK assertion harness bootstraps.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing xUnit.net usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `TestCaseId` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Discovery is deterministic; malformed theories report discovery errors; IDs stay stable under unrelated source changes. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
