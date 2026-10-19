# DJ-047 .j Components: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [Radzen.Blazor.Tests/FabTests.cs:9](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L9) | Fab_Renders_WithClassName | yes |
| [Radzen.Blazor.Tests/FabTests.cs:19](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L19) | Fab_Renders_IconParameter | yes |
| [Radzen.Blazor.Tests/FabTests.cs:31](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L31) | Fab_DefaultSize_IsLarge | yes |
| [Radzen.Blazor.Tests/FabTests.cs:40](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L40) | Fab_Renders_IconOnly_Class | yes |
| [Radzen.Blazor.Tests/FabTests.cs:52](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L52) | Fab_Renders_ButtonStyle | yes |
| [Radzen.Blazor.Tests/FabTests.cs:64](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L64) | Fab_Renders_Variant | yes |
| [Radzen.Blazor.Tests/FabTests.cs:76](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L76) | Fab_Renders_DisabledState | yes |
| [Radzen.Blazor.Tests/FabTests.cs:88](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L88) | Fab_Renders_TextParameter | yes |
| [Radzen.Blazor.Tests/FabTests.cs:100](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L100) | Fab_Renders_Shade | yes |
| [Radzen.Blazor.Tests/FabTests.cs:112](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L112) | Fab_NotVisible_DoesNotRender | yes |
| [Radzen.Blazor.Tests/MD5Tests.cs:22](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/MD5Tests.cs#L22) | InputsAroundThePaddingBoundaryHashLikeRfc1321 | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-047-F01-01 | WP-01 | Parameter changes produce deterministic render changes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F01-02 | WP-01 | disposed components release handlers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F01-03 | WP-01 | unsupported component APIs remain inventoried | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F02-01 | WP-02 | Stale validation results cannot overwrite newer input state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F02-02 | WP-02 | errors remain associated with fields | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F02-03 | WP-02 | keyboard input and IME behavior are tested | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F03-01 | WP-03 | Out-of-order responses cannot replace newer data | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F03-02 | WP-03 | selections follow declared identity rules | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F03-03 | WP-03 | large lists render bounded visible state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F04-01 | WP-04 | Dialog close restores focus | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F04-02 | WP-04 | RTL fixtures remain usable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F04-03 | WP-04 | asset versions/licenses are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F04-04 | WP-04 | no unreviewed frontend framework is silently adopted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F05-01 | WP-05 | Server-only operation is distinguished from required browser behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F05-02 | WP-05 | hydration retains state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F05-03 | WP-05 | claimed components have interaction and accessibility evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F06-01 | WP-06 | Cancelled uploads release resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F06-02 | WP-06 | timezone changes preserve event identity rules | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-047-F06-03 | WP-06 | proprietary designer functionality is not claimed from the open repository | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Grid filtering/sorting; upload cancellation; chart accessibility; date/time locales; keyboard navigation; RTL.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
