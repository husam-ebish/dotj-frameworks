# DJ-045 .j Toolkit: feature compatibility matrix

C# partial types/source generators adapt to generated companions or subclasses; Span/ref-struct semantics cannot be copied directly.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | MVVM observables and commands | Proposed Java contracts: ObservableObject, RelayCommand, AsyncCommand | Notification order is deterministic; concurrent command execution obeys policy; cancelled commands expose cancellation distinctly | Planned; evidence gates open |
| WP-02 | Messenger and weak subscriptions | Proposed Java contracts: Messenger, Recipient, MessageToken | Unsubscribed recipients stop receiving future deliveries; token scopes do not collide; weak subscriptions do not retain recipients indefinitely | Planned; evidence gates open |
| WP-03 | Source generators and analyzers | Proposed Java contracts: MvvmAnnotation, GeneratedMember, ToolkitDiagnostic | Generated sources compile; conflicts point to annotations; generated semantics match handwritten equivalents in fixtures | Planned; evidence gates open |
| WP-04 | Collections memory and high-performance utilities | Proposed Java contracts: CollectionView, BufferOwner, UtilityCapability | Owned buffers have explicit lifetimes; unsupported ref-struct semantics are documented; optimizations preserve reference behavior | Planned; evidence gates open |
| WP-05 | UI adapters and verification | Proposed Java contracts: ToolkitAdapter, NotificationTrace, GeneratorFixture | Core toolkit has no UI runtime dependency; generated code has stable diagnostics; GC tests do not depend on arbitrary sleep timing | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Keep UI framework independence; memory/pooling helpers need explicit ownership instead of unsafe CLR assumptions.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
