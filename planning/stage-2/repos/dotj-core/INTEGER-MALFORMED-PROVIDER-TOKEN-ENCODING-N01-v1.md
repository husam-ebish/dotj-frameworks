# Integer malformed provider token encoding

Batch 2353: Fifty-six profiles combine seven sign/separator/currency fields with isolated and repeated surrogates, valid pairs, reversed pairs and NUL suffixes. Six styles exercise String/Char/UTF8 Parse/TryParse with original UTF-16 units and independent JDK UTF8 replacement configured to U+FFFD. Question-mark and replacement-character input controls expose accidental default JDK replacement differences.

131040 pinned native calls and 174720 Java facade calls pass 349440 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to the preceding parser qualification. Existing packaged/API evidence remains applicable; the full 368-check canonical gate remains required before merge.

Selected malformed provider tokens only; full cultures/grammar/ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify provider callback count, failure identity and destination/holder mutation boundaries for integer ToString and Char/UTF8 TryFormat.
