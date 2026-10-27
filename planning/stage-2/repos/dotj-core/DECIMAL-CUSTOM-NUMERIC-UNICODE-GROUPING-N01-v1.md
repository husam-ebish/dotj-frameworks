# Decimal custom numeric Unicode grouping

Batch 2369: Sixteen exact Decimal bit states, twenty-three custom formats and eight group-size/separator profiles cover inline literals, padded digits, fractional coefficients, terminal zero/empty groups, malformed UTF16 and supplementary separators. Complete ToString and Char/UTF8 buffer results, provider callbacks, immutable bits and capacity boundaries match the pinned runtime.

59088 pinned native calls and 59088 Java facade calls pass 233408 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the preceding Decimal section candidate; packaged/API evidence remains applicable; the full 384-check canonical gate remains required before merge.

Selected custom numeric grouping only; scaling/exponent interactions, full grammar/cultures/ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify exact Decimal comma, percent and per-mille scaling with midpoint rounding, 96-bit coefficients, scale-28 tiny values and zero-section transitions.
