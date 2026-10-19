# DJ-043 .j Avalonia: feature compatibility matrix

Preserve layout/style selector and binding behavior; original compiled bindings and renderer internals need Java adaptations.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Property styling and control model | Proposed Java contracts: AvaloniaProperty, StyledElement, ControlTheme | Priority fixtures resolve identically within profile; style removal restores lower values; detached controls release subscriptions | Planned; evidence gates open |
| WP-02 | Layout rendering and text | Proposed Java contracts: Layoutable, SceneNode, RenderBackend, GlyphRun | Renderer feasibility has a concrete native dependency record; text tests pin fonts; layout loops are detected with diagnostics | Planned; evidence gates open |
| WP-03 | Windowing input accessibility and platforms | Proposed Java contracts: TopLevel, PlatformHandle, InputRoot, AutomationPeer | IME composition survives focus transitions; accessibility nodes match controls; handles close once on each tested platform | Planned; evidence gates open |
| WP-04 | XAML compiler designer and tooling | Proposed Java contracts: CompiledMarkup, BindingPath, PreviewSession | Markup diagnostics refer to original lines; previews recover from invalid edits; generated output is reproducible | Planned; evidence gates open |
| WP-05 | Controls interop and qualification | Proposed Java contracts: ControlCatalog, NativeViewHost, VisualRegression | Control coverage is explicit; native interop resources remain owned; MIT root text does not erase third-party obligations | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Skia/HarfBuzz/native window dependencies and optional commercial backends need exact provenance. Backend list must follow inspected release.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
