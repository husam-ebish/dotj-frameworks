# DJ-040 .j Presentation: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Dispatcher affinity, dependency-property precedence, templates and layout need owned behavior. WPF assembly/XAML compatibility is not automatic.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | XAML object model and property system | Internal planning vocabulary (verify upstream public identity): DependencyProperty, DependencyObject, XamlNode | Property precedence is fixture-backed; cyclic resources/bindings fail diagnostically; arbitrary XAML type activation is constrained | Planned; evidence gates open |
| WP-02 | Layout controls and binding | Internal planning vocabulary (verify upstream public identity): Visual, MeasureResult, ArrangeRect, BindingExpression | Layout stabilizes under bounded passes; virtualized items release recycled state; binding failures identify source and target | Planned; evidence gates open |
| WP-03 | Rendering text and input | Internal planning vocabulary (verify upstream public identity): DrawingContext, TextRun, InputEvent, RoutedEvent | Pixel evidence identifies backend/font/DPI; input routing is deterministic; Java2D fallback is not labeled WPF rendering parity | Planned; evidence gates open |
| WP-04 | Windows native integration and deployment | Internal planning vocabulary (verify upstream public identity): WindowPeer, Dispatcher, NativeResource | Native handles release on close; cross-thread access fails predictably; unsupported OS capabilities have explicit results | Planned; evidence gates open |
| WP-05 | Documents media and compatibility qualification | Internal planning vocabulary (verify upstream public identity): DocumentPaginator, MediaCapability, PresentationProfile | No omitted subsystem is disguised as complete WPF parity; visual differences are recorded; runtime/native feasibility gates remain visible | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Windows-first backend is proposed; cross-platform rendering is a distinct extension. Font/rendering dependencies and redistribution require review.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
