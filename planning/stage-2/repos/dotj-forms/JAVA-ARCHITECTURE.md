# DJ-041 .j Forms: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide Windows Forms-style imperative desktop controls and event-driven applications.

Product type: Native desktop framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-forms-01 | Control, Form, EventHandler, ControlCollection | Forms controls and event lifecycle |
| dotj-forms-02 | WindowHandle, Message, NativeControlPeer | Windows message and native adapters |
| dotj-forms-03 | BindingSource, LayoutEngine, DialogResult | Data binding layout and dialogs |
| dotj-forms-04 | DesignSurface, ComponentDescriptor, DesignerDocument | Designer serialization and tooling |
| dotj-forms-05 | ControlCoverage, AccessibilityCase, VisualFixture | Control coverage and Windows acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Java listeners adapt .NET events; native handle recreation, message dispatch and designer serialization need explicit contracts.

## Feature contracts and invariants

### WP-01: Forms controls and event lifecycle

Internal analysis vocabulary (not permission to rename the public API): `Control`, `Form`, `EventHandler`, `ControlCollection`.

Define creation parenting visibility layout and disposal order. Model event subscriptions and handle-recreation behavior. Specify Java event adaptation with stable listener removal.

Required observable invariant: Disposed controls stop dispatching; child ownership is explicit; handle recreation preserves documented state without leaking listeners.

### WP-02: Windows message and native adapters

Internal analysis vocabulary (not permission to rename the public API): `WindowHandle`, `Message`, `NativeControlPeer`.

Inventory Win32 COM GDI and accessibility dependencies. Define message-loop UI-thread and callback ownership. Map each control to native or owned-rendered backend.

Required observable invariant: Message ordering has fixture-backed expectations; native callbacks cannot outlive owners; non-Windows support is not inferred.

### WP-03: Data binding layout and dialogs

Internal analysis vocabulary (not permission to rename the public API): `BindingSource`, `LayoutEngine`, `DialogResult`.

Specify binding currency change notifications and formatting. Implement anchoring docking autosizing and scaling contracts. Map common dialogs clipboard drag/drop and printing separately.

Required observable invariant: Binding updates avoid feedback loops; DPI changes relayout correctly; modal ownership and cancellation release native resources.

### WP-04: Designer serialization and tooling

Internal analysis vocabulary (not permission to rename the public API): `DesignSurface`, `ComponentDescriptor`, `DesignerDocument`.

Investigate design-time services source serialization and resource files. Generate editable Java initialization code. Keep designer plugins isolated from runtime artifacts.

Required observable invariant: Generated forms compile; designer round trips preserve user-owned regions; missing design-time capabilities are reported explicitly.

### WP-05: Control coverage and Windows acceptance

Internal analysis vocabulary (not permission to rename the public API): `ControlCoverage`, `AccessibilityCase`, `VisualFixture`.

Inventory every public control/component family. Run keyboard screen-reader focus and high-DPI scenarios. Test lifecycle stress and resource counters.

Required observable invariant: A control is supported only with behavior and accessibility evidence; native handle counts return to baseline; visual baselines identify OS/theme.

## Bootstrap and dependency boundaries

FFM/JNI to Win32 common controls, COM where necessary; JDK host process.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Windows Forms usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `Control` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Disposed controls stop dispatching; child ownership is explicit; handle recreation preserves documented state without leaking listeners. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
