# DJ-046 .j Material: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/MudBlazor.UnitTests/Components/FabTests.cs:17](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L17) | DefaultAppearance | yes |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:33](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L33) | VariantSetsClasses | yes |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:51](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L51) | DisabledKeepsVariantClass | yes |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:66](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L66) | DisabledRemovesRipple | yes |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:78](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L78) | LabelExtendsFabBetweenIcons | yes |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:96](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L96) | RendersNoIconWhenNoneIsSet | yes |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:107](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L107) | DropShadowOffRemovesElevation | yes |
| [src/MudBlazor.UnitTests/Components/CardTests.cs:16](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/CardTests.cs#L16) | CardChildContent | yes |
| [src/MudBlazor.UnitTests/Components/CardTests.cs:31](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/CardTests.cs#L31) | CardMedia_Should_KeepUserSuppliedTitle | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-046-F01-01 | WP-01 | Parameter changes produce deterministic output | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F01-02 | WP-01 | disposal releases subscriptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F01-03 | WP-01 | MudBlazor ownership is not confused with desktop MaterialDesignInXaml | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F02-01 | WP-02 | Late validation cannot overwrite newer input | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F02-02 | WP-02 | error text is associated with its field | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F02-03 | WP-02 | culture-dependent values have explicit parsing rules | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F03-01 | WP-03 | Superseded remote loads are cancelled or ignored | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F03-02 | WP-03 | editing preserves key identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F03-03 | WP-03 | virtualized memory is bounded by viewport/cache policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F04-01 | WP-04 | Closing a host resolves pending dialogs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F04-02 | WP-04 | focus returns correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F04-03 | WP-04 | notifications remain accessible without stealing keyboard focus | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F05-01 | WP-05 | No browser JVM is assumed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F05-02 | WP-05 | theme changes preserve component state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F05-03 | WP-05 | assets carry notices | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F05-04 | WP-05 | interop version mismatch fails visibly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F06-01 | WP-06 | Visual resemblance alone cannot mark a component compatible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F06-02 | WP-06 | every claimed component has interaction evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-046-F06-03 | WP-06 | complex widgets remain visible if gated | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Keyboard/focus; ARIA; RTL; responsive layouts; virtualized grids; theme contrast; server reconnect.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
