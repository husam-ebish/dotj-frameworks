# DJ-011 .j Containers: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:62](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L62) | VerifyBlazorWasmScenario | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:91](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L91) | VerifyInsecureFiles | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:98](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L98) | VerifyNoSasToken | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:105](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L105) | VerifyEnvironmentVariables | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:142](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L142) | VerifyDotnetFolderContents | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:174](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L174) | VerifyInstalledPackages | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:181](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L181) | VerifyDefaultUser | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:191](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L191) | VerifyGitInstallation | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:204](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L204) | VerifyTarInstallation | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:219](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L219) | VerifyDnxInstallation | not confirmed |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs:32](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs#L32) | VerifyTestData | yes |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs:90](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs#L90) | VerifyTestDataDockerfilePaths | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-011-F01-01 | WP-01 | Every image can be traced to immutable inputs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F01-02 | WP-01 | no floating base tag is used in reproducibility claims | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F01-03 | WP-01 | unsupported platforms remain explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F02-01 | WP-02 | Two clean builds have explainable digest differences or identical output | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F02-02 | WP-02 | registry credentials never occur in layers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F02-03 | WP-02 | service-provider modules survive linking | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F03-01 | WP-03 | SIGTERM reaches application lifecycle | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F03-02 | WP-03 | writable paths are declared | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F03-03 | WP-03 | TLS and timezone fixtures pass on each advertised image | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F04-01 | WP-04 | Manifest entries refer only to tested images | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F04-02 | WP-04 | native loading failures are attributable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F04-03 | WP-04 | Linux evidence is never used as proof of Windows support | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F05-01 | WP-05 | Published digest retains its verification record | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F05-02 | WP-05 | rebuilds update dependency locks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-011-F05-03 | WP-05 | rollback selects a known immutable manifest | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Non-root startup; signals and graceful shutdown; read-only root; CA/timezone behavior; image SBOM and multi-architecture smoke tests.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
