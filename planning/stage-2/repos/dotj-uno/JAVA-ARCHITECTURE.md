# DJ-044 .j Uno: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Reproduce WinUI-oriented cross-platform application capabilities with explicit platform backends.

Product type: Native/browser UI framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-uno-01 | WinUiTypeModel, DependencyProperty, XamlDocument | WinUI-compatible API and XAML surface |
| dotj-uno-02 | FrameworkElement, Binding, NavigationState | Controls bindings layout and navigation |
| dotj-uno-03 | PlatformView, SkiaSurface, NativeOwnership | Native and Skia backends |
| dotj-uno-04 | BrowserRuntimeProfile, InteropMessage, MobilePackage | Browser WebAssembly and mobile feasibility |
| dotj-uno-05 | ResourceGenerator, HotReloadSession, UnoCompatibilityMatrix | Tooling resource generation and qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

WinUI API compatibility and Java idioms differ; .NET-to-Wasm tooling cannot be carried over as a JVM runtime.

## Feature contracts and invariants

### WP-01: WinUI-compatible API and XAML surface

Internal analysis vocabulary (not permission to rename the public API): `WinUiTypeModel`, `DependencyProperty`, `XamlDocument`.

Inventory generated/reference WinUI surface and Uno-specific extensions. Define Java namespace/type adaptations. Track platform-specific API gaps rather than stubbing success.

Required observable invariant: Unsupported APIs fail explicitly; generated inventories retain unresolved members; XAML type identities are stable.

### WP-02: Controls bindings layout and navigation

Internal analysis vocabulary (not permission to rename the public API): `FrameworkElement`, `Binding`, `NavigationState`.

Specify dependency properties templates resources and visual states. Implement layout/input contracts shared across backends. Define navigation and state restoration.

Required observable invariant: Bindings preserve precedence; visual-state transitions are testable; restored navigation rejects incompatible state versions.

### WP-03: Native and Skia backends

Internal analysis vocabulary (not permission to rename the public API): `PlatformView`, `SkiaSurface`, `NativeOwnership`.

Separate native-control and Skia rendering profiles. Inventory SDK native libraries and text-shaping dependencies. Define lifecycle accessibility and input translation per backend.

Required observable invariant: Backend capabilities are queryable; shared API existence is not proof of platform support; native teardown is verified.

### WP-04: Browser WebAssembly and mobile feasibility

Internal analysis vocabulary (not permission to rename the public API): `BrowserRuntimeProfile`, `InteropMessage`, `MobilePackage`.

Investigate Java-to-browser execution/code generation independently. Specify JS/native interop serialization and event boundaries. Prove mobile runtime packaging and app lifecycle on devices.

Required observable invariant: Browser profile has an executable technology choice before implementation commitment; mobile support requires install/launch evidence; no browser JVM assumption.

### WP-05: Tooling resource generation and qualification

Internal analysis vocabulary (not permission to rename the public API): `ResourceGenerator`, `HotReloadSession`, `UnoCompatibilityMatrix`.

Map code generators resources hot reload and build tasks. Integrate workloads through SDK contracts. Run per-platform control accessibility and deployment acceptance.

Required observable invariant: Hot reload invalidates stale generated state; resource IDs are stable; platform limitations remain visible in release profiles.

## Bootstrap and dependency boundaries

Native SDKs and owned bindings; browser DOM/JS/Wasm bridge requires a separate execution design.

Proposed .j dependencies: core,toolkit;web(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Uno Platform usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `WinUiTypeModel` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unsupported APIs fail explicitly; generated inventories retain unresolved members; XAML type identities are stable. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
