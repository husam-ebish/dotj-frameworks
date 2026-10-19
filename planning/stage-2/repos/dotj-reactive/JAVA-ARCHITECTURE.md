# DJ-028 .j Reactive: Java architecture and contracts

Implement observable sequences, operators, subjects and schedulers with owned semantics.

Product type: JVM concurrency library. Proposed Java package root: `org.dotj.reactive`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-reactive-01 | Observable, Observer, Subscription | Observable and observer protocol |
| dotj-reactive-02 | Scheduler, ScheduledAction, VirtualClock | Schedulers and virtual time |
| dotj-reactive-03 | OperatorPlan, ErrorPolicy, WindowState | Operators and error composition |
| dotj-reactive-04 | Subject, ReplayBuffer, RefCountState | Subjects sharing and concurrency |
| dotj-reactive-05 | FlowBridge, DemandPolicy, MarbleCase | Flow adapters and conformance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Rx push observables and Flow demand are different; use explicit bridge policies. Port disposal and terminal-event semantics rather than substituting Reactor.

## Feature contracts and invariants

### WP-01: Observable and observer protocol

Contract vocabulary: `Observable`, `Observer`, `Subscription`.

Specify serialized notifications terminal events and unsubscribe. Separate hot cold and shared source semantics. Define null acceptance and synchronous subscription failures.

Required observable invariant: No notification follows a terminal event; disposal is idempotent; synchronous errors follow the declared delivery rule.

### WP-02: Schedulers and virtual time

Contract vocabulary: `Scheduler`, `ScheduledAction`, `VirtualClock`.

Define immediate current-thread event-loop and worker scheduling. Specify recursive scheduling cancellation and clock units. Separate wall-clock time from monotonic durations.

Required observable invariant: Virtual-time traces are reproducible; cancellation removes pending work; recursive scheduling cannot unexpectedly overflow stack.

### WP-03: Operators and error composition

Contract vocabulary: `OperatorPlan`, `ErrorPolicy`, `WindowState`.

Inventory transformation combination filtering aggregation and time operators. Define ordering buffering and error propagation per operator. Use bounded-state policies where upstream semantics allow.

Required observable invariant: Merge/concat/switch have distinct traces; delayed errors preserve ordering; unbounded operators are documented with their memory behavior.

### WP-04: Subjects sharing and concurrency

Contract vocabulary: `Subject`, `ReplayBuffer`, `RefCountState`.

Specify subject serialization and replay termination behavior. Handle connect/refcount subscription races. Define buffer eviction by count and time.

Required observable invariant: Late subscribers see the documented terminal/replay sequence; refcount disconnects once; concurrent observers cannot corrupt state.

### WP-05: Flow adapters and conformance

Contract vocabulary: `FlowBridge`, `DemandPolicy`, `MarbleCase`.

Map Java Flow demand to explicitly documented observable policies. Port marble and scheduler regression fixtures. Test dropped buffered and failed overflow modes independently.

Required observable invariant: Push-only sources never claim native backpressure; adapter demand is honored; every implemented operator has trace-level acceptance.

## Bootstrap and dependency boundaries

Executors and java.util.concurrent.Flow where backpressure contracts align.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Reactive Extensions usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `Observable` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: No notification follows a terminal event; disposal is idempotent; synchronous errors follow the declared delivery rule. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
