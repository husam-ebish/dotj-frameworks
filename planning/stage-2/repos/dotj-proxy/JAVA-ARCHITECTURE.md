# DJ-014 .j Proxy: Java architecture and contracts

Build programmable HTTP reverse proxy routing, transforms and resilient forwarding.

Product type: JVM networking library. Proposed Java package root: `org.dotj.proxy`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-proxy-01 | ProxyRoute, ClusterSnapshot, DestinationState | Route and cluster configuration |
| dotj-proxy-02 | ForwardingContext, HeaderTransform, DuplexTunnel | Streaming forwarding and transforms |
| dotj-proxy-03 | LoadBalancingPolicy, AffinityToken, HealthReport | Balancing affinity and health |
| dotj-proxy-04 | ForwardAttempt, RetryDecision, TimeoutBudget | Retry timeout and security boundaries |
| dotj-proxy-05 | ProxyCapabilityMatrix, RouteMetrics, FaultScenario | Protocol and operational acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve forwarding semantics including headers, trailers, cancellation and WebSockets; a simple HTTP relay does not establish YARP parity.

## Feature contracts and invariants

### WP-01: Route and cluster configuration

Contract vocabulary: `ProxyRoute`, `ClusterSnapshot`, `DestinationState`.

Validate route matching priorities and destination references. Publish immutable configuration snapshots with revision IDs. Drain removed destinations without corrupting active requests.

Required observable invariant: Invalid reload preserves last good snapshot; each request sees one revision; removed backends stop receiving new work.

### WP-02: Streaming forwarding and transforms

Contract vocabulary: `ForwardingContext`, `HeaderTransform`, `DuplexTunnel`.

Define end-to-end body trailers and cancellation ownership. Remove hop-by-hop headers and normalize forwarding metadata. Support upgrades only through capable transport adapters.

Required observable invariant: Request/response bodies are not fully buffered by default; smuggling cases are rejected; tunnel disconnect closes both owned halves.

### WP-03: Balancing affinity and health

Contract vocabulary: `LoadBalancingPolicy`, `AffinityToken`, `HealthReport`.

Implement deterministic policy inputs and destination eligibility. Define active/passive health timing and recovery. Bind affinity state to validated cluster identities.

Required observable invariant: Unhealthy destinations are excluded as configured; stale affinity cannot cross clusters; health flapping obeys explicit recovery policy.

### WP-04: Retry timeout and security boundaries

Contract vocabulary: `ForwardAttempt`, `RetryDecision`, `TimeoutBudget`.

Separate connection failures from potentially committed requests. Budget retries through resilience contracts without duplicating bodies. Specify trusted proxy boundaries and TLS backend validation.

Required observable invariant: Non-replayable requests are not silently retried; cancellation stops all attempts; untrusted forwarded headers cannot change authenticated origin.

### WP-05: Protocol and operational acceptance

Contract vocabulary: `ProxyCapabilityMatrix`, `RouteMetrics`, `FaultScenario`.

Exercise HTTP versions WebSockets and trailers independently. Measure bounded memory under slow clients/backends. Test reload shutdown and destination failure concurrently.

Required observable invariant: Each advertised forwarding feature has wire evidence; active drain has a bounded outcome; diagnostic labels do not contain unbounded URLs.

## Bootstrap and dependency boundaries

Owned web transport plus JDK HTTP client where semantics suffice; SSLEngine for TLS.

Proposed .j dependencies: web,resilience,extensions. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing YARP usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ProxyRoute` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Invalid reload preserves last good snapshot; each request sees one revision; removed backends stop receiving new work. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
