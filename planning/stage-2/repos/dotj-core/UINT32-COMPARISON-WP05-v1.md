# Selected UInt32 comparison, equality and hashing

Batch 2137 advances DJ-001-WP-05-T1 without implementation acceptance credit.

UInt32 adds typed/object CompareTo and Equals methods, GetHashCode, Java equality/hash adapters and the selected non-generic IComparable projection. Comparisons return native -1/0/1 ordering over unsigned values held in Java longs; hashing preserves the native low 32-bit signed result. Null compares lower than an instance; other object types throw ArgumentException without a parameter name. Equality requires the same UInt32 carrier/value. A null typed Java carrier remains an adapter-domain error outside the CLR value parameter.

The pinned CoreLib 10.0.12 corpus records 266 selected hashes and 989 target pairs across 23 anchors, including Int32 boundary neighbors and UInt32 maximum. The packaged consumer checks 5,547 groups through typed, object, interface and Java routes. The preceding formatting consumer and Type projection are updated for the selected IComparable/IConvertible/IFormattable profile.

Generic interface arity, other numeric APIs, CLR value/boxing identity and complete qualification remain open. Product runtime dependencies remain JDK-only; validation tools and intermediate artifacts stay on D:.
