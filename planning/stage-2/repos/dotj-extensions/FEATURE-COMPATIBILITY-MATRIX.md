# DJ-006 .j Extensions: feature compatibility matrix

Map every package to runtime or extensions at a pinned revision; options validation, configuration precedence and lifecycle behavior require explicit Java contracts.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Package ownership and adapter graph | Proposed Java contracts: ExtensionModuleDescriptor, CapabilitySPI, IntegrationManifest | Every inspected package has exactly one owner; core contracts never depend on richer adapters; no namespace-based ownership shortcut is accepted | Planned; evidence gates open |
| WP-02 | Resilience HTTP and service discovery | Proposed Java contracts: ServiceEndpointResolver, HttpPipelineDecorator, DiscoverySnapshot | Refresh cannot publish half-built endpoint sets; retries never replay unsafe operations by default; discovery failures follow declared stale-data policy | Planned; evidence gates open |
| WP-03 | Telemetry diagnostics and compliance | Proposed Java contracts: MeterAdapter, Redactor, HealthProbe, ResourceSnapshot | Secrets are redacted before sinks; unbounded user labels are rejected or bounded; missing platform probes yield unknown rather than healthy; redaction never mutates the caller's object | Planned; evidence gates open |
| WP-04 | AI vector and ingestion abstractions | Proposed Java contracts: ChatClient, EmbeddingClient, VectorStore, IngestionStage | Mocked provider streams obey cancellation/backpressure; malformed tool arguments fail validation; ingestion preserves source/provenance; no existing Java AI framework substitutes for these contracts | Planned; evidence gates open |
| WP-05 | Testing helpers and packaging | Proposed Java contracts: FakeTimeProvider, TestHost, ExtensionCompatibilityMatrix | An application using only core APIs loads no AI/native/cloud code; deterministic fake time drives retry/health tests; adapter version conflicts are diagnosed before startup | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Package ownership cannot be inferred from namespace. Freeze a package-to-repository map before implementation and keep newly discovered packages visible.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
