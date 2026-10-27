# Decimal custom scientific formatting

Batch 2371: Thirty-four exact Decimal bit states and twenty-seven custom scientific formats cover significant-digit rounding, exponent normalization, signed padding, scale-28 coefficients, compound percent/comma scaling, zero sections and malformed selected literals. Complete ToString and four Char/UTF8 buffer routes match the pinned runtime.

19266 pinned native calls and 19266 Java facade calls pass 76146 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the preceding Decimal section candidate; packaged/API evidence remains applicable; the full 386-check canonical gate remains required before merge.

Selected single scientific exponent marker only; multiple markers, arbitrary grammar/cultures/ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify standard Decimal fixed/number/currency/percent/exponential/general/round-trip formatting at signed zero, fractional midpoint, scale-28, 96-bit and exponent carry boundaries.
