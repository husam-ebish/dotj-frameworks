# Decimal custom token termination

Batch 2377: Thirty-four exact Decimal bit states and thirty token-boundary formats cover dangling escapes, unclosed quotes, repeated decimal markers, decimal-only bodies, scientific/scaling combinations, extra sections, NUL termination and malformed UTF16 literals. All ToString and Char/UTF8 destination/callback/immutable-bit comparisons match native.

18906 pinned native calls and 18906 Java facade calls pass 74604 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the shared token termination candidate; its fresh packaged/API/retained evidence remains applicable; the full 392-check canonical gate remains required before merge.

Selected token/section boundaries only; multiple exponent markers, full grammar/cultures/ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Implement and qualify custom formats with multiple exponent markers: native emits only the first scientific exponent and preserves later marker/sign/zero runs as literals.
