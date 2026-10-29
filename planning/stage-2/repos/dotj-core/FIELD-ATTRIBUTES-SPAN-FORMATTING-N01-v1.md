# FieldAttributes span formatting

Batch 2446: 12480 native/Java calls compare 112320 exact result/error/written/buffer/format/provider groups. Thirteen values, twelve format profiles, eight capacities, five array/slice/alias layouts and two providers exercise the array adapter and typed Char Span projection against emitted native ISpanFormattable calls. Insufficient capacity writes zero and preserves buffers; invalid formats preserve the initial written holder and buffers. Format/destination overlap is compared byte-for-byte at UTF16 code-unit level. Providers are never queried.

12480 pinned native calls and 12480 Java facade calls pass 112320 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The candidate JAR is byte-identical to the preceding enum conversion qualification. Fresh packaging, API and retained reflection checks are required; the full 461-check canonical gate remains required before merge.

Selected Char Span and array-adapter formatting only; complete Enum ABI, caller-owned invalid Java holders, UTF8 enum formatting and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Implement and qualify FieldInfo.SetValue rejection for selected literal fields with native FieldAccessException behavior and unchanged field values.

## Supporting validation tooling

The reference-source digest check now streams the full archive through a 256 KiB buffer in 188 existing/current verifiers. Every byte is still checked against the unchanged pinned SHA-256 on every invocation; there is no digest cache. Exact preimage hashes, inverse byte comparisons and independent AST comparisons preserve all other expressions, source assertions and error checks. The deployed helper passes14 boundary/error/import cases, and eight actual verifiers pass16 isolated CLI/import checks. The helper hash and baseline source commit are bound in oracle-streaming-hash-validation-v1.json. The full461-check canonical gate remains required before merge.

This changes development tooling only. No extra numbered batch or acceptance task is credited, no whole-process memory or whole-gate speedup is claimed, and54 new prepared verifiers in2447-2500 remain unmigrated.
