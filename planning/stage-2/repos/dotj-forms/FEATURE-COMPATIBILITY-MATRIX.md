# DJ-041 .j Forms: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Java listeners adapt .NET events; native handle recreation, message dispatch and designer serialization need explicit contracts.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Forms controls and event lifecycle | Internal planning vocabulary (verify upstream public identity): Control, Form, EventHandler, ControlCollection | Disposed controls stop dispatching; child ownership is explicit; handle recreation preserves documented state without leaking listeners | Planned; evidence gates open |
| WP-02 | Windows message and native adapters | Internal planning vocabulary (verify upstream public identity): WindowHandle, Message, NativeControlPeer | Message ordering has fixture-backed expectations; native callbacks cannot outlive owners; non-Windows support is not inferred | Planned; evidence gates open |
| WP-03 | Data binding layout and dialogs | Internal planning vocabulary (verify upstream public identity): BindingSource, LayoutEngine, DialogResult | Binding updates avoid feedback loops; DPI changes relayout correctly; modal ownership and cancellation release native resources | Planned; evidence gates open |
| WP-04 | Designer serialization and tooling | Internal planning vocabulary (verify upstream public identity): DesignSurface, ComponentDescriptor, DesignerDocument | Generated forms compile; designer round trips preserve user-owned regions; missing design-time capabilities are reported explicitly | Planned; evidence gates open |
| WP-05 | Control coverage and Windows acceptance | Internal planning vocabulary (verify upstream public identity): ControlCoverage, AccessibilityCase, VisualFixture | A control is supported only with behavior and accessibility evidence; native handle counts return to baseline; visual baselines identify OS/theme | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Swing controls are not a parity substitute. COM/ActiveX and design-time integration require Windows-only feasibility tracks.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
