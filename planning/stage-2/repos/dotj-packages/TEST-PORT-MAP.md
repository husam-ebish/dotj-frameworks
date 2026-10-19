# DJ-062 .j Packages: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/NuGet.Tests.Apex/NuGet.OptProf/Tests.cs:36](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Tests.Apex/NuGet.OptProf/Tests.cs#L36) | OpenSolutionAndBuild_PackageReferenceSdk | yes |
| [test/NuGet.Tests.Apex/NuGet.OptProf/Tests.cs:47](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Tests.Apex/NuGet.OptProf/Tests.cs#L47) | IVsPackageSourceProvider_GetSources | yes |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs:24](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs#L24) | Cycle_PackageWithSameNameAsProjectVerifyCycleDetectedAsync | yes |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs:70](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs#L70) | Cycle_ProjectWithSameNameAsProjectVerifyCycleDetectedAsync | yes |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs:118](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs#L118) | Cycle_PackageWithSameNameAsProjectVerifyCycleDetectedTwoLevelsDownAsync | yes |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs:170](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs#L170) | Cycle_PackageWithSameNameAsProjectVerifyCycleDetectedAtEndAsync | yes |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs:225](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs#L225) | Cycle_PackageCircularDependencyVerifyCycleDetectedAsync | yes |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs:284](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs#L284) | Cycle_TransitiveProjectWithSameNameAsPackageVerifyCycleDetectedAsync | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-062-F01-01 | WP-01 | NuGet packages are not treated as executable Java artifacts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F01-02 | WP-01 | traversal fails | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F01-03 | WP-01 | immutable content identity is recorded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F02-01 | WP-02 | Same input lock yields same graph | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F02-02 | WP-02 | incompatible constraints fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F02-03 | WP-02 | optional/platform dependencies remain traceable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F03-01 | WP-03 | Corrupt downloads never enter cache | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F03-02 | WP-03 | offline restore performs no network calls | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F03-03 | WP-03 | credentials cannot cross feed origins | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F04-01 | WP-04 | Repacking locked inputs produces explainable output | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F04-02 | WP-04 | conflicting immutable versions fail | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F04-03 | WP-04 | publication metadata preserves source/license provenance | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F05-01 | WP-05 | Standalone restore works without registry or SDK | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F05-02 | WP-05 | lock upgrades are reviewable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-062-F05-03 | WP-05 | a successful restore is not a security certification | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Version resolution; prerelease ranges; source conflicts; offline cache; signature failure; traversal; lockfile reproducibility.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
