# DJ-048 .j Structured Log: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Serilog.Tests/LogTests.cs:7](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs#L7) | TheUninitializedLoggerIsSilent | yes |
| [test/Serilog.Tests/LogTests.cs:15](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs#L15) | CloseAndFlushDisposesTheLogger | yes |
| [test/Serilog.Tests/LogTests.cs:24](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs#L24) | CloseAndFlushResetsLoggerToSilentLogger | yes |
| [test/Serilog.Tests/LogTests.cs:34](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs#L34) | CloseAndFlushAsyncDisposesTheLogger | yes |
| [test/Serilog.Tests/LogTests.cs:43](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs#L43) | CloseAndFlushAsyncDisposesTheLoggerEvenWhenItIsNotAsyncDisposable | yes |
| [test/Serilog.Tests/LogTests.cs:53](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs#L53) | CloseAndFlushAsyncResetsLoggerToSilentLogger | yes |
| [test/Serilog.Tests/VersioningTests.cs:6](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/VersioningTests.cs#L6) | AssemblyIsExplicitlyVersioned | yes |
| [test/Serilog.Tests/VersioningTests.cs:14](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/VersioningTests.cs#L14) | AssemblySubordinateVersionPartsAreZero | yes |
| [test/Serilog.Tests/VersioningTests.cs:22](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/VersioningTests.cs#L22) | AssemblyIsSigned | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-048-F01-01 | WP-01 | Template holes bind deterministically | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F01-02 | WP-01 | cycles cannot recurse forever | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F01-03 | WP-01 | structured values survive independent formatting | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F02-01 | WP-02 | Concurrent scopes do not leak properties | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F02-02 | WP-02 | duplicate enrichment precedence is stable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F02-03 | WP-02 | disabled levels avoid unnecessary value construction | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F03-01 | WP-03 | Shutdown has a bounded flush result | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F03-02 | WP-03 | queue overflow is observable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F03-03 | WP-03 | sink errors do not recurse through the same failing logger | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F04-01 | WP-04 | Formatting cannot inject extra JSON records | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F04-02 | WP-04 | bridge retains template/properties where possible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F04-03 | WP-04 | optional sinks do not load in core logger | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F05-01 | WP-05 | No caller-owned sink is closed unexpectedly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F05-02 | WP-05 | performance evidence names payloads and settings | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-048-F05-03 | WP-05 | Serilog behavior remains distinct from dotj-log | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Template parsing; duplicate properties; recursive destructuring; async sink loss; sensitive-data filtering; shutdown flush.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
