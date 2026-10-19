# DJ-047 .j Components: Java architecture and contracts

Provide Radzen-style application UI components, data displays and interaction tooling.

Product type: Browser component library. Proposed Java package root: `org.dotj.components`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-components-01 | ComponentDescriptor, Parameter, RenderState | Component API and rendering |
| dotj-components-02 | InputState, EditContext, ValidationMessage | Forms input and validation |
| dotj-components-03 | GridState, SortDescriptor, SelectionModel | Tables grids and data interaction |
| dotj-components-04 | Theme, DialogResult, NavigationItem, AssetManifest | Themes dialogs navigation and assets |
| dotj-components-05 | BrowserAdapter, AccessibilityCase, ComponentMatrix | Browser interop accessibility and coverage |
| dotj-components-06 | ChartSeries, SchedulerView, UploadSession, ComponentScope | Charts scheduler upload and designer boundary |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve event/data-binding behavior and pagination/filtering contracts; chart/scheduler UI must not take over domain scheduling ownership.

## Feature contracts and invariants

### WP-01: Component API and rendering

Contract vocabulary: `ComponentDescriptor`, `Parameter`, `RenderState`.

Inventory Radzen open-source component families and parameters. Bind component output to dotj-web/Razor contracts. Define parameter updates event callbacks and disposal.

Required observable invariant: Parameter changes produce deterministic render changes; disposed components release handlers; unsupported component APIs remain inventoried.

### WP-02: Forms input and validation

Contract vocabulary: `InputState`, `EditContext`, `ValidationMessage`.

Specify value parsing formatting focus and touched/dirty states. Integrate optional validation adapters. Handle asynchronous validation races and debounce.

Required observable invariant: Stale validation results cannot overwrite newer input state; errors remain associated with fields; keyboard input and IME behavior are tested.

### WP-03: Tables grids and data interaction

Contract vocabulary: `GridState`, `SortDescriptor`, `SelectionModel`.

Define local/remote sorting filtering grouping and pagination. Specify virtualization item identity and selection persistence. Bound remote requests and cancel superseded loads.

Required observable invariant: Out-of-order responses cannot replace newer data; selections follow declared identity rules; large lists render bounded visible state.

### WP-04: Themes dialogs navigation and assets

Contract vocabulary: `Theme`, `DialogResult`, `NavigationItem`, `AssetManifest`.

Define styling tokens responsive layout and directionality. Manage overlays focus traps and navigation events. Track icons fonts CSS and JavaScript asset provenance.

Required observable invariant: Dialog close restores focus; RTL fixtures remain usable; asset versions/licenses are explicit; no unreviewed frontend framework is silently adopted.

### WP-05: Browser interop accessibility and coverage

Contract vocabulary: `BrowserAdapter`, `AccessibilityCase`, `ComponentMatrix`.

Specify required JS functions through a narrow versioned contract. Test hydration reconnect keyboard screen readers and reduced motion. Map every component to implemented deferred or feasibility-gated status.

Required observable invariant: Server-only operation is distinguished from required browser behavior; hydration retains state; claimed components have interaction and accessibility evidence.

### WP-06: Charts scheduler upload and designer boundary

Contract vocabulary: `ChartSeries`, `SchedulerView`, `UploadSession`, `ComponentScope`.

Specify SVG/canvas charts accessible alternatives and interaction. Keep scheduler UI distinct from durable job scheduling. Define upload cancellation limits and open-component versus proprietary designer scope.

Required observable invariant: Cancelled uploads release resources; timezone changes preserve event identity rules; proprietary designer functionality is not claimed from the open repository.

## Bootstrap and dependency boundaries

Owned component runtime, SVG/canvas/DOM and CSS.

Proposed .j dependencies: web. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Radzen Blazor usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ComponentDescriptor` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Parameter changes produce deterministic render changes; disposed components release handlers; unsupported component APIs remain inventoried. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
