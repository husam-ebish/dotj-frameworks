# DJ-034 .j MQTT: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Pin supported MQTT versions; QoS packet lifecycle, retained messages and session expiry must preserve protocol state.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Packet codecs and negotiation | Internal planning vocabulary (verify upstream public identity): MqttPacket, ProtocolVersion, PropertySet | Malformed frames fail before allocation growth; unsupported versions are explicit; version-specific properties cannot leak into older packets | Planned; evidence gates open |
| WP-02 | Client connection and session state | Internal planning vocabulary (verify upstream public identity): ClientSession, SessionExpiry, KeepAliveState | Reconnect obeys negotiated session status; stale packets cannot complete new operations; keepalive uses deterministic clock tests | Planned; evidence gates open |
| WP-03 | QoS inflight and retained delivery | Internal planning vocabulary (verify upstream public identity): PacketIdentifier, InflightRecord, DeliveryState | QoS2 duplicate handshakes do not corrupt state; packet IDs are not reused while live; no end-to-end exactly-once claim is inferred | Planned; evidence gates open |
| WP-04 | Broker subscriptions and routing | Internal planning vocabulary (verify upstream public identity): SubscriptionFilter, BrokerSession, RetainedMessage | Wildcard matching has normative fixtures; unauthorized subscriptions fail; a slow subscriber cannot exhaust broker memory | Planned; evidence gates open |
| WP-05 | Extensions transports and conformance | Internal planning vocabulary (verify upstream public identity): MqttCapability, TransportAdapter, ProtocolTrace | Each advertised MQTT version is tested independently; unsupported transports fail explicitly; protocol transcripts exclude credentials | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Determine managed-client/module distribution at pinned release; broker persistence and WebSocket transport ownership remain decisions.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
