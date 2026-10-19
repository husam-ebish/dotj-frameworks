# DJ-045 .j Toolkit: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

C# partial types/source generators adapt to generated companions or subclasses; Span/ref-struct semantics cannot be copied directly.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | MVVM observables and commands | Internal planning vocabulary (verify upstream public identity): ObservableObject, RelayCommand, AsyncCommand | Notification order is deterministic; concurrent command execution obeys policy; cancelled commands expose cancellation distinctly | Planned; evidence gates open |
| WP-02 | Messenger and weak subscriptions | Internal planning vocabulary (verify upstream public identity): Messenger, Recipient, MessageToken | Unsubscribed recipients stop receiving future deliveries; token scopes do not collide; weak subscriptions do not retain recipients indefinitely | Planned; evidence gates open |
| WP-03 | Source generators and analyzers | Internal planning vocabulary (verify upstream public identity): MvvmAnnotation, GeneratedMember, ToolkitDiagnostic | Generated sources compile; conflicts point to annotations; generated semantics match handwritten equivalents in fixtures | Planned; evidence gates open |
| WP-04 | Collections memory and high-performance utilities | Internal planning vocabulary (verify upstream public identity): CollectionView, BufferOwner, UtilityCapability | Owned buffers have explicit lifetimes; unsupported ref-struct semantics are documented; optimizations preserve reference behavior | Planned; evidence gates open |
| WP-05 | UI adapters and verification | Internal planning vocabulary (verify upstream public identity): ToolkitAdapter, NotificationTrace, GeneratorFixture | Core toolkit has no UI runtime dependency; generated code has stable diagnostics; GC tests do not depend on arbitrary sleep timing | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Keep UI framework independence; memory/pooling helpers need explicit ownership instead of unsafe CLR assumptions.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
