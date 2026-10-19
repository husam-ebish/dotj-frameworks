# DJ-015 .j Actors: feature compatibility matrix

Grain identity, scheduling and reentrancy require explicit Java semantics. Delivery guarantees are not exactly-once and failures must remain observable.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Identity activation and scheduling | Proposed Java contracts: ActorId, ActivationId, TurnContext, ReentrancyPolicy | Concurrent first calls cannot silently create conflicting authoritative activations; reentrant waits have documented behavior; collected activations release resources | Planned; evidence gates open |
| WP-02 | Membership placement and failure detection | Proposed Java contracts: MemberEpoch, MembershipView, PlacementDecision | A partition scenario has an explicit availability/consistency outcome; stale epochs cannot commit ownership changes; placement is explainable | Planned; evidence gates open |
| WP-03 | Messaging serialization and code generation | Proposed Java contracts: InvocationEnvelope, RequestId, SerializerSchema, ProxyDescriptor | Unknown fields follow schema policy; lost replies never imply exactly-once execution; caller cancellation does not falsely prove remote rollback | Planned; evidence gates open |
| WP-04 | Persistence reminders and streams | Proposed Java contracts: StateVersion, ReminderRecord, StreamSubscription | Conflicting writes are surfaced; reminders survive activation loss according to store guarantees; slow subscribers cannot grow memory without bounds | Planned; evidence gates open |
| WP-05 | Cluster operations and provider adapters | Proposed Java contracts: ClusterManifest, ProviderContract, UpgradeScenario | Unsupported provider guarantees are stated; rolling upgrades preserve declared schemas; no successful test is generalized into exactly-once delivery | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Membership/storage providers and generated serialization may add absent upstream sources; wire compatibility is unproven until pinned protocol analysis.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
