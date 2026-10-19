# DJ-051 .j Test: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [CakeScripts.Tests/VersionParsersTests.cs:9](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/VersionParsersTests.cs#L9) | ThatWeCanParseAssemblyVersionStrings | yes |
| [src/NUnitFramework/tests/WorkItemTests.cs:20](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L20) | CreateWorkItems | not confirmed |
| [src/NUnitFramework/tests/WorkItemTests.cs:31](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L31) | DisposeWorkItems | not confirmed |
| [src/NUnitFramework/tests/WorkItemTests.cs:37](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L37) | ConstructWorkItem | yes |
| [src/NUnitFramework/tests/WorkItemTests.cs:48](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L48) | ExecuteWorkItem | yes |
| [src/NUnitFramework/tests/WorkItemTests.cs:61](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L61) | CanStopRun | yes |
| [src/NUnitFramework/tests/WorkItemTests.cs:79](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L79) | DummyTest | not confirmed |
| [src/NUnitFramework/tests/WorkItemTests.cs:87](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L87) | GetsTargetApartmentFromParentTests | yes |
| [src/NUnitFramework/tests/WorkItemTests.cs:95](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L95) | GetsTargetApartmentFromParentTestsInWrappedTests | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-051-F01-01 | WP-01 | Invalid fixture combinations produce explicit errors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F01-02 | WP-01 | category filters are reproducible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F01-03 | WP-01 | discovery does not execute test bodies | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F02-01 | WP-02 | Actual-value suppliers execute according to contract | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F02-02 | WP-02 | compound constraints report meaningful subfailures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F02-03 | WP-02 | tolerance semantics are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F03-01 | WP-03 | Failed setup has documented teardown behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F03-02 | WP-03 | context cannot leak across parallel tests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F03-03 | WP-03 | original failures survive cleanup exceptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F04-01 | WP-04 | Case explosion has explicit limits | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F04-02 | WP-04 | nonparallel rules are enforced | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F04-03 | WP-04 | timed-out processes cannot corrupt runner state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F05-01 | WP-05 | Framework can run under a minimal owned harness | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F05-02 | WP-05 | crashed tests have distinct results | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-051-F05-03 | WP-05 | external engine sources remain separately tracked | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Setup/teardown failure ordering; combinatorial cases; constraints; parallel scope; culture and timeout restoration.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
