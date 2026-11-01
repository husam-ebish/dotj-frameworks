# DJ-001 .j Core: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/mono/wasm/Wasm.Build.Tests/IcuTests.cs:57](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/mono/wasm/Wasm.Build.Tests/IcuTests.cs#L57) | FullIcuFromRuntimePackWithInvariant | yes |
| [src/mono/wasm/Wasm.Build.Tests/IcuTests.cs:71](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/mono/wasm/Wasm.Build.Tests/IcuTests.cs#L71) | FullIcuFromRuntimePackWithCustomIcu | yes |
| [src/mono/wasm/Wasm.Build.Tests/IcuTests.cs:88](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/mono/wasm/Wasm.Build.Tests/IcuTests.cs#L88) | NonExistingCustomFileAssertError | yes |
| [src/libraries/System.Linq/tests/AllTests.cs:12](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs#L12) | SameResultsRepeatCallsIntQuery | yes |
| [src/libraries/System.Linq/tests/AllTests.cs:23](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs#L23) | SameResultsRepeatCallsStringQuery | yes |
| [src/libraries/System.Linq/tests/AllTests.cs:54](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs#L54) | All | yes |
| [src/libraries/System.Linq/tests/AllTests.cs:63](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs#L63) | AllRunOnce | yes |
| [src/libraries/System.Linq/tests/AllTests.cs:72](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs#L72) | NullSource_ThrowsArgumentNullException | yes |
| [src/libraries/System.Linq/tests/AllTests.cs:78](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs#L78) | NullPredicate_ThrowsArgumentNullException | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-001-F01-01 | WP-01 | Equal parameterized types share identity | Independent Java and .NET oracle cases passed for one bounded shape; five supporting upstream reflection cases passed in Batch-060, without a direct reference-identity assertion. [Corpus](evidence/wp01-fixture-corpus-v10.0.12.json) |
| DJ-001-F01-02 | WP-01 | different generic arguments do not | Independent Java and .NET oracle cases passed for one bounded shape; four upstream argument-metadata cases passed, without a direct inequality assertion. [Disposition](evidence/type-inequality-disposition-v10.0.12.json) |
| DJ-001-F01-03 | WP-01 | supplied resources are never closed implicitly | Independent Java and .NET DI oracle cases passed; 37 selected upstream DI ownership/order cases passed in Batch-062. Batch 2502 matched the original Java lifecycle fixtures against a native oracle on a private runtime JAR. [Corpus](evidence/wp01-fixture-corpus-v10.0.12.json) [Lifecycle](OWNERSHIP-SOURCE-LIFECYCLE-v1.md) |
| DJ-001-F01-04 | WP-01 | context values do not leak between requests | Java explicit-context and independent same-worker CLR cases passed; two supporting upstream context methods passed. Mechanisms differ and no exact upstream cross-request case is claimed. [Corpus](evidence/wp01-fixture-corpus-v10.0.12.json) |
| DJ-001-F02-01 | WP-02 | Late registration runs synchronously | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F02-02 | WP-02 | sequential callbacks use the declared LIFO profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F02-03 | WP-02 | self-close cannot deadlock | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F02-04 | WP-02 | CancelAsync completion waits for callbacks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F02-05 | WP-02 | token identity survives source disposal as specified | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F03-01 | WP-03 | Concurrent singleton resolves return one published identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F03-02 | WP-03 | aliases close once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F03-03 | WP-03 | supplied singleton stays caller-owned | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F03-04 | WP-03 | empty-provider writes fail | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F03-05 | WP-03 | failed reload does not acquire an invented atomic guarantee | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F04-01 | WP-04 | Invalid options never publish as valid | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F04-02 | WP-04 | monitor close removes subscriptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F04-03 | WP-04 | disabled log handling follows declared formatter behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F04-04 | WP-04 | partial host startup releases completed services in defined order | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F05-01 | WP-05 | Decimal bit-preserving paths retain scale/sign | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F05-02 | WP-05 | invalid byte sequences follow explicit modes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F05-03 | WP-05 | Turkish casing and DST ambiguity are fixture-covered | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F05-04 | WP-05 | Instant conversion cannot discard unspecified Kind silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F06-01 | WP-06 | Enumerator disposal and deferred exceptions match profiles | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F06-02 | WP-06 | grouping/null/equality differences are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F06-03 | WP-06 | query IR round trips preserve node types and constants | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F06-04 | WP-06 | provider translation has no silent client execution | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F07-01 | WP-07 | Partial reads/writes and half-closes retain data | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F07-02 | WP-07 | bounded buffers enforce backpressure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F07-03 | WP-07 | file handles close on failure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F07-04 | WP-07 | network cancellation does not imply rollback | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F07-05 | WP-07 | unsupported distributed enlistment fails explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F08-01 | WP-08 | System.Text.Json tests cannot be satisfied merely by Newtonsoft behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F08-02 | WP-08 | unsafe type activation is disabled | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F08-03 | WP-08 | signature bytes and canonicalization use vectors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F08-04 | WP-08 | CLR assembly execution is never claimed from metadata parsing | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F09-01 | WP-09 | All 218 known library directories have ownership and test routes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F09-02 | WP-09 | unsupported backend calls report capability gaps | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F09-03 | WP-09 | no custom VM is assumed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-001-F09-04 | WP-09 | a backend remains blocked until a reproducible execution experiment succeeds | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Numeric overflow and decimal rounding; Turkish casing and Unicode normalization; cancellation races; stream disposal and endianness.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature needs mapped cases or an explicit independent-oracle rationale. Every skip needs a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. The bounded WP-01 internal Java fixtures and selected upstream tests have run; future public API acceptance tests and later-package fixtures remain open.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-001-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-001-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-001-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
