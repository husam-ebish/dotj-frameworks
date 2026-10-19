# DJ-020 .j SQL: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/Dapper.Tests/XmlTests.cs:16](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L16) | CommonXmlTypesSupported | yes |
| [tests/Dapper.Tests/EnumTests.cs:16](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L16) | TestEnumWeirdness | yes |
| [tests/Dapper.Tests/EnumTests.cs:23](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L23) | TestEnumStrings | yes |
| [tests/Dapper.Tests/EnumTests.cs:33](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L33) | TestEnumParamsWithNullable | yes |
| [tests/Dapper.Tests/EnumTests.cs:45](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L45) | TestEnumParamsWithoutNullable | yes |
| [tests/Dapper.Tests/EnumTests.cs:93](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L93) | AdoNetEnumValue | yes |
| [tests/Dapper.Tests/EnumTests.cs:109](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L109) | DapperEnumValue_SqlServer | yes |
| [tests/Dapper.Tests/EnumTests.cs:128](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L128) | SO27024806_TestVarcharEnumMemberWithExplicitConstructor | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-020-F01-01 | WP-01 | Closing a result releases owned statements | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F01-02 | WP-01 | caller transactions are not committed implicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F01-03 | WP-01 | cancellation outcome reflects driver uncertainty | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F02-01 | WP-02 | Empty lists follow declared SQL policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F02-02 | WP-02 | null parameter types are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F02-03 | WP-02 | placeholder parsing cannot rewrite literal SQL text | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F03-01 | WP-03 | Schema changes cannot reuse incompatible mappings | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F03-02 | WP-03 | errors identify column and destination | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F03-03 | WP-03 | primitive nulls use declared policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F04-01 | WP-04 | Unread grids are drained or closed predictably | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F04-02 | WP-04 | split ambiguity is reported | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F04-03 | WP-04 | partial batch success is not collapsed into an all-or-nothing result | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F05-01 | WP-05 | Unsupported provider features fail visibly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F05-02 | WP-05 | extension provenance is separate | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-020-F05-03 | WP-05 | performance reports include query data and resource ownership assumptions | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Nulls; duplicate columns; multi-result sets; parameter expansion; cancellation; transaction reuse; connection leaks.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
