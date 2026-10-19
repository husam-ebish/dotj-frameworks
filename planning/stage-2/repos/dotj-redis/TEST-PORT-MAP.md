# DJ-022 .j Redis: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/RESPite.Tests/RespReaderTests.cs:138](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L138) | HandleSplitTokens | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:150](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L150) | BlobString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:168](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L168) | EmptyBlobString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:178](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L178) | SimpleString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:190](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L190) | SimpleError_ImplicitErrors | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:201](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L201) | SimpleError_Careful | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:212](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L212) | Number | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:233](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L233) | Null | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:243](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L243) | NullString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:260](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L260) | Double | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:272](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L272) | Integer_Simple | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:285](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L285) | Double_Simple | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:298](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L298) | Double_Infinity | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:311](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L311) | Double_PosInfinity | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:324](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L324) | Double_NegInfinity | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:337](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L337) | Double_NaN | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:349](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L349) | Boolean_T | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:358](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L358) | Boolean_F | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:367](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L367) | Boolean_1 | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:376](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L376) | Boolean_0 | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:385](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L385) | BlobError_ImplicitErrors | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:396](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L396) | BlobError_Careful | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:407](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L407) | VerbatimString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:421](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L421) | BigIntegers | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:435](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L435) | Array | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:476](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L476) | NullArray | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:489](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L489) | NestedArray | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:526](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L526) | Map | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:558](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L558) | Set | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:631](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L631) | AttributeRoot | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:679](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L679) | AttributeInner | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:735](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L735) | Push | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:761](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L761) | PushThenGetReply | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:790](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L790) | GetReplyThenPush | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:821](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L821) | ArrayThenString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:846](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L846) | ScalarLengthIs_NullBulkString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:858](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L858) | ScalarLengthIs_Empty | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:869](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L869) | ScalarLengthIs_Simple | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:882](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L882) | ScalarLengthIs_Streaming | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:896](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L896) | ScalarLengthIs_Streaming_ShortCircuits | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:915](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L915) | StreamingScalar_BufferPartial | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:933](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L933) | ScalarLengthIs_SimpleString | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:945](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L945) | AggregateLengthIs_NullArray | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:955](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L955) | AggregateLengthIs_Empty | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:967](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L967) | AggregateLengthIs_Simple | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:981](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L981) | AggregateLengthIs_Streaming | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:995](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L995) | AggregateLengthIs_Streaming_ShortCircuits | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:1015](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L1015) | AggregateLengthIs_Streaming_MalformedAfterShortCircuit | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:1033](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L1033) | AggregateLengthIs_Map | yes |
| [tests/RESPite.Tests/RespReaderTests.cs:1048](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs#L1048) | AggregateLengthIs_Set | yes |
| [tests/RESPite.Tests/CycleBufferTests.cs:12](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/CycleBufferTests.cs#L12) | WriteMultiSegmentSequence_WritesEverySegment | yes |
| [tests/RESPite.Tests/CycleBufferTests.cs:50](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/CycleBufferTests.cs#L50) | SetNext | not confirmed |
| [tests/RESPite.Tests/CycleBufferTests.cs:62](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/CycleBufferTests.cs#L62) | CanDiscardSafely | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-022-F01-01 | WP-01 | Fragmented frames decode identically | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F01-02 | WP-01 | oversized replies fail safely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F01-03 | WP-01 | unknown commands cannot inherit unsafe retry assumptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F02-01 | WP-02 | Disconnect cannot associate old replies with a new connection | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F02-02 | WP-02 | non-idempotent ambiguous writes are not silently replayed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F02-03 | WP-02 | pending futures settle | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F03-01 | WP-03 | ASK does not permanently rewrite ownership | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F03-02 | WP-03 | redirect loops are bounded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F03-03 | WP-03 | stale topology cannot route cross-slot transactions silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F04-01 | WP-04 | Aborted transactions remain distinguishable from empty results | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F04-02 | WP-04 | reconnect resubscription is documented | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F04-03 | WP-04 | slow consumers have bounded queues | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F05-01 | WP-05 | Every claimed command has routing/codec fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F05-02 | WP-05 | unavailable server features return explicit errors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-022-F05-03 | WP-05 | diagnostics redact authentication material | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

RESP null/empty distinctions; cluster MOVED/ASK; disconnect mid-command; pubsub resubscribe; blocking-command isolation.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-022-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-022-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-022-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
