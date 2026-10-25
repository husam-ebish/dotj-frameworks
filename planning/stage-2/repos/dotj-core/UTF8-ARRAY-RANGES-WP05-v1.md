# Selected UTF-8 array slices

Batch 2165 adds seven selected String/Char[]/Byte[] range overloads to Encoding. They preserve native null-first validation, negative index before negative count, overflow-safe remaining-length checks and overload-specific parameter identity. String range overflow names index; character and byte array overflow name the corresponding source array. Strict fallback indexes are relative to the selected slice.

Pinned CoreLib records 12,370 strict/replacement cases across twelve UTF-16 and twenty byte-array inputs, null sources, split surrogate/multibyte sequences, negative and maximum Int32 boundaries. The packaged consumer checks conversion/failure metadata and unchanged input arrays for 24,740 groups. The packaged product build and its independent consumers also pass with the new UTF-8 class inventory.

This is selected stateless slice conversion. Whole-character-array convenience methods, destination buffers, span/pointer overloads, stateful conversion, custom fallback objects, logical type lookup, native source/CLR ABI and WP-05-T2 acceptance remain open. No framework qualification or implementation-task completion is credited. The next concrete task is native destination-buffer mutation and capacity behavior.
