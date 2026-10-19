# DJ-054 .j Coverage: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/coverlet.core.tests/CoverageResultTests.cs:65](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs#L65) | TestGetThresholdTypesBelowThresholdLine | yes |
| [test/coverlet.core.tests/CoverageResultTests.cs:84](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs#L84) | TestGetThresholdTypesBelowThresholdMethod | yes |
| [test/coverlet.core.tests/CoverageResultTests.cs:103](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs#L103) | TestGetThresholdTypesBelowThresholdBranch | yes |
| [test/coverlet.core.tests/CoverageResultTests.cs:122](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs#L122) | TestGetThresholdTypesBelowThresholdAllGood | yes |
| [test/coverlet.core.tests/CoverageResultTests.cs:141](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs#L141) | TestGetThresholdTypesBelowThresholdAllFail | yes |
| [test/coverlet.core.tests/CoverageResultTests.cs:161](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs#L161) | TestGetThresholdTypesBelowThresholdWhenNoModuleInstrumented | yes |
| [test/coverlet.integration.tests/WpfResolverTests.cs:24](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.integration.tests/WpfResolverTests.cs#L24) | TestInstrument_NetCoreSharedFrameworkResolver | yes |
| [test/coverlet.integration.tests/WpfResolverTests.cs:51](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.integration.tests/WpfResolverTests.cs#L51) | TestInstrument_NetCoreSharedFrameworkResolver_SelfContained | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-054-F01-01 | WP-01 | Instrumented classes pass verification | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F01-02 | WP-01 | constructors/exceptions/synchronized blocks behave equivalently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F01-03 | WP-01 | unsupported bytecode versions fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F02-01 | WP-02 | Reported totals reconcile with declared denominator | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F02-02 | WP-02 | missing debug info is visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F02-03 | WP-02 | IL branches are not relabeled JVM branches | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F03-01 | WP-03 | Duplicate sessions do not double-count | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F03-02 | WP-03 | changed classes cannot merge silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F03-03 | WP-03 | incomplete runs are marked incomplete | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F04-01 | WP-04 | Filters are explainable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F04-02 | WP-04 | report totals match raw data | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F04-03 | WP-04 | threshold failures distinguish missing data from insufficient coverage | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F05-01 | WP-05 | No claimed support without verifier/semantic evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F05-02 | WP-05 | incompatible agents are diagnosed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-054-F05-03 | WP-05 | no JaCoCo substitution supplies coverage implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Branch attribution; exceptions; constructors; retransformation; multi-loader classes; forked JVM merging; deterministic reports.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
