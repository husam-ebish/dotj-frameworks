# Decimal CreateTruncating floating carriers

Batch 2387: 1230 raw IEEE Single/Double cases cover exponent/fraction boundaries, signed zeros, NaN payloads, infinities, subnormals, midpoint-adjacent values and deterministic samples. All 2460 bit-result/input-immutability groups match native truncating creation. Native behavior matches the shared saturation implementation, including exact NaN zero scale.

1230 pinned native calls and 1230 Java facade calls pass 2460 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the preceding truncating-creation candidate. Its fresh packaged/API and retained evidence remains applicable; the full 402-check canonical gate remains required before merge.

Selected owned/JDK numeric carriers only; Half identity, custom INumberBase dispatch, CLR generic constraints/ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Implement and qualify selected Char/Byte/Int32 Span element reads and writes through array-backed views, including aliasing, bounds, full-buffer preservation and explicit ref-return adaptation limits.
