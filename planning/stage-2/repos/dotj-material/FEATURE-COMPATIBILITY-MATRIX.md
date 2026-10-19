# DJ-046 .j Material: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Blazor components depend on renderer/event lifecycle; visual similarity is not component behavioral parity. No browser JVM assumption.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | MudBlazor component contracts and lifecycle | Internal planning vocabulary (verify upstream public identity): MaterialComponent, ComponentParameter, RenderState | Parameter changes produce deterministic output; disposal releases subscriptions; MudBlazor ownership is not confused with desktop MaterialDesignInXaml | Planned; evidence gates open |
| WP-02 | Forms inputs and validation | Internal planning vocabulary (verify upstream public identity): FormContext, InputState, ValidationBinding | Late validation cannot overwrite newer input; error text is associated with its field; culture-dependent values have explicit parsing rules | Planned; evidence gates open |
| WP-03 | Tables grids and virtualization | Internal planning vocabulary (verify upstream public identity): GridState, FilterDefinition, SortDefinition, ItemKey | Superseded remote loads are cancelled or ignored; editing preserves key identity; virtualized memory is bounded by viewport/cache policy | Planned; evidence gates open |
| WP-04 | Dialogs overlays navigation and feedback | Internal planning vocabulary (verify upstream public identity): DialogHost, Overlay, Snackbar, NavigationState | Closing a host resolves pending dialogs; focus returns correctly; notifications remain accessible without stealing keyboard focus | Planned; evidence gates open |
| WP-05 | Themes icons CSS and browser bridge | Internal planning vocabulary (verify upstream public identity): MaterialTheme, IconManifest, BrowserInterop | No browser JVM is assumed; theme changes preserve component state; assets carry notices; interop version mismatch fails visibly | Planned; evidence gates open |
| WP-06 | Accessibility examples and qualification | Internal planning vocabulary (verify upstream public identity): ComponentCoverage, AriaCase, VisualFixture | Visual resemblance alone cannot mark a component compatible; every claimed component has interaction evidence; complex widgets remain visible if gated | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Block component implementation scheduling until Razor/web component contracts and browser bridge are defined. Assets/icons require separate license tracking.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
