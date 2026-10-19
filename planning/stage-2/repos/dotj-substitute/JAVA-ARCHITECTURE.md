# DJ-053 .j Substitute: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide concise substitutes, received-call assertions and return configuration.

Product type: JVM mocking library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-substitute-01 | Substitute, CallSpecification, ArgumentSpecification | Substitution and call specification |
| dotj-substitute-02 | ReturnSequence, CallAction, AutoValueProvider | Returns callbacks and recursive values |
| dotj-substitute-03 | ReceivedCheck, CallOrder, EventAdapter | Received calls order and events |
| dotj-substitute-04 | SubstituteFactory, InterceptionCapability, ConfigurationScope | Proxy instrumentation and thread state |
| dotj-substitute-05 | SubstituteCase, AssertionAdapter, CleanupRecord | Integration and regression acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Thread-local recording and fluent setup must avoid consuming production calls; Java primitive defaults and overloads need a documented DSL.

## Feature contracts and invariants

### WP-01: Substitution and call specification

Internal analysis vocabulary (not permission to rename the public API): `Substitute`, `CallSpecification`, `ArgumentSpecification`.

Define interface substitution and supported class boundaries. Resolve matcher ambiguity and overloaded calls. Separate call recording from configuration calls.

Required observable invariant: Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable.

### WP-02: Returns callbacks and recursive values

Internal analysis vocabulary (not permission to rename the public API): `ReturnSequence`, `CallAction`, `AutoValueProvider`.

Specify return precedence sequential values and exceptions. Support out/ref-like semantics only through explicit Java holders. Bound recursive substitute creation and cache identities.

Required observable invariant: Exhausted sequences obey documented policy; holder adaptation is explicit; recursive substitutes remain stable per configured path.

### WP-03: Received calls order and events

Internal analysis vocabulary (not permission to rename the public API): `ReceivedCheck`, `CallOrder`, `EventAdapter`.

Define received/not-received cardinality and argument predicates. Implement ordered assertions with useful traces. Map C# event behavior to Java listener contracts.

Required observable invariant: Order checks identify missing/out-of-order calls; predicate errors are diagnosable; listener raises follow declared exception rules.

### WP-04: Proxy instrumentation and thread state

Internal analysis vocabulary (not permission to rename the public API): `SubstituteFactory`, `InterceptionCapability`, `ConfigurationScope`.

Use JDK interface proxies as the initial capability. Gate class interception on separately owned bytecode research. Isolate ambient call-specification state under concurrency.

Required observable invariant: Parallel configuration cannot cross-contaminate substitutes; unsupported members fail explicitly; no Mockito implementation is adopted.

### WP-05: Integration and regression acceptance

Internal analysis vocabulary (not permission to rename the public API): `SubstituteCase`, `AssertionAdapter`, `CleanupRecord`.

Keep test-runner integrations optional. Port call matching recursive values and concurrency regressions. Check generated-class lifecycle and reset behavior.

Required observable invariant: Substitutes run independently of NUnit/xUnit ports; reset clears only owned state; instrumentation capabilities are reported accurately.

## Bootstrap and dependency boundaries

JDK interfaces/proxies and optional owned bytecode bridge.

Proposed .j dependencies: core;mock(optional-spi). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NSubstitute usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `Substitute` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Public API direction under the owner requirement

Preserve NSubstitute public names and call/return/received concepts, including Substitute.For, Returns and Received where declared. Java proxy machinery is internal; do not force adoption of a renamed mocking API.
