# DJ-007 .j Diagnostics: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/tests/SOS.Tests/ClrUTests.cs:28](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/ClrUTests.cs#L28) | ClrU_StructureLinesOffsets | not confirmed |
| [src/tests/SOS.Tests/ClrUTests.cs:61](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/ClrUTests.cs#L61) | ClrU_InterleavesGcInfoEhInfoIl | not confirmed |
| [src/tests/SOS.Tests/ClrUTests.cs:87](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/ClrUTests.cs#L87) | ClrU_AcceptsInstructionPointer | not confirmed |
| [src/tests/SOS.Tests/DumpIlTests.cs:21](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/DumpIlTests.cs#L21) | DumpIl_DecodesKnownMethod | not confirmed |
| [src/tests/SOS.Tests/DumpIlTests.cs:44](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/DumpIlTests.cs#L44) | DumpIl_RejectsEmptyExpression | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-007-F01-01 | WP-01 | PID reuse never attaches to the replacement process | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F01-02 | WP-01 | permission failures expose no target secrets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F01-03 | WP-01 | target death produces a bounded failure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F02-01 | WP-02 | GC allocation and thread fixtures yield correlated events | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F02-02 | WP-02 | overload increments loss counters | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F02-03 | WP-02 | stopped sessions leave no recording running | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F03-01 | WP-03 | Unknown formats fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F03-02 | WP-03 | a known retained object has an explainable root path | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F03-03 | WP-03 | mismatched symbols are rejected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F04-01 | WP-04 | A per-command matrix distinguishes supported JVM equivalents from unproven CLR readers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F04-02 | WP-04 | no JVM dump is labeled CLR-compatible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F05-01 | WP-05 | Reports include clock units target identity and collector version | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-007-F05-02 | WP-05 | baseline and observed overhead are recorded without invented thresholds | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Attach permissions; process disappearance; allocation/GC traces; symbol mismatches; overhead and secret redaction.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-007-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-007-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-007-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
