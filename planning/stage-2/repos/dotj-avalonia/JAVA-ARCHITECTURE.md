# DJ-043 .j Avalonia: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Build retained-mode cross-platform UI with styling, binding and owned controls.

Product type: Cross-platform native UI framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-avalonia-01 | AvaloniaProperty, StyledElement, ControlTheme | Property styling and control model |
| dotj-avalonia-02 | Layoutable, SceneNode, RenderBackend, GlyphRun | Layout rendering and text |
| dotj-avalonia-03 | TopLevel, PlatformHandle, InputRoot, AutomationPeer | Windowing input accessibility and platforms |
| dotj-avalonia-04 | CompiledMarkup, BindingPath, PreviewSession | XAML compiler designer and tooling |
| dotj-avalonia-05 | ControlCatalog, NativeViewHost, VisualRegression | Controls interop and qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve layout/style selector and binding behavior; original compiled bindings and renderer internals need Java adaptations.

## Feature contracts and invariants

### WP-01: Property styling and control model

Internal analysis vocabulary (not permission to rename the public API): `AvaloniaProperty`, `StyledElement`, `ControlTheme`.

Define property priorities inheritance and binding semantics. Implement selectors styles resources templates and control lifetimes. Preserve control-specific state transitions.

Required observable invariant: Priority fixtures resolve identically within profile; style removal restores lower values; detached controls release subscriptions.

### WP-02: Layout rendering and text

Internal analysis vocabulary (not permission to rename the public API): `Layoutable`, `SceneNode`, `RenderBackend`, `GlyphRun`.

Specify measure/arrange invalidation and scene updates. Inventory Skia text-shaping and graphics dependencies. Define backend capabilities color spaces clipping and DPI.

Required observable invariant: Renderer feasibility has a concrete native dependency record; text tests pin fonts; layout loops are detected with diagnostics.

### WP-03: Windowing input accessibility and platforms

Internal analysis vocabulary (not permission to rename the public API): `TopLevel`, `PlatformHandle`, `InputRoot`, `AutomationPeer`.

Map Windows Linux macOS mobile/browser adapters separately. Define focus capture IME clipboard and accessibility trees. Track thread affinity and native handle lifetimes.

Required observable invariant: IME composition survives focus transitions; accessibility nodes match controls; handles close once on each tested platform.

### WP-04: XAML compiler designer and tooling

Internal analysis vocabulary (not permission to rename the public API): `CompiledMarkup`, `BindingPath`, `PreviewSession`.

Compile Java-targeted markup and typed bindings. Preserve source maps and preview reload behavior. Isolate designer execution and crash recovery.

Required observable invariant: Markup diagnostics refer to original lines; previews recover from invalid edits; generated output is reproducible.

### WP-05: Controls interop and qualification

Internal analysis vocabulary (not permission to rename the public API): `ControlCatalog`, `NativeViewHost`, `VisualRegression`.

Inventory controls data templates virtualization animation and interop. Port behavior tests and maintain per-backend visual references. Verify root licence and third-party NOTICE obligations.

Required observable invariant: Control coverage is explicit; native interop resources remain owned; MIT root text does not erase third-party obligations.

## Bootstrap and dependency boundaries

JVM plus candidate native rendering/font bindings; no JavaFX substitution.

Proposed .j dependencies: core,toolkit. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Avalonia usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `AvaloniaProperty` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Priority fixtures resolve identically within profile; style removal restores lower values; detached controls release subscriptions. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
