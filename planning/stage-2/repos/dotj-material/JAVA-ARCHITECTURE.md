# DJ-046 .j Material: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide Material-style .j web components with forms, tables, overlays and themes.

Product type: Browser component library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

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

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Blazor components depend on renderer/event lifecycle; visual similarity is not component behavioral parity. No browser JVM assumption.

## Feature contracts and invariants

### WP-01: MudBlazor component contracts and lifecycle

Internal analysis vocabulary (not permission to rename the public API): `MaterialComponent`, `ComponentParameter`, `RenderState`.

Inventory MudBlazor component families and state transitions. Adapt Razor parameters events and disposal to dotj-web runtime. Define rerender and server reconnect behavior.

Required observable invariant: Parameter changes produce deterministic output; disposal releases subscriptions; MudBlazor ownership is not confused with desktop MaterialDesignInXaml.

### WP-02: Forms inputs and validation

Internal analysis vocabulary (not permission to rename the public API): `FormContext`, `InputState`, `ValidationBinding`.

Specify parsing formatting touched/dirty and focus states. Compose synchronous/asynchronous validation with dotj-validation. Cancel stale validation and preserve IME composition.

Required observable invariant: Late validation cannot overwrite newer input; error text is associated with its field; culture-dependent values have explicit parsing rules.

### WP-03: Tables grids and virtualization

Internal analysis vocabulary (not permission to rename the public API): `GridState`, `FilterDefinition`, `SortDefinition`, `ItemKey`.

Define filtering sorting grouping paging and editing contracts. Separate local data from asynchronous remote providers. Specify virtualization measurement and row identity.

Required observable invariant: Superseded remote loads are cancelled or ignored; editing preserves key identity; virtualized memory is bounded by viewport/cache policy.

### WP-04: Dialogs overlays navigation and feedback

Internal analysis vocabulary (not permission to rename the public API): `DialogHost`, `Overlay`, `Snackbar`, `NavigationState`.

Define modal focus ownership result delivery and stacking. Handle escape cancellation nested dialogs and host disposal. Specify navigation menus tooltips and transient announcements.

Required observable invariant: Closing a host resolves pending dialogs; focus returns correctly; notifications remain accessible without stealing keyboard focus.

### WP-05: Themes icons CSS and browser bridge

Internal analysis vocabulary (not permission to rename the public API): `MaterialTheme`, `IconManifest`, `BrowserInterop`.

Define palette typography breakpoints RTL and reduced motion. Track icon/font/script licenses and immutable versions. Use a narrow JS interface for browser-only measurements/events.

Required observable invariant: No browser JVM is assumed; theme changes preserve component state; assets carry notices; interop version mismatch fails visibly.

### WP-06: Accessibility examples and qualification

Internal analysis vocabulary (not permission to rename the public API): `ComponentCoverage`, `AriaCase`, `VisualFixture`.

Port MudBlazor behavior regressions and sample scenarios. Test keyboard ARIA contrast hydration and reconnect. Maintain per-component coverage and browser matrix.

Required observable invariant: Visual resemblance alone cannot mark a component compatible; every claimed component has interaction evidence; complex widgets remain visible if gated.

## Bootstrap and dependency boundaries

dotj-web component runtime, CSS and minimal owned browser scripts.

Proposed .j dependencies: web,validation. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MudBlazor usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `MaterialComponent` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Parameter changes produce deterministic output; disposal releases subscriptions; MudBlazor ownership is not confused with desktop MaterialDesignInXaml. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Public API direction under the owner requirement

Retain original MudBlazor component names, parameters and event names for the declared source profile. Do not rename Mud-prefixed components merely to match .j product branding. Browser/runtime syntax and execution gaps remain explicit.
