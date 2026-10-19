# DJ-030 .j Scheduler: Java architecture and contracts

Implement calendar/cron scheduling, persistent triggers and clustered execution.

Product type: JVM scheduling library. Proposed Java package root: `org.dotj.scheduler`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-scheduler-01 | JobKey, TriggerKey, CalendarExclusion | Jobs triggers and calendars |
| dotj-scheduler-02 | NextFireTime, MisfireInstruction, SchedulerClock | Misfires scheduling and clocks |
| dotj-scheduler-03 | TriggerStore, SchedulerInstance, AcquisitionLease | Persistent store and clustering |
| dotj-scheduler-04 | JobExecutionContext, Listener, InterruptRequest | Execution listeners and lifecycle |
| dotj-scheduler-05 | StoreAdapter, ScheduleTrace, ManagementApi | Adapters and verification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Quartz.NET behavior is the source; do not reuse Java Quartz. Preserve DST/misfire semantics explicitly and compare time-zone data versions.

## Feature contracts and invariants

### WP-01: Jobs triggers and calendars

Contract vocabulary: `JobKey`, `TriggerKey`, `CalendarExclusion`.

Define job data durability and trigger association. Parse cron/simple triggers under an explicit timezone model. Apply exclusion calendars and boundary rules.

Required observable invariant: DST gaps/overlaps have fixture-backed outcomes; invalid cron fails with location; calendars do not silently change timezone.

### WP-02: Misfires scheduling and clocks

Contract vocabulary: `NextFireTime`, `MisfireInstruction`, `SchedulerClock`.

Define misfire thresholds and each catch-up policy. Separate monotonic waits from civil-time calculations. Handle clock jumps and paused triggers.

Required observable invariant: Restart after downtime produces the documented firing sequence; clock adjustments do not spin indefinitely; pause/resume retains policy.

### WP-03: Persistent store and clustering

Contract vocabulary: `TriggerStore`, `SchedulerInstance`, `AcquisitionLease`.

Specify transaction isolation and trigger acquisition. Fence stale clustered scheduler instances. Recover interrupted firings with explicit re-execution semantics.

Required observable invariant: Concurrent nodes do not acquire one occurrence twice under declared store guarantees; recovery does not claim exactly-once side effects.

### WP-04: Execution listeners and lifecycle

Contract vocabulary: `JobExecutionContext`, `Listener`, `InterruptRequest`.

Define listener ordering veto and exception behavior. Enforce configured per-job concurrency restrictions. Bound shutdown and interrupt signaling.

Required observable invariant: Listener failure cannot leak a worker; nonconcurrent jobs serialize correctly; interrupt remains cooperative and observable.

### WP-05: Adapters and verification

Contract vocabulary: `StoreAdapter`, `ScheduleTrace`, `ManagementApi`.

Keep persistence and hosting adapters optional. Port cron/calendar/misfire fixtures using fake time. Run database contention and node-restart scenarios.

Required observable invariant: Core schedule calculation works without a database; test traces identify timezone data version; every claimed store has recovery evidence.

## Bootstrap and dependency boundaries

java.time, monotonic timing, executors and JDBC-compatible storage.

Proposed .j dependencies: core;postgresql(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Quartz.NET usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `JobKey` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: DST gaps/overlaps have fixture-backed outcomes; invalid cron fails with location; calendars do not silently change timezone. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
