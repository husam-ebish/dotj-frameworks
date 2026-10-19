# DJ-015 .j Actors: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Orleans.Core.Tests/ConfigTests.cs:37](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L37) | Config_AzureConnectionInfo | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:53](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L53) | Config_AdoNetConnectionInfo | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:65](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L65) | Config_LocalIPAddressFallback_UsesIPv4Loopback | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:72](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L72) | Config_LocalIPAddressFallback_UsesIPv6Loopback | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:79](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L79) | Config_LocalIPAddressFallback_ThrowsForExplicitInterface | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:85](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L85) | CollectionAttributes_NullProperties_ThrowWithExactParameterName | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:99](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L99) | CollectionAttributes_ValidProperties_PreserveIdleDeactivationValues | yes |
| [test/Orleans.Core.Tests/ConfigTests.cs:117](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs#L117) | ClusterOptionsValidator_NullOptions_ThrowsWithExactParameterName | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:21](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L21) | IdSpan_CreateEmptyString_NotEqualToDefault | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:37](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L37) | IdSpan_HashCode_ConsistentWithEquality | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:55](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L55) | IdSpan_Default_HasExpectedProperties | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:68](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L68) | IdSpan_CreateEmptyString_HasExpectedProperties | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:82](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L82) | IdSpan_SameContent_AreEqual | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:97](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L97) | IdSpan_DifferentContent_AreNotEqual | yes |
| [test/Orleans.Core.Tests/IdSpanTests.cs:111](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs#L111) | IdSpan_CompareTo_HandlesNullAndEmpty | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-015-F01-01 | WP-01 | Concurrent first calls cannot silently create conflicting authoritative activations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F01-02 | WP-01 | reentrant waits have documented behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F01-03 | WP-01 | collected activations release resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F02-01 | WP-02 | A partition scenario has an explicit availability/consistency outcome | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F02-02 | WP-02 | stale epochs cannot commit ownership changes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F02-03 | WP-02 | placement is explainable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F03-01 | WP-03 | Unknown fields follow schema policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F03-02 | WP-03 | lost replies never imply exactly-once execution | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F03-03 | WP-03 | caller cancellation does not falsely prove remote rollback | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F04-01 | WP-04 | Conflicting writes are surfaced | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F04-02 | WP-04 | reminders survive activation loss according to store guarantees | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F04-03 | WP-04 | slow subscribers cannot grow memory without bounds | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F05-01 | WP-05 | Unsupported provider guarantees are stated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F05-02 | WP-05 | rolling upgrades preserve declared schemas | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-015-F05-03 | WP-05 | no successful test is generalized into exactly-once delivery | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Split brain; activation races; reentrant deadlocks; serializer evolution; node loss during writes; rolling upgrades.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
