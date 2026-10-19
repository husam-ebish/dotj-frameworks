# DJ-017 .j Service Client: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/svcutilcore/tests/SvcutilTests.cs:19](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/svcutilcore/tests/SvcutilTests.cs#L19) | SvcutilTest1 | yes |
| [src/System.ServiceModel.Http/tests/ServiceModel/HttpIdentityTests.cs:12](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.ServiceModel.Http/tests/ServiceModel/HttpIdentityTests.cs#L12) | SpnEndpointIdentity_NotSupportedThrows | not confirmed |
| [src/System.ServiceModel.Http/tests/ServiceModel/HttpIdentityTests.cs:24](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.ServiceModel.Http/tests/ServiceModel/HttpIdentityTests.cs#L24) | UpnEndpointIdentityThrows | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-017-F01-01 | WP-01 | Generated clients retain wire names | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F01-02 | WP-01 | ambiguous schemas fail with locations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F01-03 | WP-01 | unsupported binding assertions are never silently ignored | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F02-01 | WP-02 | External entities are disabled by default | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F02-02 | WP-02 | attachments preserve bytes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F02-03 | WP-02 | SOAP faults retain codes and typed details | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F02-04 | WP-02 | binary XML remains gated until verified | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F03-01 | WP-03 | Aborting releases pending calls | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F03-02 | WP-03 | a faulted channel cannot be reused silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F03-03 | WP-03 | transport-specific capabilities are reported before opening | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F04-01 | WP-04 | Security policy mismatch fails before application data is sent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F04-02 | WP-04 | replay fixtures fail | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F04-03 | WP-04 | Windows identity is not emulated by passing a username header | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F05-01 | WP-05 | Interoperation evidence is binding/version specific | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F05-02 | WP-05 | client and server modules have no cycle | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-017-F05-03 | WP-05 | missing reference environment blocks claims rather than disappearing from scope | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Cross-process .NET service calls; SOAP faults; namespaces; quotas; streaming; authentication and timeout races.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-017-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-017-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-017-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
