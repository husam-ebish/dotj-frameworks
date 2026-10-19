# DJ-049 .j Log: feature compatibility matrix

Preserve rule ordering, layout context and reload atomicity; Java call-site discovery needs measured overhead.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Log event and routing rules | Proposed Java contracts: LogEvent, Logger, LoggingRule, Level | An event follows one configuration revision; final rules stop routing as declared; caller context does not mutate after enqueue | Planned; evidence gates open |
| WP-02 | Layouts and renderers | Proposed Java contracts: Layout, LayoutRenderer, LayoutContext | Malformed layouts fail with locations; recursive renderers terminate; timezone/culture rendering is explicit | Planned; evidence gates open |
| WP-03 | Targets wrappers and async delivery | Proposed Java contracts: Target, Wrapper, FlushResult | Rotation preserves record boundaries; flush reports failures; bounded queues expose drops; target failure avoids recursive logging loops | Planned; evidence gates open |
| WP-04 | Configuration variables and extensions | Proposed Java contracts: LogConfiguration, Variable, ExtensionDescriptor | Invalid reload leaves previous configuration active; external XML entities are disabled; missing extensions produce clear diagnostics | Planned; evidence gates open |
| WP-05 | Adapters and operational acceptance | Proposed Java contracts: CoreLoggingAdapter, LayoutFixture, TargetFailure | Failure modes are observable without crashing unrelated application paths; adapter preserves severity/context; target coverage is explicit | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Target packages outside main repo and platform event-log APIs need separate source/dependency records.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
