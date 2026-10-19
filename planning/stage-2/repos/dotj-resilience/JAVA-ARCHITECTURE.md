# DJ-027 .j Resilience: Java architecture and contracts

Provide composable retries, timeouts, circuit breakers, bulkheads and rate-control strategies.

Product type: JVM resilience library. Proposed Java package root: `org.dotj.resilience`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-resilience-01 | ResiliencePipeline, ExecutionContext, Outcome | Pipeline and execution context |
| dotj-resilience-02 | RetryDecision, TimeoutBudget, FallbackResult | Retry timeout and fallback |
| dotj-resilience-03 | CircuitState, ProbeLease, PermitLease | Circuit breaker and concurrency limits |
| dotj-resilience-04 | HedgeAttempt, WinnerSelection, ResultDisposer | Hedging and result disposal |
| dotj-resilience-05 | StrategyEvent, HttpResilienceAdapter, VirtualClock | Telemetry adapters and deterministic tests |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Cancellation cannot safely stop arbitrary Java work. Separate timeout completion from underlying operation termination; preserve strategy ordering.

## Feature contracts and invariants

### WP-01: Pipeline and execution context

Contract vocabulary: `ResiliencePipeline`, `ExecutionContext`, `Outcome`.

Define ordered strategy composition and immutable reusable pipelines. Separate per-call state from shared strategy state. Propagate deadlines cancellation and operation identifiers.

Required observable invariant: Concurrent calls do not share attempt counters; context cleanup runs on every outcome; caller cancellation remains distinguishable from timeout.

### WP-02: Retry timeout and fallback

Contract vocabulary: `RetryDecision`, `TimeoutBudget`, `FallbackResult`.

Specify attempt counting backoff jitter and retry predicates. Budget total versus per-attempt timeout explicitly. Prevent fallback from swallowing cancellation by default.

Required observable invariant: Deterministic fake time reproduces attempts; retry-after handling is bounded; non-replayable operations require explicit caller policy.

### WP-03: Circuit breaker and concurrency limits

Contract vocabulary: `CircuitState`, `ProbeLease`, `PermitLease`.

Define closed/open/half-open transition races. Bound queued work and permit ownership. Separate rate limits from concurrency/bulkhead limits.

Required observable invariant: Only allowed probes enter half-open state; cancellation returns permits once; rejected work reports strategy-specific outcomes.

### WP-04: Hedging and result disposal

Contract vocabulary: `HedgeAttempt`, `WinnerSelection`, `ResultDisposer`.

Specify parallel attempt eligibility and winner rules. Cancel losing attempts without assuming remote rollback. Dispose losing owned results and bound concurrency.

Required observable invariant: No hedge occurs for ineligible requests; losing response bodies are closed; simultaneous completions yield one returned result.

### WP-05: Telemetry adapters and deterministic tests

Contract vocabulary: `StrategyEvent`, `HttpResilienceAdapter`, `VirtualClock`.

Emit bounded-cardinality strategy telemetry. Keep HTTP integration optional through core interfaces. Run race/property tests with fake time and seeded randomness.

Required observable invariant: Telemetry excludes payload secrets; retry fixtures are reproducible; composition order has explicit examples and acceptance outcomes.

## Bootstrap and dependency boundaries

Executors, ScheduledExecutorService, atomic state and monotonic clocks.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Polly usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ResiliencePipeline` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Concurrent calls do not share attempt counters; context cleanup runs on every outcome; caller cancellation remains distinguishable from timeout. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
