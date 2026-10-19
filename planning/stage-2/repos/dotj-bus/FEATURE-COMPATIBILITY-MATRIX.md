# DJ-066 .j Bus: feature compatibility matrix

Broker interoperability is transport-specific; at-least-once delivery and transactional outbox do not imply exactly-once effects. Saga state evolution needs contracts.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Message contracts topology and transport SPI | Proposed Java contracts: MessageEnvelope, EndpointAddress, TransportAdapter | Unknown message versions fail explicitly; send and publish have distinct routing; transport claims are scoped to tested adapters | Planned; evidence gates open |
| WP-02 | Consumers pipelines retries and faults | Proposed Java contracts: ConsumeContext, Consumer, Middleware, FaultMessage | Acknowledge occurs at declared durability boundary; repeated failures reach observable quarantine; faults do not recursively create unbounded fault loops | Planned; evidence gates open |
| WP-03 | Sagas state machines and persistence | Proposed Java contracts: SagaId, StateMachine, CorrelationRule, SagaStore | Concurrent events cannot silently overwrite state; unknown correlations are diagnosable; transition history explains duplicate handling | Planned; evidence gates open |
| WP-04 | Outbox inbox scheduling and delivery guarantees | Proposed Java contracts: OutboxRecord, InboxKey, DeliveryAttempt, ScheduledMessage | Lost broker acknowledgment can produce duplicates but not a false exactly-once claim; deduplication window is explicit; recovery replays only committed intents | Planned; evidence gates open |
| WP-05 | Transports orchestration and operational acceptance | Proposed Java contracts: BusHost, EndpointHealth, TransportMatrix, UpgradePlan | Every transport has its own guarantee matrix; host shutdown bounds outstanding work; inspected Apache source terms are not generalized to all product versions | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Version-specific source/license availability and broker client dependencies may block modules. Each transport remains in scope pending an explicit decision.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
