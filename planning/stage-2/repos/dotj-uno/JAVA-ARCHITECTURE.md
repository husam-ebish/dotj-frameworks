# DJ-044 .j Uno: Java architecture and contracts

Reproduce WinUI-oriented cross-platform application capabilities with explicit platform backends.

Product type: Native/browser UI framework. Proposed Java package root: `org.dotj.uno`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-uno-01 | WinUiTypeModel, DependencyProperty, XamlDocument | WinUI-compatible API and XAML surface |
| dotj-uno-02 | FrameworkElement, Binding, NavigationState | Controls bindings layout and navigation |
| dotj-uno-03 | PlatformView, SkiaSurface, NativeOwnership | Native and Skia backends |
| dotj-uno-04 | BrowserRuntimeProfile, InteropMessage, MobilePackage | Browser WebAssembly and mobile feasibility |
| dotj-uno-05 | ResourceGenerator, HotReloadSession, UnoCompatibilityMatrix | Tooling resource generation and qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

WinUI API compatibility and Java idioms differ; .NET-to-Wasm tooling cannot be carried over as a JVM runtime.

## Feature contracts and invariants

### WP-01: WinUI-compatible API and XAML surface

Contract vocabulary: `WinUiTypeModel`, `DependencyProperty`, `XamlDocument`.

Inventory generated/reference WinUI surface and Uno-specific extensions. Define Java namespace/type adaptations. Track platform-specific API gaps rather than stubbing success.

Required observable invariant: Unsupported APIs fail explicitly; generated inventories retain unresolved members; XAML type identities are stable.

### WP-02: Controls bindings layout and navigation

Contract vocabulary: `FrameworkElement`, `Binding`, `NavigationState`.

Specify dependency properties templates resources and visual states. Implement layout/input contracts shared across backends. Define navigation and state restoration.

Required observable invariant: Bindings preserve precedence; visual-state transitions are testable; restored navigation rejects incompatible state versions.

### WP-03: Native and Skia backends

Contract vocabulary: `PlatformView`, `SkiaSurface`, `NativeOwnership`.

Separate native-control and Skia rendering profiles. Inventory SDK native libraries and text-shaping dependencies. Define lifecycle accessibility and input translation per backend.

Required observable invariant: Backend capabilities are queryable; shared API existence is not proof of platform support; native teardown is verified.

### WP-04: Browser WebAssembly and mobile feasibility

Contract vocabulary: `BrowserRuntimeProfile`, `InteropMessage`, `MobilePackage`.

Investigate Java-to-browser execution/code generation independently. Specify JS/native interop serialization and event boundaries. Prove mobile runtime packaging and app lifecycle on devices.

Required observable invariant: Browser profile has an executable technology choice before implementation commitment; mobile support requires install/launch evidence; no browser JVM assumption.

### WP-05: Tooling resource generation and qualification

Contract vocabulary: `ResourceGenerator`, `HotReloadSession`, `UnoCompatibilityMatrix`.

Map code generators resources hot reload and build tasks. Integrate workloads through SDK contracts. Run per-platform control accessibility and deployment acceptance.

Required observable invariant: Hot reload invalidates stale generated state; resource IDs are stable; platform limitations remain visible in release profiles.

## Bootstrap and dependency boundaries

Native SDKs and owned bindings; browser DOM/JS/Wasm bridge requires a separate execution design.

Proposed .j dependencies: core,toolkit;web(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Uno Platform usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `WinUiTypeModel` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unsupported APIs fail explicitly; generated inventories retain unresolved members; XAML type identities are stable. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
