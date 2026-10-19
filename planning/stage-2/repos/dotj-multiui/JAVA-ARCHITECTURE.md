# DJ-042 .j MultiUI: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide shared UI/application abstractions with platform-specific handlers.

Product type: Mobile/native UI framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-multiui-01 | Application, Page, Handler, PropertyMapper | Application model and handler contracts |
| dotj-multiui-02 | XamlCompiler, BindableProperty, ResourceDictionary | Shared XAML binding and controls |
| dotj-multiui-03 | AndroidPeer, ActivityState, PermissionRequest | Android backend and device services |
| dotj-multiui-04 | PlatformBackend, NativeBridge, DeploymentProfile | Apple and desktop feasibility |
| dotj-multiui-05 | WorkloadManifest, AppPackage, PlatformTestMatrix | Workloads build and cross-platform qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Android ART is not a Java 25 desktop JVM; iOS has no standard supported JVM deployment assumption. Shared syntax does not guarantee portable execution.

## Feature contracts and invariants

### WP-01: Application model and handler contracts

Internal analysis vocabulary (not permission to rename the public API): `Application`, `Page`, `Handler`, `PropertyMapper`.

Map MAUI controls layouts navigation and lifecycle. Define virtual-view to native-handler ownership. Specify platform overrides and handler replacement.

Required observable invariant: Handlers attach/detach once; navigation state survives documented lifecycle transitions; platform overrides do not mutate shared global maps.

### WP-02: Shared XAML binding and controls

Internal analysis vocabulary (not permission to rename the public API): `XamlCompiler`, `BindableProperty`, `ResourceDictionary`.

Define supported XAML grammar and generated bindings. Map styles templates resources and layout measurement. Separate shared semantics from platform widget behavior.

Required observable invariant: Compiled and runtime XAML agree on fixtures; missing resources have source diagnostics; layout differences are recorded per backend.

### WP-03: Android backend and device services

Internal analysis vocabulary (not permission to rename the public API): `AndroidPeer`, `ActivityState`, `PermissionRequest`.

Map JNI Android SDK and packaging prerequisites. Handle activity recreation permissions and configuration changes. Define camera storage sensors networking and main-thread adapters.

Required observable invariant: Denied permissions produce explicit results; rotation does not leak peers; device APIs are tested on declared API levels.

### WP-04: Apple and desktop feasibility

Internal analysis vocabulary (not permission to rename the public API): `PlatformBackend`, `NativeBridge`, `DeploymentProfile`.

Investigate iOS AOT/runtime restrictions and Apple SDK toolchain. Specify Windows/macOS native bindings and signing inputs. Prove minimal render input lifecycle and packaging per target.

Required observable invariant: No mobile platform is claimed before executable proof; native dependencies/licenses are enumerated; signing credentials remain external.

### WP-05: Workloads build and cross-platform qualification

Internal analysis vocabulary (not permission to rename the public API): `WorkloadManifest`, `AppPackage`, `PlatformTestMatrix`.

Connect SDK workloads only after backend feasibility. Define asset localization linker and resource packaging. Run control accessibility navigation and lifecycle matrices.

Required observable invariant: Each supported target has install/launch evidence; unsupported APIs fail explicitly; shared tests do not replace device-specific validation.

## Bootstrap and dependency boundaries

Android SDK/toolchain; Apple SDK/Xcode and Objective-C/Swift bridge or AOT research; Windows native bindings.

Proposed .j dependencies: core,toolkit;presentation(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET MAUI usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `Application` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Handlers attach/detach once; navigation state survives documented lifecycle transitions; platform overrides do not mutate shared global maps. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
