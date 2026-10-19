# DJ-029 .j Jobs: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Run durable background jobs with retries, scheduling, workers and administrative visibility.

Product type: Persistent JVM job framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-jobs-01 | JobDescriptor, JobState, StateTransition | Job representation and state machine |
| dotj-jobs-02 | JobStore, WorkerLease, QueueRecord | Persistent storage and atomic claims |
| dotj-jobs-03 | JobContext, JobFilter, WorkerPool | Worker execution filters and cancellation |
| dotj-jobs-04 | RecurringDefinition, Continuation, ScheduleOccurrence | Recurring jobs continuations and batches |
| dotj-jobs-05 | JobDashboard, QueueMetrics, RetentionPolicy | Dashboard and operational acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Serialized CLR method calls require Java invocation descriptors and allowlists; at-least-once processing demands application idempotency.

## Feature contracts and invariants

### WP-01: Job representation and state machine

Internal analysis vocabulary (not permission to rename the public API): `JobDescriptor`, `JobState`, `StateTransition`.

Serialize versioned Java method identifiers and arguments safely. Define enqueue scheduled processing succeeded failed and deleted states. Specify retries and expiration as explicit transitions.

Required observable invariant: Unknown method versions fail before invocation; arbitrary type activation is disabled; state history explains each retry.

### WP-02: Persistent storage and atomic claims

Internal analysis vocabulary (not permission to rename the public API): `JobStore`, `WorkerLease`, `QueueRecord`.

Define transactional enqueue and dequeue/claim contracts. Fence stale workers and recover expired claims. Inventory storage-provider sources and license requirements.

Required observable invariant: Two workers cannot hold the same valid claim under store assumptions; crashed workers become reclaimable; guarantees are stated per provider.

### WP-03: Worker execution filters and cancellation

Internal analysis vocabulary (not permission to rename the public API): `JobContext`, `JobFilter`, `WorkerPool`.

Order filters and manage scoped dependencies. Propagate shutdown cancellation without promising execution rollback. Record ambiguous outcomes and bound retry policy.

Required observable invariant: A side effect followed by crash is recognized as possibly duplicated; filter failures release resources; shutdown leaves recoverable job state.

### WP-04: Recurring jobs continuations and batches

Internal analysis vocabulary (not permission to rename the public API): `RecurringDefinition`, `Continuation`, `ScheduleOccurrence`.

Separate schedule calculation from durable enqueue. Define duplicate occurrence keys and continuation conditions. Keep commercial/extension-only features in a distinct provenance track.

Required observable invariant: DST/restart cases do not silently lose occurrence identity; continuations obey terminal conditions; unlicensed extensions are not copied.

### WP-05: Dashboard and operational acceptance

Internal analysis vocabulary (not permission to rename the public API): `JobDashboard`, `QueueMetrics`, `RetentionPolicy`.

Build optional authenticated web dashboard. Redact arguments and restrict retry/delete permissions. Test storage outage process death and poison jobs.

Required observable invariant: Dashboard cannot execute arbitrary methods; retained payloads obey policy; at-least-once limitations are visible in documentation.

## Bootstrap and dependency boundaries

Executors, own storage client and web stack.

Proposed .j dependencies: core,postgresql,scheduler;web(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Hangfire usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `JobDescriptor` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unknown method versions fail before invocation; arbitrary type activation is disabled; state history explains each retry. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
