# DJ-049 .j Log: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide configurable rule-driven logging, layouts and target pipelines.

Product type: JVM logging library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-log-01 | LogEvent, Logger, LoggingRule, Level | Log event and routing rules |
| dotj-log-02 | Layout, LayoutRenderer, LayoutContext | Layouts and renderers |
| dotj-log-03 | Target, Wrapper, FlushResult | Targets wrappers and async delivery |
| dotj-log-04 | LogConfiguration, Variable, ExtensionDescriptor | Configuration variables and extensions |
| dotj-log-05 | CoreLoggingAdapter, LayoutFixture, TargetFailure | Adapters and operational acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve rule ordering, layout context and reload atomicity; Java call-site discovery needs measured overhead.

## Feature contracts and invariants

### WP-01: Log event and routing rules

Internal analysis vocabulary (not permission to rename the public API): `LogEvent`, `Logger`, `LoggingRule`, `Level`.

Define logger-name matching levels final rules and routing order. Snapshot event context before asynchronous delivery. Specify reconfiguration publication and fallback behavior.

Required observable invariant: An event follows one configuration revision; final rules stop routing as declared; caller context does not mutate after enqueue.

### WP-02: Layouts and renderers

Internal analysis vocabulary (not permission to rename the public API): `Layout`, `LayoutRenderer`, `LayoutContext`.

Parse nested layout expressions and option syntax. Implement date exception context and environment renderers. Bound recursive rendering and redact configured sensitive data.

Required observable invariant: Malformed layouts fail with locations; recursive renderers terminate; timezone/culture rendering is explicit.

### WP-03: Targets wrappers and async delivery

Internal analysis vocabulary (not permission to rename the public API): `Target`, `Wrapper`, `FlushResult`.

Inventory file console network database and archive targets. Define buffering retry/fallback wrapper order. Handle file rotation concurrent writes and shutdown.

Required observable invariant: Rotation preserves record boundaries; flush reports failures; bounded queues expose drops; target failure avoids recursive logging loops.

### WP-04: Configuration variables and extensions

Internal analysis vocabulary (not permission to rename the public API): `LogConfiguration`, `Variable`, `ExtensionDescriptor`.

Load XML/programmatic configuration securely. Resolve variables and target references before publication. Isolate optional extension assemblies as Java service modules.

Required observable invariant: Invalid reload leaves previous configuration active; external XML entities are disabled; missing extensions produce clear diagnostics.

### WP-05: Adapters and operational acceptance

Internal analysis vocabulary (not permission to rename the public API): `CoreLoggingAdapter`, `LayoutFixture`, `TargetFailure`.

Keep core logger bridge optional. Port routing/layout/target regressions by selected capability. Exercise disk-full permissions reconnect and concurrent reload.

Required observable invariant: Failure modes are observable without crashing unrelated application paths; adapter preserves severity/context; target coverage is explicit.

## Bootstrap and dependency boundaries

JDK XML, filesystem, queues and optional network I/O.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NLog usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `LogEvent` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: An event follows one configuration revision; final rules stop routing as declared; caller context does not mutate after enqueue. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
