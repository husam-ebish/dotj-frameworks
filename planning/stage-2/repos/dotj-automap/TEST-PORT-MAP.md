# DJ-064 .j Automap: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/UnitTests/MaxDepthTests.cs:17](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L17) | AddChild | not confirmed |
| [src/UnitTests/MaxDepthTests.cs:54](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L54) | Second_level_children_is_empty_with_max_depth_1 | yes |
| [src/UnitTests/MaxDepthTests.cs:62](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L62) | Second_level_children_are_not_null_with_max_depth_2 | yes |
| [src/UnitTests/MaxDepthTests.cs:75](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L75) | Third_level_children_is_empty_with_max_depth_2 | yes |
| [src/UnitTests/MaxDepthTests.cs:86](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L86) | Third_level_children_are_not_null_max_depth_3 | yes |
| [src/UnitTests/IgnoreAllTests.cs:29](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L29) | Should_not_ignore | yes |
| [src/UnitTests/IgnoreAllTests.cs:65](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L65) | GlobalIgnore_ignores_all_properties_beginning_with_string | yes |
| [src/UnitTests/IgnoreAllTests.cs:79](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L79) | GlobalIgnore_ignores_all_properties_beginning_with_string_in_profiles | yes |
| [src/UnitTests/IgnoreAllTests.cs:92](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L92) | GlobalIgnore_ignores_properties_with_names_matching_but_different_types | yes |
| [src/UnitTests/IgnoreAllTests.cs:105](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L105) | Ignored_properties_should_be_default_value | yes |
| [src/UnitTests/IgnoreAllTests.cs:120](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L120) | Ignore_supports_two_different_values | yes |
| [src/UnitTests/IgnoreAllTests.cs:150](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L150) | Ignore_On_Source_Field | yes |
| [src/UnitTests/IgnoreAllTests.cs:186](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L186) | Ignore_On_Source_Field | yes |
| [src/UnitTests/IgnoreAllTests.cs:217](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L217) | Sould_not_throw_exception_when_reverse_property_does_not_exist | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-064-F01-01 | WP-01 | No source-derived implementation proceeds under assumed MIT terms | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F01-02 | WP-01 | profile validation reports unmapped/conflicting members | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F01-03 | WP-01 | rights gate is recorded separately from architecture | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F02-01 | WP-02 | Cycles follow declared preservation policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F02-02 | WP-02 | hook order is stable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F02-03 | WP-02 | errors identify source/destination member paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F03-01 | WP-03 | Invalid reverse maps fail early | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F03-02 | WP-03 | concurrent requests cannot share scoped resolver state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F03-03 | WP-03 | cache keys include configuration identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F04-01 | WP-04 | Provider SQL remains parameterized | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F04-02 | WP-04 | unsupported resolver yields a planning diagnostic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F04-03 | WP-04 | no entire-table fallback occurs silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F05-01 | WP-05 | Behavior evidence is separate from license clearance | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F05-02 | WP-05 | no ModelMapper substitute is adopted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-064-F05-03 | WP-05 | all unresolved licensed features remain listed | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Flattening; inheritance; reverse mapping; collection/null behavior; validation errors; query projection correctness.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
