# DJ-014 .j Proxy: feature compatibility matrix

Preserve forwarding semantics including headers, trailers, cancellation and WebSockets; a simple HTTP relay does not establish YARP parity.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Route and cluster configuration | Proposed Java contracts: ProxyRoute, ClusterSnapshot, DestinationState | Invalid reload preserves last good snapshot; each request sees one revision; removed backends stop receiving new work | Planned; evidence gates open |
| WP-02 | Streaming forwarding and transforms | Proposed Java contracts: ForwardingContext, HeaderTransform, DuplexTunnel | Request/response bodies are not fully buffered by default; smuggling cases are rejected; tunnel disconnect closes both owned halves | Planned; evidence gates open |
| WP-03 | Balancing affinity and health | Proposed Java contracts: LoadBalancingPolicy, AffinityToken, HealthReport | Unhealthy destinations are excluded as configured; stale affinity cannot cross clusters; health flapping obeys explicit recovery policy | Planned; evidence gates open |
| WP-04 | Retry timeout and security boundaries | Proposed Java contracts: ForwardAttempt, RetryDecision, TimeoutBudget | Non-replayable requests are not silently retried; cancellation stops all attempts; untrusted forwarded headers cannot change authenticated origin | Planned; evidence gates open |
| WP-05 | Protocol and operational acceptance | Proposed Java contracts: ProxyCapabilityMatrix, RouteMetrics, FaultScenario | Each advertised forwarding feature has wire evidence; active drain has a bounded outcome; diagnostic labels do not contain unbounded URLs | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

HTTP/2 multiplexing and protocol upgrades may require transport extensions; distinguish proxy policy from generic resilience policy.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
