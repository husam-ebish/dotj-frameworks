# DJ-017 .j Service Client: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

SOAP interoperability is separate from CLR type serialization or Windows-integrated security. Preserve deprecated feature history as versioned scope.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Contracts metadata and proxy generation | Internal planning vocabulary (verify upstream public identity): ServiceContract, OperationDescription, WsdlModel | Generated clients retain wire names; ambiguous schemas fail with locations; unsupported binding assertions are never silently ignored | Planned; evidence gates open |
| WP-02 | XML SOAP and message codecs | Internal planning vocabulary (verify upstream public identity): SoapEnvelope, MessageEncoder, FaultDetail | External entities are disabled by default; attachments preserve bytes; SOAP faults retain codes and typed details; binary XML remains gated until verified | Planned; evidence gates open |
| WP-03 | Channels bindings and transport state | Internal planning vocabulary (verify upstream public identity): ChannelFactory, ChannelState, BindingProfile | Aborting releases pending calls; a faulted channel cannot be reused silently; transport-specific capabilities are reported before opening | Planned; evidence gates open |
| WP-04 | Security federation and sessions | Internal planning vocabulary (verify upstream public identity): CredentialProfile, SecurityContext, SessionToken | Security policy mismatch fails before application data is sent; replay fixtures fail; Windows identity is not emulated by passing a username header | Planned; evidence gates open |
| WP-05 | Interoperability and shared wire modules | Internal planning vocabulary (verify upstream public identity): WireContract, ReferenceServiceFixture, ClientCompatibilityProfile | Interoperation evidence is binding/version specific; client and server modules have no cycle; missing reference environment blocks claims rather than disappearing from scope | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

WS-* coverage, binary XML, NetTcp and Windows named pipes need individual feasibility decisions; no blanket WCF compatibility.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
