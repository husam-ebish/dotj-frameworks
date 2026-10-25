# Selected UInt16 comparison, equality and hashing

Batch 2135 advances DJ-001-WP-05-T1 without implementation acceptance credit.

UInt16 adds direct typed/object CompareTo and Equals methods, GetHashCode, Java equality/hash adapters and the selected non-generic IComparable projection. Comparisons preserve native arithmetic differences, including -65535/65535, rather than only a normalized sign. Null compares lower than a UInt16 object; other object types throw ArgumentException without a parameter name. Equality requires a UInt16 carrier with the same unsigned value; hashes preserve values 0 through 65535. A null typed Java carrier is outside the native value-parameter domain and is rejected with ArgumentNullException(value).

The pinned CoreLib 10.0.12 reference captures 267 selected UInt16 hashes and 989 target pairs across 23 boundary/anchor values, same-type inputs, null, scalar boxes, strings, objects and foreign enums. Packaged consumers verify 5,549 groups through typed, object, interface and Java routes. Type and the preceding formatting consumer are updated for the selected IComparable/IConvertible/IFormattable profile.

Generic IComparable<UInt16>/IEquatable<UInt16> interface arity, other numeric APIs, CLR boxing/value identity and full qualification remain open. The product remains JDK-only; validation tools and intermediate artifacts stay on D:.
