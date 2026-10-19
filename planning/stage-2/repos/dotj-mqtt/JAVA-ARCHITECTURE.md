# DJ-034 .j MQTT: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide MQTT clients, managed connection workflows and broker capabilities where present upstream.

Product type: JVM protocol framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-mqtt-01 | MqttPacket, ProtocolVersion, PropertySet | Packet codecs and negotiation |
| dotj-mqtt-02 | ClientSession, SessionExpiry, KeepAliveState | Client connection and session state |
| dotj-mqtt-03 | PacketIdentifier, InflightRecord, DeliveryState | QoS inflight and retained delivery |
| dotj-mqtt-04 | SubscriptionFilter, BrokerSession, RetainedMessage | Broker subscriptions and routing |
| dotj-mqtt-05 | MqttCapability, TransportAdapter, ProtocolTrace | Extensions transports and conformance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Pin supported MQTT versions; QoS packet lifecycle, retained messages and session expiry must preserve protocol state.

## Feature contracts and invariants

### WP-01: Packet codecs and negotiation

Internal analysis vocabulary (not permission to rename the public API): `MqttPacket`, `ProtocolVersion`, `PropertySet`.

Implement versioned MQTT packet framing and variable integers. Validate flags lengths properties and UTF rules. Negotiate limits and capabilities at CONNECT/CONNACK.

Required observable invariant: Malformed frames fail before allocation growth; unsupported versions are explicit; version-specific properties cannot leak into older packets.

### WP-02: Client connection and session state

Internal analysis vocabulary (not permission to rename the public API): `ClientSession`, `SessionExpiry`, `KeepAliveState`.

Define connect reconnect ping and disconnect transitions. Persist session state according to clean-start/session-expiry rules. Handle transport TLS cancellation and connection loss.

Required observable invariant: Reconnect obeys negotiated session status; stale packets cannot complete new operations; keepalive uses deterministic clock tests.

### WP-03: QoS inflight and retained delivery

Internal analysis vocabulary (not permission to rename the public API): `PacketIdentifier`, `InflightRecord`, `DeliveryState`.

Specify QoS0/1/2 handshake state machines. Handle duplicates retransmission and receive maximum. Separate broker delivery guarantees from application processing.

Required observable invariant: QoS2 duplicate handshakes do not corrupt state; packet IDs are not reused while live; no end-to-end exactly-once claim is inferred.

### WP-04: Broker subscriptions and routing

Internal analysis vocabulary (not permission to rename the public API): `SubscriptionFilter`, `BrokerSession`, `RetainedMessage`.

Implement topic filters shared subscriptions and authorization hooks. Define retained-message update and expiry. Bound per-client queues and slow-consumer behavior.

Required observable invariant: Wildcard matching has normative fixtures; unauthorized subscriptions fail; a slow subscriber cannot exhaust broker memory.

### WP-05: Extensions transports and conformance

Internal analysis vocabulary (not permission to rename the public API): `MqttCapability`, `TransportAdapter`, `ProtocolTrace`.

Separate TCP WebSocket and server/client capability profiles. Port upstream packet/client/server regressions. Run reconnect TLS malformed-packet and interoperability suites.

Required observable invariant: Each advertised MQTT version is tested independently; unsupported transports fail explicitly; protocol transcripts exclude credentials.

## Bootstrap and dependency boundaries

NIO, SSLEngine, buffers and scheduled executors.

Proposed .j dependencies: core;web(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MQTTnet usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `MqttPacket` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Malformed frames fail before allocation growth; unsupported versions are explicit; version-specific properties cannot leak into older packets. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
