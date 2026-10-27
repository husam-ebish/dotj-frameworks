# Integer digit and whitespace grammar

Batch 2350: Nine decimal/general/hex/binary styles cover all six accepted ASCII whitespace characters and Unicode whitespace controls, Arabic/Indic/fullwidth/supplementary digits, hexadecimal letter case, radix prefix rejection and terminal versus embedded NUL. String/Char/UTF8 Parse/TryParse use sliced views and primitive/boxed byte spans.

79920 pinned native calls and 106560 Java facade calls pass 213120 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the preceding parser qualification. Existing packaged/API evidence remains applicable; the full 365-check canonical gate remains required before merge.

Selected digit/whitespace inputs only; all cultures/full grammar/ABI and task acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify every valid NumberStyles value with representative nonzero, fractional, signed and range-boundary inputs for all four small integer types across String/Char/UTF8.
