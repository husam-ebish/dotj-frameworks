# DJ-055 .j Benchmark: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/BenchmarkDotNet.Tests/FolderNameTests.cs:19](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/tests/BenchmarkDotNet.Tests/FolderNameTests.cs#L19) | ToFolderNameTest | yes |
| [tests/BenchmarkDotNet.Tests/FolderNameTests.cs:26](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/tests/BenchmarkDotNet.Tests/FolderNameTests.cs#L26) | ToFolderNameStructTest | yes |
| [tests/BenchmarkDotNet.Tests/FolderNameTests.cs:35](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/tests/BenchmarkDotNet.Tests/FolderNameTests.cs#L35) | FileNamesAreConsistentAcrossOSes | yes |
| [tests/BenchmarkDotNet.Tests/GlobFilterTests.cs:19](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/tests/BenchmarkDotNet.Tests/GlobFilterTests.cs#L19) | TheFilterIsCaseInsensitive | yes |
| [tests/BenchmarkDotNet.Tests/GlobFilterTests.cs:40](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/tests/BenchmarkDotNet.Tests/GlobFilterTests.cs#L40) | TheFilterWorksWithParams | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-055-F01-01 | WP-01 | All parameter combinations have stable IDs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F01-02 | WP-01 | setup is outside measured interval unless configured | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F01-03 | WP-01 | failed runs publish no misleading timing | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F02-01 | WP-02 | Reports identify JVM/CPU/OS/flags | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F02-02 | WP-02 | warmup and measurement data are separate | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F02-03 | WP-02 | timer overhead is measured and accounted for | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F03-01 | WP-03 | Recomputed summaries match raw data | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F03-02 | WP-03 | outlier removal is visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F03-03 | WP-03 | noisy comparisons are not labeled definitive wins | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F04-01 | WP-04 | Unsupported counters are unavailable rather than zero | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F04-02 | WP-04 | profiler versions are recorded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F04-03 | WP-04 | diagnostic overhead does not contaminate primary results invisibly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F05-01 | WP-05 | No JMH framework replaces the harness | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F05-02 | WP-05 | exports retain units | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-055-F05-03 | WP-05 | deterministic harness tests are separate from noisy performance expectations | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Known workload sanity checks; timer overhead; dead-code elimination controls; process isolation; thermal/noise disclosure.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-055-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-055-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-055-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
