# DJ-025 .j Container: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide advanced component registration, lifetime scopes and resolution with an owned container.

Product type: JVM DI library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-container-01 | ServiceKey, Registration, ResolutionContext | Registration model and resolution |
| dotj-container-02 | LifetimeScope, OwnedValue, ReleaseAction | Scopes ownership and disposal |
| dotj-container-03 | RegistrationModule, ComponentScanner, ActivationMiddleware | Modules scanning and activation pipelines |
| dotj-container-04 | LazyService, ServiceFactory, MetadataValue, InterceptorAdapter | Advanced relationships and interception |
| dotj-container-05 | CoreContainerAdapter, ScopeDiagnostic, StressScenario | Core bridge and concurrent acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Translate open generics to type tokens; ownership and scope disposal must be explicit. Dynamic class interception is not JDK interface proxy equivalence.

## Feature contracts and invariants

### WP-01: Registration model and resolution

Internal analysis vocabulary (not permission to rename the public API): `ServiceKey`, `Registration`, `ResolutionContext`.

Define named keyed typed and generic registrations. Specify constructor selection parameter overrides and decorators. Detect dependency cycles with a complete resolution path.

Required observable invariant: Ambiguous constructors fail deterministically; generic constraints are enforced; circular resolution errors identify the cycle.

### WP-02: Scopes ownership and disposal

Internal analysis vocabulary (not permission to rename the public API): `LifetimeScope`, `OwnedValue`, `ReleaseAction`.

Define singleton scoped transient matching-scope and owned lifetimes. Track factory-created versus externally owned instances. Dispose deduplicated owned instances in reverse activation order.

Required observable invariant: Externally supplied objects remain untouched; alias registrations dispose once; failed activation cleans partially constructed owned dependencies.

### WP-03: Modules scanning and activation pipelines

Internal analysis vocabulary (not permission to rename the public API): `RegistrationModule`, `ComponentScanner`, `ActivationMiddleware`.

Define module load order and conditional registration. Scan metadata without eagerly initializing application classes. Provide ordered activation hooks with exception-safe cleanup.

Required observable invariant: Scanning executes no static application initialization; activation hook failures do not leak instances; module precedence is reproducible.

### WP-04: Advanced relationships and interception

Internal analysis vocabulary (not permission to rename the public API): `LazyService`, `ServiceFactory`, `MetadataValue`, `InterceptorAdapter`.

Specify collection lazy factory and metadata relationships. Define dynamic registration sources and caching boundaries. Isolate interception/code-generation prerequisites.

Required observable invariant: Lazy/factory values respect originating scope; metadata does not force instantiation; unsupported final-class interception is explicit.

### WP-05: Core bridge and concurrent acceptance

Internal analysis vocabulary (not permission to rename the public API): `CoreContainerAdapter`, `ScopeDiagnostic`, `StressScenario`.

Adapt core DI contracts without changing Autofac-specific semantics. Test concurrent creation disposal and child-scope races. Publish capability differences from the core default container.

Required observable invariant: Bridge differences are documented; a disposed scope cannot admit new resolutions; optional adapter creates no core-to-container dependency.

## Bootstrap and dependency boundaries

Reflection, MethodHandles, AutoCloseable and ServiceLoader.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Autofac usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ServiceKey` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Ambiguous constructors fail deterministically; generic constraints are enforced; circular resolution errors identify the cycle. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
