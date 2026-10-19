# DJ-039 .j GraphQL: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide an independent GraphQL.NET-style schema and execution engine.

Product type: JVM GraphQL library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-graphql-01 | DocumentNode, GraphType, Schema | Parser AST and schema types |
| dotj-graphql-02 | ValidationContext, VariableValue, ExecutionPlan | Validation coercion and operation planning |
| dotj-graphql-03 | ExecutionContext, FieldResult, ExecutionError | Execution errors and asynchronous fields |
| dotj-graphql-04 | SubscriptionSource, DataLoader, GraphHttpAdapter | Subscriptions loaders and adapters |
| dotj-graphql-05 | GraphProfile, ValidationCase, ExecutionTrace | Specification and upstream regression suite |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

GraphQL semantics can interoperate while C# resolver delegates adapt to Java. No reuse of graphql-java.

## Feature contracts and invariants

### WP-01: Parser AST and schema types

Internal analysis vocabulary (not permission to rename the public API): `DocumentNode`, `GraphType`, `Schema`.

Implement grammar source locations and document validation. Define scalar enum input/object interface and union contracts. Support schema-first and code-first construction separately.

Required observable invariant: Malformed documents have stable spans; invalid schemas fail before execution; scalar coercion is defined for literals and variables.

### WP-02: Validation coercion and operation planning

Internal analysis vocabulary (not permission to rename the public API): `ValidationContext`, `VariableValue`, `ExecutionPlan`.

Implement operation selection fragment rules and directive handling. Coerce variables/defaults with exact null/absence distinctions. Cache plans by schema and validated document identity.

Required observable invariant: Omitted and explicit-null inputs differ correctly; fragment cycles fail; stale schema plans cannot execute silently.

### WP-03: Execution errors and asynchronous fields

Internal analysis vocabulary (not permission to rename the public API): `ExecutionContext`, `FieldResult`, `ExecutionError`.

Define field scheduling null bubbling and error paths. Propagate cancellation through asynchronous resolvers. Separate resolver exceptions from public error messages.

Required observable invariant: Errors retain field/index paths; non-null violations bubble correctly; internal stack traces are hidden unless explicitly enabled.

### WP-04: Subscriptions loaders and adapters

Internal analysis vocabulary (not permission to rename the public API): `SubscriptionSource`, `DataLoader`, `GraphHttpAdapter`.

Specify subscription lifetime and event execution. Scope batched loaders per operation/user. Keep HTTP and serializer integrations optional.

Required observable invariant: Disconnect closes subscriptions; cache entries cannot leak across requests; core executor needs no web framework.

### WP-05: Specification and upstream regression suite

Internal analysis vocabulary (not permission to rename the public API): `GraphProfile`, `ValidationCase`, `ExecutionTrace`.

Lock specification version and upstream behavior exceptions. Port parser validation execution and bug regressions. Test depth complexity and malicious query limits.

Required observable invariant: Claims identify exact specification/profile; expensive requests are bounded; no graphql-java substitution implements the port.

## Bootstrap and dependency boundaries

Collections, executors, own JSON and optional web transport.

Proposed .j dependencies: core,json;web(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing GraphQL.NET usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `DocumentNode` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Malformed documents have stable spans; invalid schemas fail before execution; scalar coercion is defined for literals and variables. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
