# DJ-013 .j Aspire: Java architecture and contracts

Describe, launch, observe and deploy distributed application resource graphs.

Product type: Developer/orchestration tool. Proposed Java package root: `org.dotj.aspire`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-aspire-01 | ResourceId, ResourceSpec, ReferenceExpression | Application resource graph |
| dotj-aspire-02 | ResourceController, HealthState, ProcessHandle, ContainerHandle | Local orchestration and lifecycle |
| dotj-aspire-03 | EndpointReference, ConnectionDescriptor, IntegrationDescriptor | Service discovery and integration catalog |
| dotj-aspire-04 | ResourceSnapshot, LogStream, TraceLink, DashboardSession | Dashboard and observability |
| dotj-aspire-05 | DeploymentModel, Exporter, DeploymentDiff | Deployment export and operational parity |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Translate resource APIs to Java; dashboard and deployment formats require their own contracts. Do not reuse an existing Java Aspire implementation.

## Feature contracts and invariants

### WP-01: Application resource graph

Contract vocabulary: `ResourceId`, `ResourceSpec`, `ReferenceExpression`.

Define named resources dependencies endpoints and parameters. Validate graph cycles and unresolved references. Separate literal configuration from secret references.

Required observable invariant: Invalid graphs fail before launching anything; stable resource IDs survive serialization; secrets are not rendered into public manifests.

### WP-02: Local orchestration and lifecycle

Contract vocabulary: `ResourceController`, `HealthState`, `ProcessHandle`, `ContainerHandle`.

Map DCP-related source and protocol ownership. Launch dependencies according to readiness policies. Reconcile failures restarts shutdown and orphan cleanup.

Required observable invariant: A failed dependency blocks dependents with a reason; partial startup cleans owned children; user-owned processes are never terminated.

### WP-03: Service discovery and integration catalog

Contract vocabulary: `EndpointReference`, `ConnectionDescriptor`, `IntegrationDescriptor`.

Publish endpoint changes through extensions contracts. Specify adapters for databases brokers and external resources. Version integration requirements and isolate optional dependencies.

Required observable invariant: Endpoint rebinding reaches consumers; incompatible integrations fail before launch; disabled integrations introduce no runtime dependency.

### WP-04: Dashboard and observability

Contract vocabulary: `ResourceSnapshot`, `LogStream`, `TraceLink`, `DashboardSession`.

Build authenticated resource views and bounded live streams. Correlate service logs metrics traces and lifecycle events. Mask secrets in configuration and diagnostic exports.

Required observable invariant: Disconnected viewers release subscriptions; hostile log text is escaped; resource filters preserve correlation across restarts.

### WP-05: Deployment export and operational parity

Contract vocabulary: `DeploymentModel`, `Exporter`, `DeploymentDiff`.

Translate graph semantics into explicit backend resources. Report local-only features and unsupported deployment mappings. Validate generated artifacts without applying them.

Required observable invariant: Export never silently drops a required dependency; secret references stay external; repeated export is deterministic for locked inputs.

## Bootstrap and dependency boundaries

ProcessBuilder, HTTP clients and container-engine protocols; external orchestrator binaries are tool dependencies.

Proposed .j dependencies: extensions,web,containers. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Aspire usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ResourceId` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Invalid graphs fail before launching anything; stable resource IDs survive serialization; secrets are not rendered into public manifests. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
