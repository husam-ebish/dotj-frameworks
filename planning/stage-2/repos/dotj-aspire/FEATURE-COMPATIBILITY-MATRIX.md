# DJ-013 .j Aspire: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Translate resource APIs to Java; dashboard and deployment formats require their own contracts. Do not reuse an existing Java Aspire implementation.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Application resource graph | Internal planning vocabulary (verify upstream public identity): ResourceId, ResourceSpec, ReferenceExpression | Invalid graphs fail before launching anything; stable resource IDs survive serialization; secrets are not rendered into public manifests | Planned; evidence gates open |
| WP-02 | Local orchestration and lifecycle | Internal planning vocabulary (verify upstream public identity): ResourceController, HealthState, ProcessHandle, ContainerHandle | A failed dependency blocks dependents with a reason; partial startup cleans owned children; user-owned processes are never terminated | Planned; evidence gates open |
| WP-03 | Service discovery and integration catalog | Internal planning vocabulary (verify upstream public identity): EndpointReference, ConnectionDescriptor, IntegrationDescriptor | Endpoint rebinding reaches consumers; incompatible integrations fail before launch; disabled integrations introduce no runtime dependency | Planned; evidence gates open |
| WP-04 | Dashboard and observability | Internal planning vocabulary (verify upstream public identity): ResourceSnapshot, LogStream, TraceLink, DashboardSession | Disconnected viewers release subscriptions; hostile log text is escaped; resource filters preserve correlation across restarts | Planned; evidence gates open |
| WP-05 | Deployment export and operational parity | Internal planning vocabulary (verify upstream public identity): DeploymentModel, Exporter, DeploymentDiff | Export never silently drops a required dependency; secret references stay external; repeated export is deterministic for locked inputs | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Inspect DCP/orchestration sources and dashboard assets as extra dependencies; cloud connectors need independent license and protocol decisions.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
