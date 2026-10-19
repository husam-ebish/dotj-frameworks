# DJ-022 .j Redis: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve command ordering and result distinctions; reconnect cannot silently replay non-idempotent commands. Redis server license is separate from client source terms.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | RESP parsing and command metadata | Internal planning vocabulary (verify upstream public identity): RespValue, CommandDescriptor, ReplyDecoder | Fragmented frames decode identically; oversized replies fail safely; unknown commands cannot inherit unsafe retry assumptions | Planned; evidence gates open |
| WP-02 | Multiplexed connections and reconnect | Internal planning vocabulary (verify upstream public identity): PendingCommand, ConnectionEpoch, CompletionState | Disconnect cannot associate old replies with a new connection; non-idempotent ambiguous writes are not silently replayed; pending futures settle | Planned; evidence gates open |
| WP-03 | Cluster sentinel and routing | Internal planning vocabulary (verify upstream public identity): HashSlot, TopologySnapshot, Redirect | ASK does not permanently rewrite ownership; redirect loops are bounded; stale topology cannot route cross-slot transactions silently | Planned; evidence gates open |
| WP-04 | Transactions scripts and subscriptions | Internal planning vocabulary (verify upstream public identity): TransactionQueue, ScriptHandle, SubscriptionState | Aborted transactions remain distinguishable from empty results; reconnect resubscription is documented; slow consumers have bounded queues | Planned; evidence gates open |
| WP-05 | Command coverage and operational validation | Internal planning vocabulary (verify upstream public identity): CommandCoverage, ServerProfile, ConnectionDiagnostics | Every claimed command has routing/codec fixtures; unavailable server features return explicit errors; diagnostics redact authentication material | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Pinned upstream RESP coverage and server compatibility need inspection; topology updates may race with requests.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
