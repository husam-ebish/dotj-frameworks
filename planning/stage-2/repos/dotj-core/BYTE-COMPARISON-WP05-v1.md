# Selected Byte comparison, equality and hashing

Batch 2132 advances DJ-001-WP-05-T1 without implementation acceptance credit.

Byte adds direct typed/object CompareTo and Equals methods, GetHashCode, Java equality/hash adapters and the selected non-generic IComparable projection. Comparisons preserve native arithmetic differences, including -255/255, rather than only a normalized sign. Null compares lower than a Byte object; other object types throw ArgumentException without a parameter name. Equality requires a Byte carrier with the same unsigned value; hashes preserve values 0 through 255. A null typed Java carrier is outside the native value-parameter domain and is rejected with ArgumentNullException(value).

The pinned CoreLib 10.0.12 reference captures every byte hash and 989 target pairs across 23 boundary/anchor values, same-type inputs, null, scalar boxes, strings, objects and foreign enums. Packaged consumers verify 5,527 groups through typed, object, interface and Java routes. Type and the preceding formatting consumer are updated for the selected IComparable/IConvertible/IFormattable profile.

Generic IComparable<Byte>/IEquatable<Byte> interface arity, other numeric APIs, CLR boxing/value identity and full qualification remain open. The product remains JDK-only; validation tools and intermediate artifacts stay on D:.
