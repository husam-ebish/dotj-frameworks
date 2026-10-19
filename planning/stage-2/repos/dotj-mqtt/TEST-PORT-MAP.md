# DJ-034 .j MQTT: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [Source/MQTTnet.Tests/Protocol_Tests.cs:14](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/Protocol_Tests.cs#L14) | Encode_Four_Byte_Integer | yes |
| [Source/MQTTnet.Tests/Protocol_Tests.cs:35](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/Protocol_Tests.cs#L35) | Encode_Two_Byte_Integer | yes |
| [Source/MQTTnet.Tests/RoundtripTime_Tests.cs:19](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/RoundtripTime_Tests.cs#L19) | Round_Trip_Time | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-034-F01-01 | WP-01 | Malformed frames fail before allocation growth | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F01-02 | WP-01 | unsupported versions are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F01-03 | WP-01 | version-specific properties cannot leak into older packets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F02-01 | WP-02 | Reconnect obeys negotiated session status | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F02-02 | WP-02 | stale packets cannot complete new operations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F02-03 | WP-02 | keepalive uses deterministic clock tests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F03-01 | WP-03 | QoS2 duplicate handshakes do not corrupt state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F03-02 | WP-03 | packet IDs are not reused while live | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F03-03 | WP-03 | no end-to-end exactly-once claim is inferred | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F04-01 | WP-04 | Wildcard matching has normative fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F04-02 | WP-04 | unauthorized subscriptions fail | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F04-03 | WP-04 | a slow subscriber cannot exhaust broker memory | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F05-01 | WP-05 | Each advertised MQTT version is tested independently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F05-02 | WP-05 | unsupported transports fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-034-F05-03 | WP-05 | protocol transcripts exclude credentials | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

QoS 0/1/2 transitions; duplicate packets; reconnect; retained/will behavior; topic wildcards; auth and size limits.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-034-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-034-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-034-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
