# DJ-027 .j Resilience: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Cancellation cannot safely stop arbitrary Java work. Separate timeout completion from underlying operation termination; preserve strategy ordering.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Pipeline and execution context | Internal planning vocabulary (verify upstream public identity): ResiliencePipeline, ExecutionContext, Outcome | Concurrent calls do not share attempt counters; context cleanup runs on every outcome; caller cancellation remains distinguishable from timeout | Planned; evidence gates open |
| WP-02 | Retry timeout and fallback | Internal planning vocabulary (verify upstream public identity): RetryDecision, TimeoutBudget, FallbackResult | Deterministic fake time reproduces attempts; retry-after handling is bounded; non-replayable operations require explicit caller policy | Planned; evidence gates open |
| WP-03 | Circuit breaker and concurrency limits | Internal planning vocabulary (verify upstream public identity): CircuitState, ProbeLease, PermitLease | Only allowed probes enter half-open state; cancellation returns permits once; rejected work reports strategy-specific outcomes | Planned; evidence gates open |
| WP-04 | Hedging and result disposal | Internal planning vocabulary (verify upstream public identity): HedgeAttempt, WinnerSelection, ResultDisposer | No hedge occurs for ineligible requests; losing response bodies are closed; simultaneous completions yield one returned result | Planned; evidence gates open |
| WP-05 | Telemetry adapters and deterministic tests | Internal planning vocabulary (verify upstream public identity): StrategyEvent, HttpResilienceAdapter, VirtualClock | Telemetry excludes payload secrets; retry fixtures are reproducible; composition order has explicit examples and acceptance outcomes | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Timeout semantics and state sharing are high-risk contracts. Never default to retries for non-idempotent operations.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
