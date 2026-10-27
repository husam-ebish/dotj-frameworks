# Integer currency token precedence

Batch 2349: Sixteen selected custom NumberFormatInfo profiles cover currency/sign/separator token collisions, leading versus trailing symbol separator fallback, embedded NUL currency tokens, Unicode whitespace tokens and NumberNegativePattern 1 versus 2. Four currency style masks run String/Char/UTF8 Parse/TryParse and primitive/boxed byte spans.

36000 pinned native calls and 48000 Java facade calls pass 96000 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the preceding parser qualification. Existing packaged/API evidence remains applicable; the full 364-check canonical gate remains required before merge.

Selected currency profiles only; full cultures/grammar/ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify integer non-ASCII digit rejection, ASCII versus Unicode whitespace, embedded NUL and radix digit grammar across String/Char/UTF8 routes.
