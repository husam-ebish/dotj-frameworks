# DJ-052 .j Mock: Java architecture and contracts

Offer configurable test doubles, argument matchers, verification and behavior sequences.

Product type: JVM mocking/instrumentation library. Proposed Java package root: `org.dotj.mock`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-mock-01 | Mock, Invocation, MethodKey, ArgumentMatcher | Mock model and invocation recording |
| dotj-mock-02 | Setup, Answer, Verification, Times | Setup return callbacks and verification |
| dotj-mock-03 | ProxyFactory, InstrumentationCapability, ClassTransform | Proxy and instrumentation feasibility |
| dotj-mock-04 | MockScope, InvocationStore, AgentSession | Lifecycle concurrency and cleanup |
| dotj-mock-05 | MockExpression, MatchSpecification, MockCase | Language adaptations and conformance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# expression-based setups need an owned invocation DSL. Final/static/private mocking is not assumed; capability tiers must be explicit.

## Feature contracts and invariants

### WP-01: Mock model and invocation recording

Contract vocabulary: `Mock`, `Invocation`, `MethodKey`, `ArgumentMatcher`.

Define strict/loose mocks defaults and invocation ordering. Resolve Java overloaded generic default and bridge methods. Record arguments with explicit snapshot/reference policy.

Required observable invariant: Overload identities do not collide; strict unexpected calls fail immediately; matcher state does not leak between threads.

### WP-02: Setup return callbacks and verification

Contract vocabulary: `Setup`, `Answer`, `Verification`, `Times`.

Implement matching precedence sequences callbacks and exceptions. Define verify/no-other-calls and asynchronous results. Handle recursive mocks with bounded identity rules.

Required observable invariant: Setup order is deterministic; failed verification shows actual calls; callbacks throwing still record invocation according to contract.

### WP-03: Proxy and instrumentation feasibility

Contract vocabulary: `ProxyFactory`, `InstrumentationCapability`, `ClassTransform`.

Start with JDK interface proxies. Investigate subclass generation final/static/private interception separately. Map DynamicProxy/Castle source dependency and bytecode-tool ownership.

Required observable invariant: Interface mocks work without an agent; unsupported member interception fails clearly; instrumentation is not secretly provided by Mockito/ByteBuddy.

### WP-04: Lifecycle concurrency and cleanup

Contract vocabulary: `MockScope`, `InvocationStore`, `AgentSession`.

Specify reset concurrent verification and shared mock behavior. Scope generated classes/classloaders and agent transformations. Restore transformed classes where supported.

Required observable invariant: Reset cannot corrupt active invocations; classloader stress shows no unbounded retention; failed transformations preserve valid classes.

### WP-05: Language adaptations and conformance

Contract vocabulary: `MockExpression`, `MatchSpecification`, `MockCase`.

Replace C# expression-tree setup with explicit Java invocation DSL. Document equality matcher and property-event adaptations. Port setup verification async and regression cases.

Required observable invariant: DSL validates method identity before use; adaptations are visible; upstream features without Java equivalents remain explicit coverage entries.

## Bootstrap and dependency boundaries

JDK Proxy for interfaces; class-file API, java.lang.instrument and optional agents for classes.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Moq usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `Mock` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Overload identities do not collide; strict unexpected calls fail immediately; matcher state does not leak between threads. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
