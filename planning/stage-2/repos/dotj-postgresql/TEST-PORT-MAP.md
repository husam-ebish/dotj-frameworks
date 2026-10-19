# DJ-021 .j PostgreSQL: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Npgsql.Tests/BugTests.cs:24](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L24) | SequentialNullCheckOnNonFirstField | yes |
| [test/Npgsql.Tests/BugTests.cs:34](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L34) | SequentialSkipOverFirstRow | yes |
| [test/Npgsql.Tests/BugTests.cs:45](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L45) | SequentialConsumeWithNull | yes |
| [test/Npgsql.Tests/BugTests.cs:56](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L56) | Many_parameters_with_mixed_FormatCode | yes |
| [test/Npgsql.Tests/BugTests.cs:78](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L78) | Bug1450 | yes |
| [test/Npgsql.Tests/BugTests.cs:91](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L91) | Bug1645 | yes |
| [test/Npgsql.Tests/BugTests.cs:112](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L112) | Bug3600 | yes |
| [test/Npgsql.Tests/BugTests.cs:133](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L133) | Bug1497 | yes |
| [test/Npgsql.Tests/BugTests.cs:145](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L145) | Bug1558 | yes |
| [test/Npgsql.Tests/BugTests.cs:157](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L157) | Bug1695 | yes |
| [test/Npgsql.Tests/BugTests.cs:177](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L177) | Bug1700 | yes |
| [test/Npgsql.Tests/BugTests.cs:202](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L202) | Bug1964 | yes |
| [test/Npgsql.Tests/BugTests.cs:212](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L212) | Bug1986 | yes |
| [test/Npgsql.Tests/BugTests.cs:229](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L229) | Bug1987 | yes |
| [test/Npgsql.Tests/BugTests.cs:251](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L251) | Bug2003 | yes |
| [test/Npgsql.Tests/BugTests.cs:264](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L264) | Bug2046 | yes |
| [test/Npgsql.Tests/BugTests.cs:278](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L278) | Bug1761 | yes |
| [test/Npgsql.Tests/BugTests.cs:315](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L315) | Bug2274 | yes |
| [test/Npgsql.Tests/BugTests.cs:332](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L332) | Bug2278 | yes |
| [test/Npgsql.Tests/BugTests.cs:367](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L367) | Bug2178 | yes |
| [test/Npgsql.Tests/BugTests.cs:396](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L396) | Bug2296 | yes |
| [test/Npgsql.Tests/BugTests.cs:410](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L410) | Standard_conforming_strings | yes |
| [test/Npgsql.Tests/BugTests.cs:429](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L429) | Bug1285 | yes |
| [test/Npgsql.Tests/BugTests.cs:1089](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1089) | Chunked_string_write_buffer_encoding_space | yes |
| [test/Npgsql.Tests/BugTests.cs:1115](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1115) | Chunked_char_array_write_buffer_encoding_space | yes |
| [test/Npgsql.Tests/BugTests.cs:1141](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1141) | NRE_in_BeginTextExport | yes |
| [test/Npgsql.Tests/BugTests.cs:1171](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1171) | CompositePostgresType | yes |
| [test/Npgsql.Tests/BugTests.cs:1198](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1198) | Bug3117 | yes |
| [test/Npgsql.Tests/BugTests.cs:1224](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1224) | Bug3209 | yes |
| [test/Npgsql.Tests/BugTests.cs:1234](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1234) | Bug3373 | yes |
| [test/Npgsql.Tests/BugTests.cs:1246](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1246) | Bug3649 | yes |
| [test/Npgsql.Tests/BugTests.cs:1276](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1276) | UIThreadSynchronizationContext_deadlock | yes |
| [test/Npgsql.Tests/BugTests.cs:1297](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1297) | Bug3924 | yes |
| [test/Npgsql.Tests/BugTests.cs:1338](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1338) | Bug4123 | yes |
| [test/Npgsql.Tests/BugTests.cs:1352](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1352) | Composite_with_BigInteger | yes |
| [test/Npgsql.Tests/CopyTests.cs:25](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L25) | Issue2257 | yes |
| [test/Npgsql.Tests/CopyTests.cs:62](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L62) | Raw_binary_roundtrip | yes |
| [test/Npgsql.Tests/CopyTests.cs:123](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L123) | Dispose_in_middle_of_raw_binary_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:142](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L142) | Dispose_in_middle_of_raw_binary_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:158](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L158) | Cancel_raw_binary_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:176](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L176) | Import_large_value_raw | yes |
| [test/Npgsql.Tests/CopyTests.cs:215](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L215) | Wrong_table_definition_raw_binary_copy | yes |
| [test/Npgsql.Tests/CopyTests.cs:228](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L228) | Wrong_format_raw_binary_copy | yes |
| [test/Npgsql.Tests/CopyTests.cs:250](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L250) | Binary_roundtrip | yes |
| [test/Npgsql.Tests/CopyTests.cs:307](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L307) | Cancel_binary_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:325](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L325) | Import_bytea | yes |
| [test/Npgsql.Tests/CopyTests.cs:344](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L344) | Import_numeric | yes |
| [test/Npgsql.Tests/CopyTests.cs:370](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L370) | Import_string_array | yes |
| [test/Npgsql.Tests/CopyTests.cs:388](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L388) | Import_DBNull_then_other_object | yes |
| [test/Npgsql.Tests/CopyTests.cs:408](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L408) | Import_reused_instance_mapping_info_identical_or_throws | yes |
| [test/Npgsql.Tests/CopyTests.cs:428](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L428) | Import_string_with_buffer_length | yes |
| [test/Npgsql.Tests/CopyTests.cs:445](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L445) | Import_direct_buffer | yes |
| [test/Npgsql.Tests/CopyTests.cs:461](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L461) | Import_object_null | yes |
| [test/Npgsql.Tests/CopyTests.cs:484](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L484) | Import_dbnull | yes |
| [test/Npgsql.Tests/CopyTests.cs:501](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L501) | Wrong_table_definition_binary_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:511](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L511) | Wrong_format_binary_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:520](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L520) | Wrong_table_definition_binary_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:530](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L530) | MixedOperations | yes |
| [test/Npgsql.Tests/CopyTests.cs:553](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L553) | ReadMoreColumnsThanExist | yes |
| [test/Npgsql.Tests/CopyTests.cs:578](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L578) | ReadZeroSizedColumns | yes |
| [test/Npgsql.Tests/CopyTests.cs:608](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L608) | ReadTypeInfoProviderType | yes |
| [test/Npgsql.Tests/CopyTests.cs:642](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L642) | StreamingRead | yes |
| [test/Npgsql.Tests/CopyTests.cs:655](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L655) | Wrong_format_binary_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:664](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L664) | Unexpected_exception_binary_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:690](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L690) | Import_bytea_massive | yes |
| [test/Npgsql.Tests/CopyTests.cs:713](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L713) | Export_long_string | yes |
| [test/Npgsql.Tests/CopyTests.cs:745](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L745) | Read_bit_string | yes |
| [test/Npgsql.Tests/CopyTests.cs:767](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L767) | Array | yes |
| [test/Npgsql.Tests/CopyTests.cs:790](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L790) | Enum | yes |
| [test/Npgsql.Tests/CopyTests.cs:823](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L823) | Read_null_as_nullable | yes |
| [test/Npgsql.Tests/CopyTests.cs:834](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L834) | Read_null_as_non_nullable_throws | yes |
| [test/Npgsql.Tests/CopyTests.cs:845](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L845) | Error_during_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:861](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L861) | Import_cannot_write_after_commit | yes |
| [test/Npgsql.Tests/CopyTests.cs:882](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L882) | Import_commit_in_middle_of_row | yes |
| [test/Npgsql.Tests/CopyTests.cs:905](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L905) | Import_exception_does_not_commit | yes |
| [test/Npgsql.Tests/CopyTests.cs:924](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L924) | Write_column_out_of_bounds_throws | yes |
| [test/Npgsql.Tests/CopyTests.cs:953](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L953) | Cancel_raw_binary_export_when_not_consumed_and_then_Dispose | yes |
| [test/Npgsql.Tests/CopyTests.cs:969](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L969) | Cancel_binary_export_when_not_consumed_and_then_Dispose | yes |
| [test/Npgsql.Tests/CopyTests.cs:986](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L986) | Binary_copy_read_char_column | yes |
| [test/Npgsql.Tests/CopyTests.cs:1008](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1008) | Text_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:1037](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1037) | Cancel_text_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:1051](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1051) | Text_import_empty | yes |
| [test/Npgsql.Tests/CopyTests.cs:1063](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1063) | Text_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:1089](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1089) | Dispose_in_middle_of_text_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:1104](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1104) | Wrong_table_definition_text_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:1113](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1113) | Wrong_format_text_import | yes |
| [test/Npgsql.Tests/CopyTests.cs:1122](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1122) | Wrong_table_definition_text_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:1131](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1131) | Wrong_format_text_export | yes |
| [test/Npgsql.Tests/CopyTests.cs:1140](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1140) | Cancel_text_export_when_not_consumed_and_then_Dispose | yes |
| [test/Npgsql.Tests/CopyTests.cs:1160](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L1160) | Prepended_messages | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-021-F01-01 | WP-01 | Truncated/oversized frames fail without unbounded allocation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F01-02 | WP-01 | SCRAM vectors pass | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F01-03 | WP-01 | credentials never enter trace output | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F02-01 | WP-02 | Error recovery reaches a valid sync boundary | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F02-02 | WP-02 | cancel affects only its backend session | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F02-03 | WP-02 | lost commit response remains an unknown outcome | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F03-01 | WP-03 | Boundary values round trip | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F03-02 | WP-03 | unknown OIDs return an explicit unsupported type | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F03-03 | WP-03 | no decimal precision is silently truncated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F04-01 | WP-04 | Session variables do not leak between leases | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F04-02 | WP-04 | interrupted COPY does not return a dirty connector | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F04-03 | WP-04 | ambiguous operations are not replayed silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F05-01 | WP-05 | COPY cancellation restores or discards connection safely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F05-02 | WP-05 | notification queues are bounded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F05-03 | WP-05 | replication acknowledgments never exceed durably processed position | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F06-01 | WP-06 | JDBC unsupported operations raise explicit standard failures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F06-02 | WP-06 | advertised metadata matches tests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-021-F06-03 | WP-06 | no existing PostgreSQL JDBC driver supplies the implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

SCRAM and TLS; extended query state; cancel keys; COPY; binary types; timezone/numeric boundaries; failover and pool reset.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-021-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-021-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-021-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
