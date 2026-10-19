# DJ-041 .j Forms: Java architecture and contracts

Provide Windows Forms-style imperative desktop controls and event-driven applications.

Product type: Native desktop framework. Proposed Java package root: `org.dotj.forms`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-forms-01 | Control, Form, EventHandler, ControlCollection | Forms controls and event lifecycle |
| dotj-forms-02 | WindowHandle, Message, NativeControlPeer | Windows message and native adapters |
| dotj-forms-03 | BindingSource, LayoutEngine, DialogResult | Data binding layout and dialogs |
| dotj-forms-04 | DesignSurface, ComponentDescriptor, DesignerDocument | Designer serialization and tooling |
| dotj-forms-05 | ControlCoverage, AccessibilityCase, VisualFixture | Control coverage and Windows acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Java listeners adapt .NET events; native handle recreation, message dispatch and designer serialization need explicit contracts.

## Feature contracts and invariants

### WP-01: Forms controls and event lifecycle

Contract vocabulary: `Control`, `Form`, `EventHandler`, `ControlCollection`.

Define creation parenting visibility layout and disposal order. Model event subscriptions and handle-recreation behavior. Specify Java event adaptation with stable listener removal.

Required observable invariant: Disposed controls stop dispatching; child ownership is explicit; handle recreation preserves documented state without leaking listeners.

### WP-02: Windows message and native adapters

Contract vocabulary: `WindowHandle`, `Message`, `NativeControlPeer`.

Inventory Win32 COM GDI and accessibility dependencies. Define message-loop UI-thread and callback ownership. Map each control to native or owned-rendered backend.

Required observable invariant: Message ordering has fixture-backed expectations; native callbacks cannot outlive owners; non-Windows support is not inferred.

### WP-03: Data binding layout and dialogs

Contract vocabulary: `BindingSource`, `LayoutEngine`, `DialogResult`.

Specify binding currency change notifications and formatting. Implement anchoring docking autosizing and scaling contracts. Map common dialogs clipboard drag/drop and printing separately.

Required observable invariant: Binding updates avoid feedback loops; DPI changes relayout correctly; modal ownership and cancellation release native resources.

### WP-04: Designer serialization and tooling

Contract vocabulary: `DesignSurface`, `ComponentDescriptor`, `DesignerDocument`.

Investigate design-time services source serialization and resource files. Generate editable Java initialization code. Keep designer plugins isolated from runtime artifacts.

Required observable invariant: Generated forms compile; designer round trips preserve user-owned regions; missing design-time capabilities are reported explicitly.

### WP-05: Control coverage and Windows acceptance

Contract vocabulary: `ControlCoverage`, `AccessibilityCase`, `VisualFixture`.

Inventory every public control/component family. Run keyboard screen-reader focus and high-DPI scenarios. Test lifecycle stress and resource counters.

Required observable invariant: A control is supported only with behavior and accessibility evidence; native handle counts return to baseline; visual baselines identify OS/theme.

## Bootstrap and dependency boundaries

FFM/JNI to Win32 common controls, COM where necessary; JDK host process.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Windows Forms usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `Control` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Disposed controls stop dispatching; child ownership is explicit; handle recreation preserves documented state without leaking listeners. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
