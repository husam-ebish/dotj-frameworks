# DJ-028 .j Reactive: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Rx push observables and Flow demand are different; use explicit bridge policies. Port disposal and terminal-event semantics rather than substituting Reactor.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Observable and observer protocol | Internal planning vocabulary (verify upstream public identity): Observable, Observer, Subscription | No notification follows a terminal event; disposal is idempotent; synchronous errors follow the declared delivery rule | Planned; evidence gates open |
| WP-02 | Schedulers and virtual time | Internal planning vocabulary (verify upstream public identity): Scheduler, ScheduledAction, VirtualClock | Virtual-time traces are reproducible; cancellation removes pending work; recursive scheduling cannot unexpectedly overflow stack | Planned; evidence gates open |
| WP-03 | Operators and error composition | Internal planning vocabulary (verify upstream public identity): OperatorPlan, ErrorPolicy, WindowState | Merge/concat/switch have distinct traces; delayed errors preserve ordering; unbounded operators are documented with their memory behavior | Planned; evidence gates open |
| WP-04 | Subjects sharing and concurrency | Internal planning vocabulary (verify upstream public identity): Subject, ReplayBuffer, RefCountState | Late subscribers see the documented terminal/replay sequence; refcount disconnects once; concurrent observers cannot corrupt state | Planned; evidence gates open |
| WP-05 | Flow adapters and conformance | Internal planning vocabulary (verify upstream public identity): FlowBridge, DemandPolicy, MarbleCase | Push-only sources never claim native backpressure; adapter demand is honored; every implemented operator has trace-level acceptance | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Operator inventory can be large; AsyncRx and related upstream subprojects must be tracked separately if present.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
