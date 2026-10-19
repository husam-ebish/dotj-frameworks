# DJ-042 .j MultiUI: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Core/tests/UnitTests/BrushTests.cs:12](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/BrushTests.cs#L12) | BrushColorsAreImmutable | yes |
| [src/Core/tests/UnitTests/BrushTests.cs:22](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/BrushTests.cs#L22) | BrushValuesMatchColorValues | yes |
| [src/Core/tests/UnitTests/PaintTests.cs:10](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/PaintTests.cs#L10) | TestLinearGradientPaintConstructor | yes |
| [src/Core/tests/UnitTests/PaintTests.cs:19](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/PaintTests.cs#L19) | TestLinearGradientPaintStartColor | yes |
| [src/Core/tests/UnitTests/PaintTests.cs:27](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/PaintTests.cs#L27) | TestLinearGradientPaintEndColor | yes |
| [src/Core/tests/UnitTests/PaintTests.cs:35](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/PaintTests.cs#L35) | TestNullOrEmptyLinearGradientPaint | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-042-F01-01 | WP-01 | Handlers attach/detach once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F01-02 | WP-01 | navigation state survives documented lifecycle transitions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F01-03 | WP-01 | platform overrides do not mutate shared global maps | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F02-01 | WP-02 | Compiled and runtime XAML agree on fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F02-02 | WP-02 | missing resources have source diagnostics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F02-03 | WP-02 | layout differences are recorded per backend | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F03-01 | WP-03 | Denied permissions produce explicit results | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F03-02 | WP-03 | rotation does not leak peers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F03-03 | WP-03 | device APIs are tested on declared API levels | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F04-01 | WP-04 | No mobile platform is claimed before executable proof | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F04-02 | WP-04 | native dependencies/licenses are enumerated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F04-03 | WP-04 | signing credentials remain external | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F05-01 | WP-05 | Each supported target has install/launch evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F05-02 | WP-05 | unsupported APIs fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-042-F05-03 | WP-05 | shared tests do not replace device-specific validation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Device lifecycle; permissions; orientation; accessibility; native handler parity; store packaging/signing; suspend/resume.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
