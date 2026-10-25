# Selected small-integer range fields

Batch 2147 adds public static final MinValue/MaxValue fields to SByte, Byte, UInt16 and UInt32. Java int fields represent the first three ranges; Java long fields represent UInt32 values 0 through 4294967295. These are explicit primitive-width adapters for native value-type fields, following the existing Int32 carrier convention.

Pinned CoreLib 10.0.12 supplies eight native constants and 24 checked conversion boundary cases: just outside each end, both ends and adjacent interior values. Consumers verify compiled/public/final field widths and reflection values, valid constructor values/text, and OverflowException identity/HResult outside each range. The signature inventory also records the newly present field names.

This bounded change does not establish CLR field ABI, complete numeric APIs, implementation-task acceptance or release qualification. Runtime dependencies remain JDK-only; validation tools and intermediate artifacts remain on D:.
