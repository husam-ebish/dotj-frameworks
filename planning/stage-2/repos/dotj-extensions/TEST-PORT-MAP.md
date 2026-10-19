# DJ-006 .j Extensions: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Shared/Pools/PoolTests.cs:54](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L54) | Basic | yes |
| [test/Shared/Pools/PoolTests.cs:89](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L89) | Resettable | yes |
| [test/Shared/Pools/PoolTests.cs:102](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L102) | RespectPolicy | yes |
| [test/Shared/Pools/PoolTests.cs:124](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L124) | SharedStringBuilderPool | yes |
| [test/Shared/Pools/PoolTests.cs:133](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L133) | StringBuilderPool | yes |
| [test/Shared/Pools/PoolTests.cs:147](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L147) | ListPool | yes |
| [test/Shared/Pools/PoolTests.cs:162](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L162) | DictionaryPool | yes |
| [test/Shared/Pools/PoolTests.cs:177](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L177) | HashSetPool | yes |
| [test/Shared/Pools/PoolTests.cs:192](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L192) | CancellationTokenSourcePool_NotTriggered | yes |
| [test/Shared/Pools/PoolTests.cs:208](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L208) | CancellationTokenSourcePool_Triggered | yes |
| [test/Shared/Pools/PoolTests.cs:221](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L221) | ArgChecks | yes |
| [test/Shared/Pools/PoolTests.cs:235](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L235) | Threading | yes |
| [test/Shared/Pools/PoolTests.cs:312](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs#L312) | NoopPolicy | yes |
| [test/Shared/Throw/LongTests.cs:16](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L16) | IfLongLessThan_ThrowWhenLessThan | yes |
| [test/Shared/Throw/LongTests.cs:24](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L24) | IfLongLessThan_DoesntThrow_WhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:31](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L31) | IfLongGreaterThan_ThrowWhenGreaterThan | yes |
| [test/Shared/Throw/LongTests.cs:39](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L39) | IfLongGreaterThan_DoesntThrow_WhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:46](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L46) | IfLongLessThanOrEqual_ThrowWhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:54](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L54) | IfLongLessThanOrEqual_DoesntThrow_WhenGreaterThan | yes |
| [test/Shared/Throw/LongTests.cs:61](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L61) | IfLongGreaterThanOrEqual_ThrowWhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:69](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L69) | IfLongGreaterThanOrEqual_DoesntThrow_WhenLessThan | yes |
| [test/Shared/Throw/LongTests.cs:76](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L76) | IfLongZero_ThrowWhenZero | yes |
| [test/Shared/Throw/LongTests.cs:84](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L84) | IfLongZero_DoesntThrow_WhenNotZero | yes |
| [test/Shared/Throw/LongTests.cs:91](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L91) | Long_OUtOfRange | yes |
| [test/Shared/Throw/LongTests.cs:106](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L106) | Shorter_Version_Of_GreaterThan_For_Long_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:119](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L119) | Shorter_Version_Of_GreaterThanOrEqual_For_Long_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:132](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L132) | Shorter_Version_Of_LessThan_For_Long_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:145](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L145) | Shorter_Version_Of_LessThanOrEqual_For_Long_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:158](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L158) | Shorter_Version_Of_Zero_For_Long_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:171](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L171) | Shorter_Version_Of_OutOfRange_For_Long_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:188](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L188) | IfULongLessThan_ThrowWhenLessThan | yes |
| [test/Shared/Throw/LongTests.cs:196](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L196) | IfULongLessThan_DoesntThrow_WhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:203](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L203) | IfULongGreaterThan_ThrowWhenGreaterThan | yes |
| [test/Shared/Throw/LongTests.cs:211](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L211) | IfULongGreaterThan_DoesntThrow_WhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:218](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L218) | IfULongLessThanOrEqual_ThrowWhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:226](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L226) | IfULongLessThanOrEqual_DoesntThrow_WhenGreaterThan | yes |
| [test/Shared/Throw/LongTests.cs:233](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L233) | IfULongGreaterThanOrEqual_ThrowWhenEqual | yes |
| [test/Shared/Throw/LongTests.cs:241](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L241) | IfULongGreaterThanOrEqual_DoesntThrow_WhenLessThan | yes |
| [test/Shared/Throw/LongTests.cs:248](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L248) | IfULongZero_ThrowWhenZero | yes |
| [test/Shared/Throw/LongTests.cs:256](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L256) | IfULongZero_DoesntThrow_WhenNotZero | yes |
| [test/Shared/Throw/LongTests.cs:263](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L263) | ULong_OutOfRange | yes |
| [test/Shared/Throw/LongTests.cs:278](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L278) | Shorter_Version_Of_GreaterThan_For_ULong_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:291](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L291) | Shorter_Version_Of_GreaterThanOrEqual_For_ULong_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:304](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L304) | Shorter_Version_Of_LessThan_For_ULong_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:317](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L317) | Shorter_Version_Of_LessThanOrEqual_For_ULong_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:330](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L330) | Shorter_Version_Of_Zero_For_ULong_Get_Correct_Argument_Name | yes |
| [test/Shared/Throw/LongTests.cs:343](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs#L343) | Shorter_Version_Of_OutOfRange_For_ULong_Get_Correct_Argument_Name | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-006-F01-01 | WP-01 | Every inspected package has exactly one owner | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F01-02 | WP-01 | core contracts never depend on richer adapters | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F01-03 | WP-01 | no namespace-based ownership shortcut is accepted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F02-01 | WP-02 | Refresh cannot publish half-built endpoint sets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F02-02 | WP-02 | retries never replay unsafe operations by default | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F02-03 | WP-02 | discovery failures follow declared stale-data policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F03-01 | WP-03 | Secrets are redacted before sinks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F03-02 | WP-03 | unbounded user labels are rejected or bounded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F03-03 | WP-03 | missing platform probes yield unknown rather than healthy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F03-04 | WP-03 | redaction never mutates the caller's object | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F04-01 | WP-04 | Mocked provider streams obey cancellation/backpressure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F04-02 | WP-04 | malformed tool arguments fail validation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F04-03 | WP-04 | ingestion preserves source/provenance | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F04-04 | WP-04 | no existing Java AI framework substitutes for these contracts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F05-01 | WP-05 | An application using only core APIs loads no AI/native/cloud code | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F05-02 | WP-05 | deterministic fake time drives retry/health tests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-006-F05-03 | WP-05 | adapter version conflicts are diagnosed before startup | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Configuration reload races; layered providers; service scope disposal; host shutdown; metrics cardinality.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
