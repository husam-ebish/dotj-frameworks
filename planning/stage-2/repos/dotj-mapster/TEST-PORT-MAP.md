# DJ-024 .j Mapster: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:55](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L55) | ThrowExceptionWhenInterfaceIsNotVisible | yes |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:64](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L64) | CreateTypeForSimpleInterface | yes |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:80](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L80) | CreateTypeForInheritedInterface | yes |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:98](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L98) | CreateTypeForComplexInterface | yes |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:128](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L128) | WhenMappingDerivedFromInterfaceWithoutMembers | yes |
| [src/TemplateTest/FooTest.cs:13](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L13) | TestCreateMapExpression | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-024-F01-01 | WP-01 | A map has a reproducible effective configuration | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F01-02 | WP-01 | ambiguous members fail early | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F01-03 | WP-01 | configuration caches are isolated by scope | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F02-01 | WP-02 | Nested failures name the member path | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F02-02 | WP-02 | cycles terminate by policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F02-03 | WP-02 | collection replacement versus merge is predictable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F03-01 | WP-03 | Generated and runtime maps agree on fixed fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F03-02 | WP-03 | clean rebuild produces equivalent source | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F03-03 | WP-03 | diagnostics point to the declaration | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F04-01 | WP-04 | Unsupported converter never falls back to full-table client mapping silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F04-02 | WP-04 | projected null semantics match provider profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F05-01 | WP-05 | Core mapper loads without a DI framework | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F05-02 | WP-05 | warm/cold results are reported separately | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-024-F05-03 | WP-05 | no existing Java mapper replaces implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Nested mapping; cycles; null handling; constructor selection; inherited configs; generated/runtime parity.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
