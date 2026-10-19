# DJ-065 .j Mediator: Java architecture and contracts

Provide in-process request/response, notifications and composable pipeline behavior.

Product type: JVM application library. Proposed Java package root: `org.dotj.mediator`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-mediator-01 | MediatorLicenseRecord, Request, Handler, Response | License baseline requests and handlers |
| dotj-mediator-02 | PipelineBehavior, RequestContext, ExceptionHandler | Pipeline behaviors and exception handling |
| dotj-mediator-03 | Notification, NotificationHandler, PublishStrategy | Notifications publishing and concurrency |
| dotj-mediator-04 | StreamRequest, StreamHandler, StreamBehavior | Streaming requests and lifecycle |
| dotj-mediator-05 | MediatorRegistry, CoreDiAdapter, MediatorCase | Registration adapters and verification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve handler resolution and pipeline order; generic variance and streaming cancellation need Java-specific contracts.

## Feature contracts and invariants

### WP-01: License baseline requests and handlers

Contract vocabulary: `MediatorLicenseRecord`, `Request`, `Handler`, `Response`.

Freeze inspected MediatR revision and license path. Define typed request/response and handler cardinality. Validate registration without executing handlers.

Required observable invariant: Source reuse waits for rights resolution; missing/multiple handlers fail explicitly; generic request identity survives erasure through tokens.

### WP-02: Pipeline behaviors and exception handling

Contract vocabulary: `PipelineBehavior`, `RequestContext`, `ExceptionHandler`.

Define pre/post processor nesting and exception actions. Propagate cancellation and explicit context. Separate handler failures from pipeline construction errors.

Required observable invariant: Behavior order is deterministic; cleanup runs on failure; exception handling cannot accidentally invoke the request twice.

### WP-03: Notifications publishing and concurrency

Contract vocabulary: `Notification`, `NotificationHandler`, `PublishStrategy`.

Specify sequential and parallel publish strategies. Define aggregate failures and cancellation policy. Preserve per-publication scoped dependencies.

Required observable invariant: Parallel failures are not lost; sequential strategy has stable ordering; scoped handlers are disposed after completion.

### WP-04: Streaming requests and lifecycle

Contract vocabulary: `StreamRequest`, `StreamHandler`, `StreamBehavior`.

Define lazy stream creation backpressure and cancellation. Wrap stream enumeration in pipeline lifecycle. Dispose handlers/resources when consumers stop early.

Required observable invariant: Early termination closes owned resources; exceptions preserve stream context; no hidden unbounded buffering is introduced.

### WP-05: Registration adapters and verification

Contract vocabulary: `MediatorRegistry`, `CoreDiAdapter`, `MediatorCase`.

Keep core DI integration optional. Port request pipeline notification streaming regressions after license gate. Provide deterministic registration diagnostics.

Required observable invariant: Base mediator works with explicit factories; no event bus is substituted; rights status and compatibility evidence remain separate.

## Bootstrap and dependency boundaries

Functional interfaces, type tokens, CompletionStage and Flow where explicit.

Proposed .j dependencies: core;container(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MediatR usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `MediatorLicenseRecord` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Source reuse waits for rights resolution; missing/multiple handlers fail explicitly; generic request identity survives erasure through tokens. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
