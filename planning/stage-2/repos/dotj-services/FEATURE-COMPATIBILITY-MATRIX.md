# DJ-018 .j Services: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Sharing wire codecs with service-client is proposed; server hosting semantics remain independent. Define impersonation and transaction differences.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Dispatch and operation selection | Internal planning vocabulary (verify upstream public identity): DispatchTable, OperationInvoker, ServiceInstance | Ambiguous operations fail at host startup; per-call instances are disposed once; unhandled exceptions do not disclose stack traces by default | Planned; evidence gates open |
| WP-02 | Host and transport bindings | Internal planning vocabulary (verify upstream public identity): ServiceHost, ListenerBinding, RequestChannel | Stopping a host rejects new work and bounds draining; binding limits are enforced before deserialization; client codecs do not depend on server dispatch | Planned; evidence gates open |
| WP-03 | Behaviors middleware and metadata | Internal planning vocabulary (verify upstream public identity): ServiceBehavior, MessageInspector, MetadataExporter | Exported metadata reimports into reference clients; inspector failures have defined cleanup; behavior order is deterministic | Planned; evidence gates open |
| WP-04 | Authentication authorization and transactions | Internal planning vocabulary (verify upstream public identity): CallerIdentity, AuthorizationDecision, TransactionContext | Unauthorized operations never invoke service code; unavailable impersonation fails explicitly; timeouts do not claim a committed transaction was rolled back | Planned; evidence gates open |
| WP-05 | Server interoperability and hosting acceptance | Internal planning vocabulary (verify upstream public identity): ServiceCompatibilityProfile, DotnetClientFixture, LoadScenario | Every supported binding has bidirectional fault/streaming evidence; resource use remains bounded; unsupported WS-* profiles remain enumerated | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Avoid a bidirectional client/server dependency: service-client owns a neutral wire submodule. Distributed transactions and Windows auth remain unproven.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
