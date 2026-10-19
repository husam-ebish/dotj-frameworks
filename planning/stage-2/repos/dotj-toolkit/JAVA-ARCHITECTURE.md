# DJ-045 .j Toolkit: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide MVVM helpers, generated observable models, commands and high-performance utility capabilities.

Product type: JVM utility/code-generation library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-toolkit-01 | ObservableObject, RelayCommand, AsyncCommand | MVVM observables and commands |
| dotj-toolkit-02 | Messenger, Recipient, MessageToken | Messenger and weak subscriptions |
| dotj-toolkit-03 | MvvmAnnotation, GeneratedMember, ToolkitDiagnostic | Source generators and analyzers |
| dotj-toolkit-04 | CollectionView, BufferOwner, UtilityCapability | Collections memory and high-performance utilities |
| dotj-toolkit-05 | ToolkitAdapter, NotificationTrace, GeneratorFixture | UI adapters and verification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# partial types/source generators adapt to generated companions or subclasses; Span/ref-struct semantics cannot be copied directly.

## Feature contracts and invariants

### WP-01: MVVM observables and commands

Internal analysis vocabulary (not permission to rename the public API): `ObservableObject`, `RelayCommand`, `AsyncCommand`.

Define property notifications validation and dependent updates. Specify command reentrancy cancellation and can-execute signals. Avoid event-handler leaks in lifecycle transitions.

Required observable invariant: Notification order is deterministic; concurrent command execution obeys policy; cancelled commands expose cancellation distinctly.

### WP-02: Messenger and weak subscriptions

Internal analysis vocabulary (not permission to rename the public API): `Messenger`, `Recipient`, `MessageToken`.

Define typed/token-scoped routing and registration rules. Implement weak-recipient behavior without premature collection. Specify concurrency reentrancy and unsubscribe during delivery.

Required observable invariant: Unsubscribed recipients stop receiving future deliveries; token scopes do not collide; weak subscriptions do not retain recipients indefinitely.

### WP-03: Source generators and analyzers

Internal analysis vocabulary (not permission to rename the public API): `MvvmAnnotation`, `GeneratedMember`, `ToolkitDiagnostic`.

Translate generator attributes into Java annotations. Generate deterministic accessors commands and diagnostics. Check inherited/private member naming conflicts.

Required observable invariant: Generated sources compile; conflicts point to annotations; generated semantics match handwritten equivalents in fixtures.

### WP-04: Collections memory and high-performance utilities

Internal analysis vocabulary (not permission to rename the public API): `CollectionView`, `BufferOwner`, `UtilityCapability`.

Inventory non-MVVM utility families separately. Map memory/span concepts to safe JDK facilities. Gate unsafe/vector/native accelerations by measurable need.

Required observable invariant: Owned buffers have explicit lifetimes; unsupported ref-struct semantics are documented; optimizations preserve reference behavior.

### WP-05: UI adapters and verification

Internal analysis vocabulary (not permission to rename the public API): `ToolkitAdapter`, `NotificationTrace`, `GeneratorFixture`.

Keep presentation/forms/mobile integrations optional. Port command messenger generator and utility regressions. Test GC-sensitive subscriptions with controlled reachability.

Required observable invariant: Core toolkit has no UI runtime dependency; generated code has stable diagnostics; GC tests do not depend on arbitrary sleep timing.

## Bootstrap and dependency boundaries

Annotation processing, VarHandle, ByteBuffer and CompletionStage.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET Community Toolkit usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ObservableObject` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Notification order is deterministic; concurrent command execution obeys policy; cancelled commands expose cancellation distinctly. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
