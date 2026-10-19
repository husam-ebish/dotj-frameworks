# DJ-065 .j Mediator: feature compatibility matrix

Preserve handler resolution and pipeline order; generic variance and streaming cancellation need Java-specific contracts.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | License baseline requests and handlers | Proposed Java contracts: MediatorLicenseRecord, Request, Handler, Response | Source reuse waits for rights resolution; missing/multiple handlers fail explicitly; generic request identity survives erasure through tokens | Planned; evidence gates open |
| WP-02 | Pipeline behaviors and exception handling | Proposed Java contracts: PipelineBehavior, RequestContext, ExceptionHandler | Behavior order is deterministic; cleanup runs on failure; exception handling cannot accidentally invoke the request twice | Planned; evidence gates open |
| WP-03 | Notifications publishing and concurrency | Proposed Java contracts: Notification, NotificationHandler, PublishStrategy | Parallel failures are not lost; sequential strategy has stable ordering; scoped handlers are disposed after completion | Planned; evidence gates open |
| WP-04 | Streaming requests and lifecycle | Proposed Java contracts: StreamRequest, StreamHandler, StreamBehavior | Early termination closes owned resources; exceptions preserve stream context; no hidden unbounded buffering is introduced | Planned; evidence gates open |
| WP-05 | Registration adapters and verification | Proposed Java contracts: MediatorRegistry, CoreDiAdapter, MediatorCase | Base mediator works with explicit factories; no event bus is substituted; rights status and compatibility evidence remain separate | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Version-specific licensing and separately packaged contracts must be reviewed; keep DI integration optional to avoid container coupling.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
