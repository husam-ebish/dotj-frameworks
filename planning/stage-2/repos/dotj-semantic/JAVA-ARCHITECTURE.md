# DJ-061 .j Semantic: Java architecture and contracts

Port the C# kernel/plugin, model connector and orchestration capabilities to owned Java modules.

Product type: JVM AI orchestration library. Proposed Java package root: `org.dotj.semantic`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-semantic-01 | Kernel, FunctionDescriptor, InvocationContext | Kernel functions plugins and invocation |
| dotj-semantic-02 | ChatService, EmbeddingService, StreamingContent | AI connectors chat streaming and embeddings |
| dotj-semantic-03 | PromptTemplate, ToolPolicy, PlanStep | Prompt templates planning and tool execution |
| dotj-semantic-04 | MemoryRecord, VectorAdapter, AgentState, ProcessState | Memory vector data agents and process families |
| dotj-semantic-05 | SemanticProfile, EvaluationCase, MigrationMap | Lifecycle successor boundary and evaluation |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

The upstream is multi-language: inspect C# functionality and do not reuse its Java implementation. Provider schemas evolve independently of framework API parity.

## Feature contracts and invariants

### WP-01: Kernel functions plugins and invocation

Contract vocabulary: `Kernel`, `FunctionDescriptor`, `InvocationContext`.

Inventory C# Semantic Kernel functionality separately from Java/Python trees. Define plugin discovery metadata arguments and result types. Specify filters cancellation and exception boundaries.

Required observable invariant: Plugin names/signatures validate before use; C# coverage is not inferred from existing Java implementation; invocation errors retain function context.

### WP-02: AI connectors chat streaming and embeddings

Contract vocabulary: `ChatService`, `EmbeddingService`, `StreamingContent`.

Define provider-independent content/tool-call/usage contracts. Implement provider protocol adapters with versioned capabilities. Bound streaming buffers and propagate cancellation.

Required observable invariant: Partial streams retain terminal failure information; malformed tool arguments fail validation; unavailable provider features are explicit.

### WP-03: Prompt templates planning and tool execution

Contract vocabulary: `PromptTemplate`, `ToolPolicy`, `PlanStep`.

Define template variables escaping and renderer ownership. Separate model suggestions from authorized tool execution. Bound recursive tool calls retries cost and deadlines.

Required observable invariant: Model output cannot grant new tool permissions; prompt rendering preserves declared encoding; loops terminate at configured budgets.

### WP-04: Memory vector data agents and process families

Contract vocabulary: `MemoryRecord`, `VectorAdapter`, `AgentState`, `ProcessState`.

Inventory vector/memory agent/process features at the pinned revision. Map storage/provider dependencies independently. Specify state persistence isolation and recovery.

Required observable invariant: Tenant data cannot cross query context; process retries expose possible duplicate side effects; successor-only features are not attributed to the inspected repo.

### WP-05: Lifecycle successor boundary and evaluation

Contract vocabulary: `SemanticProfile`, `EvaluationCase`, `MigrationMap`.

Record agent-framework successor notice without replacing target. Port C# behavior tests with deterministic fake providers. Run separately labeled live-provider compatibility checks.

Required observable invariant: Offline tests require no paid provider; live checks record model/API versions; no existing Java Semantic Kernel is used as implementation foundation.

## Bootstrap and dependency boundaries

JDK HTTP client, own JSON, reflection and async contracts.

Proposed .j dependencies: json,rest,extensions. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Semantic Kernel usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `Kernel` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Plugin names/signatures validate before use; C# coverage is not inferred from existing Java implementation; invocation errors retain function context. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
