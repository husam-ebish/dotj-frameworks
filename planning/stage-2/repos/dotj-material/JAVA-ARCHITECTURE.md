# DJ-046 .j Material: Java architecture and contracts

Provide Material-style .j web components with forms, tables, overlays and themes.

Product type: Browser component library. Proposed Java package root: `org.dotj.material`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-material-01 | MaterialComponent, ComponentParameter, RenderState | MudBlazor component contracts and lifecycle |
| dotj-material-02 | FormContext, InputState, ValidationBinding | Forms inputs and validation |
| dotj-material-03 | GridState, FilterDefinition, SortDefinition, ItemKey | Tables grids and virtualization |
| dotj-material-04 | DialogHost, Overlay, Snackbar, NavigationState | Dialogs overlays navigation and feedback |
| dotj-material-05 | MaterialTheme, IconManifest, BrowserInterop | Themes icons CSS and browser bridge |
| dotj-material-06 | ComponentCoverage, AriaCase, VisualFixture | Accessibility examples and qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Blazor components depend on renderer/event lifecycle; visual similarity is not component behavioral parity. No browser JVM assumption.

## Feature contracts and invariants

### WP-01: MudBlazor component contracts and lifecycle

Contract vocabulary: `MaterialComponent`, `ComponentParameter`, `RenderState`.

Inventory MudBlazor component families and state transitions. Adapt Razor parameters events and disposal to dotj-web runtime. Define rerender and server reconnect behavior.

Required observable invariant: Parameter changes produce deterministic output; disposal releases subscriptions; MudBlazor ownership is not confused with desktop MaterialDesignInXaml.

### WP-02: Forms inputs and validation

Contract vocabulary: `FormContext`, `InputState`, `ValidationBinding`.

Specify parsing formatting touched/dirty and focus states. Compose synchronous/asynchronous validation with dotj-validation. Cancel stale validation and preserve IME composition.

Required observable invariant: Late validation cannot overwrite newer input; error text is associated with its field; culture-dependent values have explicit parsing rules.

### WP-03: Tables grids and virtualization

Contract vocabulary: `GridState`, `FilterDefinition`, `SortDefinition`, `ItemKey`.

Define filtering sorting grouping paging and editing contracts. Separate local data from asynchronous remote providers. Specify virtualization measurement and row identity.

Required observable invariant: Superseded remote loads are cancelled or ignored; editing preserves key identity; virtualized memory is bounded by viewport/cache policy.

### WP-04: Dialogs overlays navigation and feedback

Contract vocabulary: `DialogHost`, `Overlay`, `Snackbar`, `NavigationState`.

Define modal focus ownership result delivery and stacking. Handle escape cancellation nested dialogs and host disposal. Specify navigation menus tooltips and transient announcements.

Required observable invariant: Closing a host resolves pending dialogs; focus returns correctly; notifications remain accessible without stealing keyboard focus.

### WP-05: Themes icons CSS and browser bridge

Contract vocabulary: `MaterialTheme`, `IconManifest`, `BrowserInterop`.

Define palette typography breakpoints RTL and reduced motion. Track icon/font/script licenses and immutable versions. Use a narrow JS interface for browser-only measurements/events.

Required observable invariant: No browser JVM is assumed; theme changes preserve component state; assets carry notices; interop version mismatch fails visibly.

### WP-06: Accessibility examples and qualification

Contract vocabulary: `ComponentCoverage`, `AriaCase`, `VisualFixture`.

Port MudBlazor behavior regressions and sample scenarios. Test keyboard ARIA contrast hydration and reconnect. Maintain per-component coverage and browser matrix.

Required observable invariant: Visual resemblance alone cannot mark a component compatible; every claimed component has interaction evidence; complex widgets remain visible if gated.

## Bootstrap and dependency boundaries

dotj-web component runtime, CSS and minimal owned browser scripts.

Proposed .j dependencies: web,validation. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MudBlazor usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `MaterialComponent` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Parameter changes produce deterministic output; disposal releases subscriptions; MudBlazor ownership is not confused with desktop MaterialDesignInXaml. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
