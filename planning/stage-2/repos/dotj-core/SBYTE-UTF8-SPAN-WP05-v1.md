# Selected SByte UTF-8 span formatting

Batch 2139 adds IUtf8SpanFormattable and byte-array/typed UTF-8 buffer routes. Short buffers return false with zero written and preserve storage. Offset views preserve surrounding bytes. Formats are validated before writes; invalid formats retain the previous out-slot value. Unicode numeric symbols use UTF-8 byte lengths.

Pinned CoreLib 10.0.12 records 2,457 buffer cases across fourteen signed-byte anchors, seventeen formats and invariant/Unicode number providers. Packaged consumers exercise 9,829 groups through raw arrays, interface dispatch and two offset views. The existing character-span corpus continues to pass; its Byte-format mismatch remains a compile rejection.

Java erases Span<Character> and Span<Byte> to the same signature. One generic destination method delegates to the checked Char/Byte heap-view carrier; the format remains a character span. This is an explicit Java bridge, with CLR byref lifetimes and native generic interface arity still open. Other numeric APIs, formats/cultures, task acceptance and release qualification remain open. The product remains JDK-only; validation tools and intermediate artifacts stay on D:.
