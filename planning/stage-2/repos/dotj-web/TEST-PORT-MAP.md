# DJ-012 .j Web: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Testing/test/DockerTests.cs:16](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Testing/test/DockerTests.cs#L16) | DoesNotRunOnWindows | not confirmed |
| [src/Testing/test/SkipOnCITests.cs:14](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Testing/test/SkipOnCITests.cs#L14) | AlwaysSkipOnCI | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-012-F01-01 | WP-01 | Conflicting framing is rejected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F01-02 | WP-01 | slow consumers bound buffers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F01-03 | WP-01 | abort terminates body reads | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F01-04 | WP-01 | unsupported protocols are advertised honestly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F02-01 | WP-02 | Ambiguous routes fail deterministically | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F02-02 | WP-02 | middleware can observe unwind order | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F02-03 | WP-02 | malformed payloads have stable status/problem responses | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F03-01 | WP-03 | Filters execute in documented nesting | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F03-02 | WP-03 | validation errors preserve field paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F03-03 | WP-03 | generated pages render escaped output and source-linked errors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F04-01 | WP-04 | Disconnected circuits expire and release state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F04-02 | WP-04 | duplicate events are handled explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F04-03 | WP-04 | browser execution is not advertised before a runnable backend exists | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F05-01 | WP-05 | Scheme confusion tests fail closed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F05-02 | WP-05 | password/reset secrets are protected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F05-03 | WP-05 | lockout and concurrent updates behave predictably | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F05-04 | WP-05 | auth store adapters are optional | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F06-01 | WP-06 | Cross-site requests cannot bypass token checks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F06-02 | WP-06 | old keys decrypt only under declared retention | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F06-03 | WP-06 | untrusted redirects and markup are rejected or escaped | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F07-01 | WP-07 | Invocation completion is correlated once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F07-02 | WP-07 | stream cancellation releases producers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F07-03 | WP-07 | reconnect behavior is documented under lost responses and node changes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F08-01 | WP-08 | Draining stops admission then bounds in-flight work | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F08-02 | WP-08 | logs exclude credentials by default | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-012-F08-03 | WP-08 | claimed capabilities have per-protocol and per-platform evidence | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

HTTP framing/smuggling; middleware order; route selection; CSRF/XSS/authentication; SignalR reconnect; component hydration and disconnect behavior.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-012-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-012-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-012-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
