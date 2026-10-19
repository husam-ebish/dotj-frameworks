# DJ-053 .j Substitute: Java architecture and contracts

Provide concise substitutes, received-call assertions and return configuration.

Product type: JVM mocking library. Proposed Java package root: `org.dotj.substitute`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-substitute-01 | Substitute, CallSpecification, ArgumentSpecification | Substitution and call specification |
| dotj-substitute-02 | ReturnSequence, CallAction, AutoValueProvider | Returns callbacks and recursive values |
| dotj-substitute-03 | ReceivedCheck, CallOrder, EventAdapter | Received calls order and events |
| dotj-substitute-04 | SubstituteFactory, InterceptionCapability, ConfigurationScope | Proxy instrumentation and thread state |
| dotj-substitute-05 | SubstituteCase, AssertionAdapter, CleanupRecord | Integration and regression acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Thread-local recording and fluent setup must avoid consuming production calls; Java primitive defaults and overloads need a documented DSL.

## Feature contracts and invariants

### WP-01: Substitution and call specification

Contract vocabulary: `Substitute`, `CallSpecification`, `ArgumentSpecification`.

Define interface substitution and supported class boundaries. Resolve matcher ambiguity and overloaded calls. Separate call recording from configuration calls.

Required observable invariant: Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable.

### WP-02: Returns callbacks and recursive values

Contract vocabulary: `ReturnSequence`, `CallAction`, `AutoValueProvider`.

Specify return precedence sequential values and exceptions. Support out/ref-like semantics only through explicit Java holders. Bound recursive substitute creation and cache identities.

Required observable invariant: Exhausted sequences obey documented policy; holder adaptation is explicit; recursive substitutes remain stable per configured path.

### WP-03: Received calls order and events

Contract vocabulary: `ReceivedCheck`, `CallOrder`, `EventAdapter`.

Define received/not-received cardinality and argument predicates. Implement ordered assertions with useful traces. Map C# event behavior to Java listener contracts.

Required observable invariant: Order checks identify missing/out-of-order calls; predicate errors are diagnosable; listener raises follow declared exception rules.

### WP-04: Proxy instrumentation and thread state

Contract vocabulary: `SubstituteFactory`, `InterceptionCapability`, `ConfigurationScope`.

Use JDK interface proxies as the initial capability. Gate class interception on separately owned bytecode research. Isolate ambient call-specification state under concurrency.

Required observable invariant: Parallel configuration cannot cross-contaminate substitutes; unsupported members fail explicitly; no Mockito implementation is adopted.

### WP-05: Integration and regression acceptance

Contract vocabulary: `SubstituteCase`, `AssertionAdapter`, `CleanupRecord`.

Keep test-runner integrations optional. Port call matching recursive values and concurrency regressions. Check generated-class lifecycle and reset behavior.

Required observable invariant: Substitutes run independently of NUnit/xUnit ports; reset clears only owned state; instrumentation capabilities are reported accurately.

## Bootstrap and dependency boundaries

JDK interfaces/proxies and optional owned bytecode bridge.

Proposed .j dependencies: core;mock(optional-spi). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NSubstitute usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `Substitute` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
