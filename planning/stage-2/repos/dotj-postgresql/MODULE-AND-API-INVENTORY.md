# DJ-021 .j PostgreSQL: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 542 | recursive complete |
| Project-definition paths | 12 | Files, not restored packages |
| API-definition/ref paths | 10 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 141 | Lexical path classification, not runnable test count |
| Sampled text files | 15 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 109 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 99 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Npgsql.Json.NET/Npgsql.Json.NET.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/Npgsql.Json.NET.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Npgsql.NetTopologySuite/Npgsql.NetTopologySuite.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.NetTopologySuite/Npgsql.NetTopologySuite.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Npgsql.NodaTime/Npgsql.NodaTime.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.NodaTime/Npgsql.NodaTime.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Npgsql.OpenTelemetry/Npgsql.OpenTelemetry.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.OpenTelemetry/Npgsql.OpenTelemetry.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Npgsql.SourceGenerators/Npgsql.SourceGenerators.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.SourceGenerators/Npgsql.SourceGenerators.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/MStatDumper/MStatDumper.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/MStatDumper/MStatDumper.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Npgsql.Benchmarks/Npgsql.Benchmarks.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Benchmarks/Npgsql.Benchmarks.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Npgsql.NativeAotTests/Npgsql.NativeAotTests.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.NativeAotTests/Npgsql.NativeAotTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Npgsql.Specification.Tests/Npgsql.Specification.Tests.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Specification.Tests/Npgsql.Specification.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Npgsql.Tests/Npgsql.Tests.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/Npgsql.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Npgsql/Common.cs:65](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Common.cs#L65) | `public enum StatementType` |
| [src/Npgsql/PgPassFile.cs:28](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/PgPassFile.cs#L28) | `public PgPassFile(string fileName)` |
| [test/Npgsql.Tests/BugTests.cs:17](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L17) | `public class BugTests : TestBase` |
| [test/Npgsql.Tests/BugTests.cs:24](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L24) | `public void SequentialNullCheckOnNonFirstField()` |
| [test/Npgsql.Tests/BugTests.cs:34](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L34) | `public void SequentialSkipOverFirstRow()` |
| [test/Npgsql.Tests/BugTests.cs:45](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L45) | `public void SequentialConsumeWithNull()` |
| [test/Npgsql.Tests/BugTests.cs:56](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L56) | `public void Many_parameters_with_mixed_FormatCode()` |
| [test/Npgsql.Tests/BugTests.cs:78](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L78) | `public void Bug1450()` |
| [test/Npgsql.Tests/BugTests.cs:91](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L91) | `public async Task Bug1645()` |
| [test/Npgsql.Tests/BugTests.cs:112](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L112) | `public async Task Bug3600()` |
| [test/Npgsql.Tests/BugTests.cs:133](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L133) | `public async Task Bug1497()` |
| [test/Npgsql.Tests/BugTests.cs:145](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L145) | `public void Bug1558()` |
| [test/Npgsql.Tests/BugTests.cs:157](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L157) | `public void Bug1695()` |
| [test/Npgsql.Tests/BugTests.cs:177](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L177) | `public void Bug1700()` |
| [test/Npgsql.Tests/BugTests.cs:202](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L202) | `public void Bug1964()` |
| [test/Npgsql.Tests/BugTests.cs:212](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L212) | `public void Bug1986()` |
| [test/Npgsql.Tests/BugTests.cs:229](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L229) | `public async Task Bug1987()` |
| [test/Npgsql.Tests/BugTests.cs:251](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L251) | `public void Bug2003()` |
| [test/Npgsql.Tests/BugTests.cs:264](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L264) | `public async Task Bug2046()` |
| [test/Npgsql.Tests/BugTests.cs:278](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L278) | `public void Bug1761()` |
| [test/Npgsql.Tests/BugTests.cs:315](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L315) | `public void Bug2274()` |
| [test/Npgsql.Tests/BugTests.cs:332](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L332) | `public async Task Bug2278()` |
| [test/Npgsql.Tests/BugTests.cs:355](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L355) | `public Bug2278EnumType Value { get; set; }` |
| [test/Npgsql.Tests/BugTests.cs:367](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L367) | `public async Task Bug2178()` |
| [test/Npgsql.Tests/BugTests.cs:396](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L396) | `public async Task Bug2296()` |
| [test/Npgsql.Tests/BugTests.cs:410](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L410) | `public void Standard_conforming_strings()` |
| [test/Npgsql.Tests/BugTests.cs:429](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L429) | `public void Bug1285()` |
| [test/Npgsql.Tests/BugTests.cs:1089](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1089) | `public async Task Chunked_string_write_buffer_encoding_space()` |
| [test/Npgsql.Tests/BugTests.cs:1115](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1115) | `public async Task Chunked_char_array_write_buffer_encoding_space()` |
| [test/Npgsql.Tests/BugTests.cs:1141](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1141) | `public async Task NRE_in_BeginTextExport()` |
| [test/Npgsql.Tests/BugTests.cs:1154](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1154) | `public enum TestEnum` |
| [test/Npgsql.Tests/BugTests.cs:1165](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1165) | `public TestEnum Test { get; set; }` |
| [test/Npgsql.Tests/BugTests.cs:1166](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1166) | `public int X { get; set; }` |
| [test/Npgsql.Tests/BugTests.cs:1167](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1167) | `public string SomeText { get; set; } = "";` |
| [test/Npgsql.Tests/BugTests.cs:1171](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1171) | `public async Task CompositePostgresType()` |
| [test/Npgsql.Tests/BugTests.cs:1198](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1198) | `public void Bug3117()` |
| [test/Npgsql.Tests/BugTests.cs:1224](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1224) | `public async Task Bug3209()` |
| [test/Npgsql.Tests/BugTests.cs:1234](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1234) | `public async Task Bug3373()` |
| [test/Npgsql.Tests/BugTests.cs:1246](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1246) | `public async Task Bug3649()` |
| [test/Npgsql.Tests/BugTests.cs:1276](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1276) | `public async Task UIThreadSynchronizationContext_deadlock()` |
| [test/Npgsql.Tests/BugTests.cs:1297](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1297) | `public async Task Bug3924()` |
| [test/Npgsql.Tests/BugTests.cs:1338](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1338) | `public async Task Bug4123()` |
| [test/Npgsql.Tests/BugTests.cs:1352](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1352) | `public async Task Composite_with_BigInteger([Values(CommandBehavior.Default, CommandBehavior.SequentialAccess)] CommandBehavior behavior)` |
| [test/Npgsql.Tests/BugTests.cs:1374](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs#L1374) | `public BigInteger Value { get; set; }` |
| [test/Npgsql.Tests/CopyTests.cs:20](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L20) | `public class CopyTests : TestBase` |
| [test/Npgsql.Tests/CopyTests.cs:25](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L25) | `public async Task Issue2257()` |
| [test/Npgsql.Tests/CopyTests.cs:62](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L62) | `public async Task Raw_binary_roundtrip([Values(false, true)] bool async)` |
| [test/Npgsql.Tests/CopyTests.cs:123](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L123) | `public async Task Dispose_in_middle_of_raw_binary_export()` |
| [test/Npgsql.Tests/CopyTests.cs:142](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L142) | `public async Task Dispose_in_middle_of_raw_binary_import()` |
| [test/Npgsql.Tests/CopyTests.cs:158](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L158) | `public async Task Cancel_raw_binary_import()` |
| [test/Npgsql.Tests/CopyTests.cs:176](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L176) | `public async Task Import_large_value_raw()` |
| [test/Npgsql.Tests/CopyTests.cs:215](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L215) | `public async Task Wrong_table_definition_raw_binary_copy()` |
| [test/Npgsql.Tests/CopyTests.cs:228](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L228) | `public async Task Wrong_format_raw_binary_copy()` |
| [test/Npgsql.Tests/CopyTests.cs:250](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L250) | `public async Task Binary_roundtrip([Values(false, true)] bool async)` |
| [test/Npgsql.Tests/CopyTests.cs:307](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L307) | `public async Task Cancel_binary_import()` |
| [test/Npgsql.Tests/CopyTests.cs:325](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L325) | `public async Task Import_bytea()` |
| [test/Npgsql.Tests/CopyTests.cs:344](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L344) | `public async Task Import_numeric()` |
| [test/Npgsql.Tests/CopyTests.cs:370](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L370) | `public async Task Import_string_array()` |
| [test/Npgsql.Tests/CopyTests.cs:388](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L388) | `public async Task Import_DBNull_then_other_object()` |
| [test/Npgsql.Tests/CopyTests.cs:408](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L408) | `public async Task Import_reused_instance_mapping_info_identical_or_throws()` |
| [test/Npgsql.Tests/CopyTests.cs:428](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L428) | `public async Task Import_string_with_buffer_length()` |
| [test/Npgsql.Tests/CopyTests.cs:445](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L445) | `public async Task Import_direct_buffer()` |
| [test/Npgsql.Tests/CopyTests.cs:461](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L461) | `public async Task Import_object_null()` |
| [test/Npgsql.Tests/CopyTests.cs:484](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L484) | `public async Task Import_dbnull(DBNull? value)` |
| [test/Npgsql.Tests/CopyTests.cs:501](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L501) | `public async Task Wrong_table_definition_binary_import()` |
| [test/Npgsql.Tests/CopyTests.cs:511](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L511) | `public async Task Wrong_format_binary_import()` |
| [test/Npgsql.Tests/CopyTests.cs:520](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L520) | `public async Task Wrong_table_definition_binary_export()` |
| [test/Npgsql.Tests/CopyTests.cs:530](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L530) | `public async Task MixedOperations()` |
| [test/Npgsql.Tests/CopyTests.cs:553](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L553) | `public async Task ReadMoreColumnsThanExist()` |
| [test/Npgsql.Tests/CopyTests.cs:578](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs#L578) | `public async Task ReadZeroSizedColumns()` |

Full lexical records (109) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Wire framing startup and authentication | PgMessage; SessionState; AuthenticationExchange |
| WP-02 | Simple extended queries and cancellation | QueryCycle; Portal; PreparedStatement; CancelKey |
| WP-03 | Type codecs and PostgreSQL semantics | PgTypeId; TextCodec; BinaryCodec; TypeRegistry |
| WP-04 | Pooling multiplexing and failover | PoolLease; ConnectorState; HostPolicy |
| WP-05 | COPY notifications replication and large objects | CopySession; Notification; ReplicationPosition |
| WP-06 | JDBC facade and server compatibility | JdbcMethodMatrix; DatabaseMetaData; DriverCapability |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
