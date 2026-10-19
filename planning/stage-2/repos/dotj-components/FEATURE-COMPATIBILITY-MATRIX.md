# DJ-047 .j Components: feature compatibility matrix

Preserve event/data-binding behavior and pagination/filtering contracts; chart/scheduler UI must not take over domain scheduling ownership.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Component API and rendering | Proposed Java contracts: ComponentDescriptor, Parameter, RenderState | Parameter changes produce deterministic render changes; disposed components release handlers; unsupported component APIs remain inventoried | Planned; evidence gates open |
| WP-02 | Forms input and validation | Proposed Java contracts: InputState, EditContext, ValidationMessage | Stale validation results cannot overwrite newer input state; errors remain associated with fields; keyboard input and IME behavior are tested | Planned; evidence gates open |
| WP-03 | Tables grids and data interaction | Proposed Java contracts: GridState, SortDescriptor, SelectionModel | Out-of-order responses cannot replace newer data; selections follow declared identity rules; large lists render bounded visible state | Planned; evidence gates open |
| WP-04 | Themes dialogs navigation and assets | Proposed Java contracts: Theme, DialogResult, NavigationItem, AssetManifest | Dialog close restores focus; RTL fixtures remain usable; asset versions/licenses are explicit; no unreviewed frontend framework is silently adopted | Planned; evidence gates open |
| WP-05 | Browser interop accessibility and coverage | Proposed Java contracts: BrowserAdapter, AccessibilityCase, ComponentMatrix | Server-only operation is distinguished from required browser behavior; hydration retains state; claimed components have interaction and accessibility evidence | Planned; evidence gates open |
| WP-06 | Charts scheduler upload and designer boundary | Proposed Java contracts: ChartSeries, SchedulerView, UploadSession, ComponentScope | Cancelled uploads release resources; timezone changes preserve event identity rules; proprietary designer functionality is not claimed from the open repository | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Separate open component repo from proprietary designer products. Browser helpers and assets require provenance.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
