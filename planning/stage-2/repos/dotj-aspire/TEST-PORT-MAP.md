# DJ-013 .j Aspire: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/Aspire.Cli.Tests/ProgramTests.cs:36](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L36) | StartMainActivity_ReportsInstallSource | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:76](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L76) | StartMainActivity_DoesNotProbeWhenActivityIsNotCreated | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:96](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L96) | ParseLogFileOption_ReturnsNull_WhenArgsAreNull | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:104](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L104) | ParseLogFileOption_ReturnsValue_WhenOptionAppearsBeforeDelimiter | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:112](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L112) | ParseLogFileOption_IgnoresValue_WhenOptionAppearsAfterDelimiter | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:120](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L120) | BuildAnsiConsole_DoesNotReenablePlaygroundFormatting_WhenHostDisablesAnsi | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:145](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L145) | AcquireBundleLeaseFromEnvironment_HoldsLeaseWhenBundleVersionDirectoryIsSet | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:166](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L166) | WarnIfGlobalSettingsContainAppHostPath_WritesWarning_WhenGlobalConfigHasAppHostPath | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:183](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L183) | WarnIfGlobalSettingsContainAppHostPath_DoesNotWarn_WhenGlobalConfigHasNoAppHostPath | yes |
| [tests/Aspire.Cli.Tests/ProgramTests.cs:200](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs#L200) | WarnIfGlobalSettingsContainAppHostPath_DoesNotWarn_WhenGlobalConfigCannotBeLoaded | yes |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs:21](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs#L21) | MainReturnsExpectedExitCode | yes |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs:34](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs#L34) | LocaleOverrideReturnsExitCode | yes |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs:71](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs#L71) | DebugOutputWritesToStderr | yes |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs:97](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs#L97) | CredentialBearingSourceIsRedactedFromInvocationLog | yes |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs:140](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs#L140) | VersionFlagSuppressesBanner | yes |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs:170](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs#L170) | RenderScenarioOutputsPublishSummaryStressCase | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-013-F01-01 | WP-01 | Invalid graphs fail before launching anything | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F01-02 | WP-01 | stable resource IDs survive serialization | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F01-03 | WP-01 | secrets are not rendered into public manifests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F02-01 | WP-02 | A failed dependency blocks dependents with a reason | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F02-02 | WP-02 | partial startup cleans owned children | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F02-03 | WP-02 | user-owned processes are never terminated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F03-01 | WP-03 | Endpoint rebinding reaches consumers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F03-02 | WP-03 | incompatible integrations fail before launch | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F03-03 | WP-03 | disabled integrations introduce no runtime dependency | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F04-01 | WP-04 | Disconnected viewers release subscriptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F04-02 | WP-04 | hostile log text is escaped | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F04-03 | WP-04 | resource filters preserve correlation across restarts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F05-01 | WP-05 | Export never silently drops a required dependency | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F05-02 | WP-05 | secret references stay external | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-013-F05-03 | WP-05 | repeated export is deterministic for locked inputs | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Dependency startup order; health transitions; secret injection; failed child cleanup; local versus deployment graph fidelity.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
