# Small-integer declared signature inventory

Batch 2146 compares four selected Java carriers with hash-pinned CoreLib 10.0.12 declared metadata. SByte has 52 declared methods, Byte and UInt16 each have 46, and UInt32 has 47. Twelve selected methods per type have projected Java declarations: formatting, comparison, equality, hashing, type code and Char/UTF-8 TryFormat routes. Four generic Span<T> bridges cover the typed Char/Byte erasure boundary.

The remaining 143 declared methods are outside this selected projection audit. Extra Java methods and native fields are explicitly inventoried. Initially all eight native MinValue/MaxValue names are absent from the carriers. The next change implements those fields with documented Java primitive widths and verifies the native values and constructor boundaries.

This audit checks declaration shapes and preserves native evidence provenance. It does not establish behavior parity, native generic interfaces, value-type ABI, byref lifetimes, implementation-task acceptance or release qualification. Candidate runtime dependencies remain JDK-only; validation uses the pinned development tools on D:.
