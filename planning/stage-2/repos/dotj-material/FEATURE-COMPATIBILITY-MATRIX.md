# DJ-046 .j Material: feature compatibility matrix

Blazor components depend on renderer/event lifecycle; visual similarity is not component behavioral parity. No browser JVM assumption.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | MudBlazor component contracts and lifecycle | Proposed Java contracts: MaterialComponent, ComponentParameter, RenderState | Parameter changes produce deterministic output; disposal releases subscriptions; MudBlazor ownership is not confused with desktop MaterialDesignInXaml | Planned; evidence gates open |
| WP-02 | Forms inputs and validation | Proposed Java contracts: FormContext, InputState, ValidationBinding | Late validation cannot overwrite newer input; error text is associated with its field; culture-dependent values have explicit parsing rules | Planned; evidence gates open |
| WP-03 | Tables grids and virtualization | Proposed Java contracts: GridState, FilterDefinition, SortDefinition, ItemKey | Superseded remote loads are cancelled or ignored; editing preserves key identity; virtualized memory is bounded by viewport/cache policy | Planned; evidence gates open |
| WP-04 | Dialogs overlays navigation and feedback | Proposed Java contracts: DialogHost, Overlay, Snackbar, NavigationState | Closing a host resolves pending dialogs; focus returns correctly; notifications remain accessible without stealing keyboard focus | Planned; evidence gates open |
| WP-05 | Themes icons CSS and browser bridge | Proposed Java contracts: MaterialTheme, IconManifest, BrowserInterop | No browser JVM is assumed; theme changes preserve component state; assets carry notices; interop version mismatch fails visibly | Planned; evidence gates open |
| WP-06 | Accessibility examples and qualification | Proposed Java contracts: ComponentCoverage, AriaCase, VisualFixture | Visual resemblance alone cannot mark a component compatible; every claimed component has interaction evidence; complex widgets remain visible if gated | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Block component implementation scheduling until Razor/web component contracts and browser bridge are defined. Assets/icons require separate license tracking.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
