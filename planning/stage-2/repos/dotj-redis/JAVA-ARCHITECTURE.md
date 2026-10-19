# DJ-022 .j Redis: Java architecture and contracts

Provide an owned Redis client with multiplexing, routing and resilient connection management.

Product type: JVM network client. Proposed Java package root: `org.dotj.redis`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-redis-01 | RespValue, CommandDescriptor, ReplyDecoder | RESP parsing and command metadata |
| dotj-redis-02 | PendingCommand, ConnectionEpoch, CompletionState | Multiplexed connections and reconnect |
| dotj-redis-03 | HashSlot, TopologySnapshot, Redirect | Cluster sentinel and routing |
| dotj-redis-04 | TransactionQueue, ScriptHandle, SubscriptionState | Transactions scripts and subscriptions |
| dotj-redis-05 | CommandCoverage, ServerProfile, ConnectionDiagnostics | Command coverage and operational validation |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve command ordering and result distinctions; reconnect cannot silently replay non-idempotent commands. Redis server license is separate from client source terms.

## Feature contracts and invariants

### WP-01: RESP parsing and command metadata

Contract vocabulary: `RespValue`, `CommandDescriptor`, `ReplyDecoder`.

Keep null empty bulk array map and error variants distinct. Define bounded streaming parser behavior for negotiated RESP versions. Attach key-routing and replay metadata to every command.

Required observable invariant: Fragmented frames decode identically; oversized replies fail safely; unknown commands cannot inherit unsafe retry assumptions.

### WP-02: Multiplexed connections and reconnect

Contract vocabulary: `PendingCommand`, `ConnectionEpoch`, `CompletionState`.

Preserve send/reply ordering and pending-command ownership. Separate definitely-unsent commands from ambiguous writes. Define reconnect authentication and database selection.

Required observable invariant: Disconnect cannot associate old replies with a new connection; non-idempotent ambiguous writes are not silently replayed; pending futures settle.

### WP-03: Cluster sentinel and routing

Contract vocabulary: `HashSlot`, `TopologySnapshot`, `Redirect`.

Compute key slots and validate multi-key constraints. Handle MOVED ASK topology refresh and failover epochs. Separate sentinel control channels from data channels.

Required observable invariant: ASK does not permanently rewrite ownership; redirect loops are bounded; stale topology cannot route cross-slot transactions silently.

### WP-04: Transactions scripts and subscriptions

Contract vocabulary: `TransactionQueue`, `ScriptHandle`, `SubscriptionState`.

Define WATCH/MULTI/EXEC result and failure semantics. Handle script-cache misses without changing command guarantees. Isolate pubsub and blocking commands from normal multiplexing.

Required observable invariant: Aborted transactions remain distinguishable from empty results; reconnect resubscription is documented; slow consumers have bounded queues.

### WP-05: Command coverage and operational validation

Contract vocabulary: `CommandCoverage`, `ServerProfile`, `ConnectionDiagnostics`.

Inventory upstream command families and supported server versions. Test TLS timeouts failover and response-size pressure. Document client source licensing separately from server deployment terms.

Required observable invariant: Every claimed command has routing/codec fixtures; unavailable server features return explicit errors; diagnostics redact authentication material.

## Bootstrap and dependency boundaries

NIO sockets, TLS, executors and buffers.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing StackExchange.Redis usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `RespValue` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Fragmented frames decode identically; oversized replies fail safely; unknown commands cannot inherit unsafe retry assumptions. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
