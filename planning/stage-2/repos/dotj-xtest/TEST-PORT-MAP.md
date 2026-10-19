# DJ-050 .j XTest: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/xunit.v3.core.tests/RecordTests.cs:9](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L9) | Exception | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:20](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L20) | NoException | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:31](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L31) | SkipExceptionEscapes | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:50](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L50) | Exception | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:61](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L61) | NoException | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:71](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L71) | SkipExceptionEscapes | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:90](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L90) | GuardClause | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:101](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L101) | Exception | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:112](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L112) | NoException | yes |
| [src/xunit.v3.core.tests/RecordTests.cs:122](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs#L122) | SkipExceptionEscapes | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:16](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L16) | AmbientTestContextIsAvailableInTest | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:46](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L46) | KeyValueStorageIsAvailableThroughoutPipeline | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:55](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L55) | CancellationTokenReturnsDefaultTokenWhenDisposed | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:65](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L65) | TryingToCancelFromDisposedContextDoesNotThrow | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:76](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L76) | StringAttachmentCannotBeReplacedByDefault | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:89](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L89) | StringAttachmentCanBeReplaced | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:103](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L103) | BinaryAttachmentCannotBeReplacedByDefault | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:116](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L116) | BinaryAttachmentCanBeReplaced | yes |
| [src/xunit.v3.core.tests/TestContextTests.cs:137](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L137) | Dispose | not confirmed |
| [src/xunit.v3.core.tests/TestContextTests.cs:150](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs#L150) | Dispose | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-050-F01-01 | WP-01 | Discovery is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F01-02 | WP-01 | malformed theories report discovery errors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F01-03 | WP-01 | IDs stay stable under unrelated source changes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F02-01 | WP-02 | Fixtures dispose once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F02-02 | WP-02 | failed setup prevents test body | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F02-03 | WP-02 | teardown errors remain visible beside assertion failure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F03-01 | WP-03 | Failure output identifies first meaningful difference | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F03-02 | WP-03 | data streams close | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F03-03 | WP-03 | async exceptions are observed rather than lost | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F04-01 | WP-04 | A crashed worker is distinguishable from failed tests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F04-02 | WP-04 | nonparallel collections are honored | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F04-03 | WP-04 | report totals reconcile with discovered/executed cases | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F05-01 | WP-05 | No JUnit engine supplies the implementation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F05-02 | WP-05 | self-tests include an independent subprocess oracle | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-050-F05-03 | WP-05 | adapter failures cannot masquerade as green tests | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Fixture scope; theory enumeration failure; parallel collections; skipped tests; timeouts; deterministic reporting.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-050-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-050-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-050-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
