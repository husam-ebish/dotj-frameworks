# DJ-044 .j Uno: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

WinUI API compatibility and Java idioms differ; .NET-to-Wasm tooling cannot be carried over as a JVM runtime.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | WinUI-compatible API and XAML surface | Internal planning vocabulary (verify upstream public identity): WinUiTypeModel, DependencyProperty, XamlDocument | Unsupported APIs fail explicitly; generated inventories retain unresolved members; XAML type identities are stable | Planned; evidence gates open |
| WP-02 | Controls bindings layout and navigation | Internal planning vocabulary (verify upstream public identity): FrameworkElement, Binding, NavigationState | Bindings preserve precedence; visual-state transitions are testable; restored navigation rejects incompatible state versions | Planned; evidence gates open |
| WP-03 | Native and Skia backends | Internal planning vocabulary (verify upstream public identity): PlatformView, SkiaSurface, NativeOwnership | Backend capabilities are queryable; shared API existence is not proof of platform support; native teardown is verified | Planned; evidence gates open |
| WP-04 | Browser WebAssembly and mobile feasibility | Internal planning vocabulary (verify upstream public identity): BrowserRuntimeProfile, InteropMessage, MobilePackage | Browser profile has an executable technology choice before implementation commitment; mobile support requires install/launch evidence; no browser JVM assumption | Planned; evidence gates open |
| WP-05 | Tooling resource generation and qualification | Internal planning vocabulary (verify upstream public identity): ResourceGenerator, HotReloadSession, UnoCompatibilityMatrix | Hot reload invalidates stale generated state; resource IDs are stable; platform limitations remain visible in release profiles | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Browser and iOS execution remain unproven; WinUI reference sources and Skia-related components may add upstream dependencies.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
