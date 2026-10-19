# DJ-048 .j Structured Log: Java architecture and contracts

Provide structured message-template events with enrichers, filters and output pipelines.

Product type: JVM logging library. Proposed Java package root: `org.dotj.structured.log`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-structured-log-01 | MessageTemplate, LogEvent, PropertyValue | Message templates and property values |
| dotj-structured-log-02 | LoggerConfig, Enricher, Filter, LevelSwitch | Logger configuration enrichment and filtering |
| dotj-structured-log-03 | Sink, Batch, DeliveryPolicy | Sinks batching and backpressure |
| dotj-structured-log-04 | EventFormatter, ConfigurationReader, LoggingBridge | Formats integrations and configuration |
| dotj-structured-log-05 | TemplateCase, SinkFaultCase, AllocationReport | Compatibility and performance corpus |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve destructuring, scalar rendering and template tokens; log-event context propagation must work across Java executors.

## Feature contracts and invariants

### WP-01: Message templates and property values

Contract vocabulary: `MessageTemplate`, `LogEvent`, `PropertyValue`.

Parse positional/named tokens alignment and format hints. Separate structured capture from rendered text. Define destructuring depth cycles and scalar conversion.

Required observable invariant: Template holes bind deterministically; cycles cannot recurse forever; structured values survive independent formatting.

### WP-02: Logger configuration enrichment and filtering

Contract vocabulary: `LoggerConfig`, `Enricher`, `Filter`, `LevelSwitch`.

Define immutable logger branches and dynamic level controls. Specify enrichers property precedence and contextual scopes. Separate request context from global mutable state.

Required observable invariant: Concurrent scopes do not leak properties; duplicate enrichment precedence is stable; disabled levels avoid unnecessary value construction.

### WP-03: Sinks batching and backpressure

Contract vocabulary: `Sink`, `Batch`, `DeliveryPolicy`.

Define synchronous/asynchronous sink ownership. Bound queues and expose drop/block/fail behavior. Specify flushing shutdown and retry ambiguity.

Required observable invariant: Shutdown has a bounded flush result; queue overflow is observable; sink errors do not recurse through the same failing logger.

### WP-04: Formats integrations and configuration

Contract vocabulary: `EventFormatter`, `ConfigurationReader`, `LoggingBridge`.

Implement text/JSON formats with stable escaping. Keep files network sinks and configuration packages separately inventoried. Bridge core logging without destroying structured event semantics.

Required observable invariant: Formatting cannot inject extra JSON records; bridge retains template/properties where possible; optional sinks do not load in core logger.

### WP-05: Compatibility and performance corpus

Contract vocabulary: `TemplateCase`, `SinkFaultCase`, `AllocationReport`.

Port message-template destructuring and logger regressions. Measure disabled enabled synchronous and batched paths separately. Test concurrent logging during reconfiguration/disposal.

Required observable invariant: No caller-owned sink is closed unexpectedly; performance evidence names payloads and settings; Serilog behavior remains distinct from dotj-log.

## Bootstrap and dependency boundaries

Time APIs, concurrent queues and JDK output primitives.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Serilog usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `MessageTemplate` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Template holes bind deterministically; cycles cannot recurse forever; structured values survive independent formatting. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
