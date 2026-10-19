# DJ-010 .j Templates: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Microsoft.TemplateEngine.Cli.UnitTests/JExtensionsTests.cs:14](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/JExtensionsTests.cs#L14) | ToInt32ParsesStringPropertyValues | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:15](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L15) | CanShrinkOneColumn | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:42](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L42) | CanShrinkMultipleColumnsAndBalanceShrinking | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:69](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L69) | CannotShrinkOverMinimumWidth | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:96](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L96) | CanShowDefaultColumns | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:124](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L124) | CanShowUserSelectedColumns | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:153](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L153) | CanShowAllColumns | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:177](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L177) | CanCenterAlign | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:200](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L200) | CanRightAlign | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:223](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L223) | CanCalculateWidthCorrectly | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:261](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L261) | CanShrinkWideCharsCorrectly | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:299](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L299) | CanIndentAllRows | yes |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs:323](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs#L323) | VerifyColumnsOptionHasAllColumnNamesDefined | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-010-F01-01 | WP-01 | Duplicate identities are diagnosed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F01-02 | WP-01 | malformed manifests do not enter catalog | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F01-03 | WP-01 | discovery executes no post-actions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F02-01 | WP-02 | Circular symbols fail with a path | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F02-02 | WP-02 | conditional renames are deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F02-03 | WP-02 | binary fixture checksums stay identical | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F03-01 | WP-03 | Archives cannot escape destination | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F03-02 | WP-03 | case-insensitive collisions are caught before writes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F03-03 | WP-03 | interruption leaves original user files intact | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F04-01 | WP-04 | Corrupt packages never become selectable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F04-02 | WP-04 | uninstall preserves generated projects | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F04-03 | WP-04 | unattended creation does not silently run arbitrary shell commands | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F05-01 | WP-05 | Same locked template and inputs produce equivalent trees | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F05-02 | WP-05 | adapter rejects CLR-only post-actions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-010-F05-03 | WP-05 | SDK receives structured conflicts and exit status | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Symbol precedence; rename collisions; binary file preservation; traversal and symlink attacks; rollback on failure.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
