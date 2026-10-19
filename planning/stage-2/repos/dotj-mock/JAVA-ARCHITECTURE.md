# DJ-052 .j Mock: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Offer configurable test doubles, argument matchers, verification and behavior sequences.

Product type: JVM mocking/instrumentation library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-mock-01 | Mock, Invocation, MethodKey, ArgumentMatcher | Mock model and invocation recording |
| dotj-mock-02 | Setup, Answer, Verification, Times | Setup return callbacks and verification |
| dotj-mock-03 | ProxyFactory, InstrumentationCapability, ClassTransform | Proxy and instrumentation feasibility |
| dotj-mock-04 | MockScope, InvocationStore, AgentSession | Lifecycle concurrency and cleanup |
| dotj-mock-05 | MockExpression, MatchSpecification, MockCase | Language adaptations and conformance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# expression-based setups need an owned invocation DSL. Final/static/private mocking is not assumed; capability tiers must be explicit.

## Feature contracts and invariants

### WP-01: Mock model and invocation recording

Internal analysis vocabulary (not permission to rename the public API): `Mock`, `Invocation`, `MethodKey`, `ArgumentMatcher`.

Define strict/loose mocks defaults and invocation ordering. Resolve Java overloaded generic default and bridge methods. Record arguments with explicit snapshot/reference policy.

Required observable invariant: Overload identities do not collide; strict unexpected calls fail immediately; matcher state does not leak between threads.

### WP-02: Setup return callbacks and verification

Internal analysis vocabulary (not permission to rename the public API): `Setup`, `Answer`, `Verification`, `Times`.

Implement matching precedence sequences callbacks and exceptions. Define verify/no-other-calls and asynchronous results. Handle recursive mocks with bounded identity rules.

Required observable invariant: Setup order is deterministic; failed verification shows actual calls; callbacks throwing still record invocation according to contract.

### WP-03: Proxy and instrumentation feasibility

Internal analysis vocabulary (not permission to rename the public API): `ProxyFactory`, `InstrumentationCapability`, `ClassTransform`.

Start with JDK interface proxies. Investigate subclass generation final/static/private interception separately. Map DynamicProxy/Castle source dependency and bytecode-tool ownership.

Required observable invariant: Interface mocks work without an agent; unsupported member interception fails clearly; instrumentation is not secretly provided by Mockito/ByteBuddy.

### WP-04: Lifecycle concurrency and cleanup

Internal analysis vocabulary (not permission to rename the public API): `MockScope`, `InvocationStore`, `AgentSession`.

Specify reset concurrent verification and shared mock behavior. Scope generated classes/classloaders and agent transformations. Restore transformed classes where supported.

Required observable invariant: Reset cannot corrupt active invocations; classloader stress shows no unbounded retention; failed transformations preserve valid classes.

### WP-05: Language adaptations and conformance

Internal analysis vocabulary (not permission to rename the public API): `MockExpression`, `MatchSpecification`, `MockCase`.

Preserve Moq public setup names/concepts and investigate Java expression capture or generated representations; keep any internal invocation IR hidden. Document equality matcher and property-event adaptations. Port setup verification async and regression cases.

Required observable invariant: Setup expression representation validates the original method identity before use; adaptations are visible; upstream features without Java equivalents remain explicit coverage entries.

## Bootstrap and dependency boundaries

JDK Proxy for interfaces; class-file API, java.lang.instrument and optional agents for classes.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Moq usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `Mock` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Overload identities do not collide; strict unexpected calls fail immediately; matcher state does not leak between threads. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Public API direction under the owner requirement

Preserve Moq public names and setup/verification concepts, including Mock, Setup and Verify where declared. A separately named Java invocation DSL is not the default user-facing design. Investigate source-generation/expression capture while retaining unsupported syntax explicitly.
