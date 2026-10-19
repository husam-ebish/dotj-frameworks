# DJ-040 .j Presentation: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Recreate WPF-style retained UI, XAML, binding and document capabilities on a Java host.

Product type: Native desktop framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-presentation-01 | DependencyProperty, DependencyObject, XamlNode | XAML object model and property system |
| dotj-presentation-02 | Visual, MeasureResult, ArrangeRect, BindingExpression | Layout controls and binding |
| dotj-presentation-03 | DrawingContext, TextRun, InputEvent, RoutedEvent | Rendering text and input |
| dotj-presentation-04 | WindowPeer, Dispatcher, NativeResource | Windows native integration and deployment |
| dotj-presentation-05 | DocumentPaginator, MediaCapability, PresentationProfile | Documents media and compatibility qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Dispatcher affinity, dependency-property precedence, templates and layout need owned behavior. WPF assembly/XAML compatibility is not automatic.

## Feature contracts and invariants

### WP-01: XAML object model and property system

Internal analysis vocabulary (not permission to rename the public API): `DependencyProperty`, `DependencyObject`, `XamlNode`.

Define metadata defaults inheritance coercion and change notifications. Parse namescopes resources bindings and markup extensions. Separate CLR-specific activation from Java type resolution.

Required observable invariant: Property precedence is fixture-backed; cyclic resources/bindings fail diagnostically; arbitrary XAML type activation is constrained.

### WP-02: Layout controls and binding

Internal analysis vocabulary (not permission to rename the public API): `Visual`, `MeasureResult`, `ArrangeRect`, `BindingExpression`.

Implement measure/arrange invalidation and logical/visual trees. Specify data templates styles triggers and item virtualization. Map binding conversions validation and collection changes.

Required observable invariant: Layout stabilizes under bounded passes; virtualized items release recycled state; binding failures identify source and target.

### WP-03: Rendering text and input

Internal analysis vocabulary (not permission to rename the public API): `DrawingContext`, `TextRun`, `InputEvent`, `RoutedEvent`.

Inventory DirectWrite/Direct2D/MILCore-related dependencies. Choose a separately gated renderer/backend contract. Define DPI text shaping hit-testing focus and routed input.

Required observable invariant: Pixel evidence identifies backend/font/DPI; input routing is deterministic; Java2D fallback is not labeled WPF rendering parity.

### WP-04: Windows native integration and deployment

Internal analysis vocabulary (not permission to rename the public API): `WindowPeer`, `Dispatcher`, `NativeResource`.

Define Windows windowing accessibility clipboard and drag/drop adapters. Specify UI thread rules native ownership and teardown. Investigate native library redistribution and JVM deployment.

Required observable invariant: Native handles release on close; cross-thread access fails predictably; unsupported OS capabilities have explicit results.

### WP-05: Documents media and compatibility qualification

Internal analysis vocabulary (not permission to rename the public API): `DocumentPaginator`, `MediaCapability`, `PresentationProfile`.

Retain document printing animation media and interop tracks. Port layout/property/input fixtures and create visual reference cases. Qualify platform features individually before advertising support.

Required observable invariant: No omitted subsystem is disguised as complete WPF parity; visual differences are recorded; runtime/native feasibility gates remain visible.

## Bootstrap and dependency boundaries

JDK host/runtime plus optional FFM/JNI Win32/DirectWrite/Direct3D bindings; AWT may bootstrap a window only.

Proposed .j dependencies: core,toolkit. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing WPF usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `DependencyProperty` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Property precedence is fixture-backed; cyclic resources/bindings fail diagnostically; arbitrary XAML type activation is constrained. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
