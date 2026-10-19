# DJ-049 .j Log: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve rule ordering, layout context and reload atomicity; Java call-site discovery needs measured overhead.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Log event and routing rules | Internal planning vocabulary (verify upstream public identity): LogEvent, Logger, LoggingRule, Level | An event follows one configuration revision; final rules stop routing as declared; caller context does not mutate after enqueue | Planned; evidence gates open |
| WP-02 | Layouts and renderers | Internal planning vocabulary (verify upstream public identity): Layout, LayoutRenderer, LayoutContext | Malformed layouts fail with locations; recursive renderers terminate; timezone/culture rendering is explicit | Planned; evidence gates open |
| WP-03 | Targets wrappers and async delivery | Internal planning vocabulary (verify upstream public identity): Target, Wrapper, FlushResult | Rotation preserves record boundaries; flush reports failures; bounded queues expose drops; target failure avoids recursive logging loops | Planned; evidence gates open |
| WP-04 | Configuration variables and extensions | Internal planning vocabulary (verify upstream public identity): LogConfiguration, Variable, ExtensionDescriptor | Invalid reload leaves previous configuration active; external XML entities are disabled; missing extensions produce clear diagnostics | Planned; evidence gates open |
| WP-05 | Adapters and operational acceptance | Internal planning vocabulary (verify upstream public identity): CoreLoggingAdapter, LayoutFixture, TargetFailure | Failure modes are observable without crashing unrelated application paths; adapter preserves severity/context; target coverage is explicit | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Target packages outside main repo and platform event-log APIs need separate source/dependency records.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
