# DJ-029 .j Jobs: feature compatibility matrix

Serialized CLR method calls require Java invocation descriptors and allowlists; at-least-once processing demands application idempotency.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Job representation and state machine | Proposed Java contracts: JobDescriptor, JobState, StateTransition | Unknown method versions fail before invocation; arbitrary type activation is disabled; state history explains each retry | Planned; evidence gates open |
| WP-02 | Persistent storage and atomic claims | Proposed Java contracts: JobStore, WorkerLease, QueueRecord | Two workers cannot hold the same valid claim under store assumptions; crashed workers become reclaimable; guarantees are stated per provider | Planned; evidence gates open |
| WP-03 | Worker execution filters and cancellation | Proposed Java contracts: JobContext, JobFilter, WorkerPool | A side effect followed by crash is recognized as possibly duplicated; filter failures release resources; shutdown leaves recoverable job state | Planned; evidence gates open |
| WP-04 | Recurring jobs continuations and batches | Proposed Java contracts: RecurringDefinition, Continuation, ScheduleOccurrence | DST/restart cases do not silently lose occurrence identity; continuations obey terminal conditions; unlicensed extensions are not copied | Planned; evidence gates open |
| WP-05 | Dashboard and operational acceptance | Proposed Java contracts: JobDashboard, QueueMetrics, RetentionPolicy | Dashboard cannot execute arbitrary methods; retained payloads obey policy; at-least-once limitations are visible in documentation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Inspect exact community/proprietary module boundaries and version license. Do not assume paid extensions are available to port.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
