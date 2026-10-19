# DJ-048 .j Structured Log: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve destructuring, scalar rendering and template tokens; log-event context propagation must work across Java executors.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Message templates and property values | Internal planning vocabulary (verify upstream public identity): MessageTemplate, LogEvent, PropertyValue | Template holes bind deterministically; cycles cannot recurse forever; structured values survive independent formatting | Planned; evidence gates open |
| WP-02 | Logger configuration enrichment and filtering | Internal planning vocabulary (verify upstream public identity): LoggerConfig, Enricher, Filter, LevelSwitch | Concurrent scopes do not leak properties; duplicate enrichment precedence is stable; disabled levels avoid unnecessary value construction | Planned; evidence gates open |
| WP-03 | Sinks batching and backpressure | Internal planning vocabulary (verify upstream public identity): Sink, Batch, DeliveryPolicy | Shutdown has a bounded flush result; queue overflow is observable; sink errors do not recurse through the same failing logger | Planned; evidence gates open |
| WP-04 | Formats integrations and configuration | Internal planning vocabulary (verify upstream public identity): EventFormatter, ConfigurationReader, LoggingBridge | Formatting cannot inject extra JSON records; bridge retains template/properties where possible; optional sinks do not load in core logger | Planned; evidence gates open |
| WP-05 | Compatibility and performance corpus | Internal planning vocabulary (verify upstream public identity): TemplateCase, SinkFaultCase, AllocationReport | No caller-owned sink is closed unexpectedly; performance evidence names payloads and settings; Serilog behavior remains distinct from dotj-log | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Many sinks are separate repositories; base scope includes SPI, with integrations explicitly tracked. Never force core to depend on concrete logger.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
