# Selected NumberStyles comparison and equality

Batch 2092 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

NumberStyles implements selected IComparable comparison, capitalized Equals(Object)/GetHashCode and Java equality/hash adapters. The same carrier compares in signed Int32 order; null compares lower than any instance; other types throw ArgumentException with no parameter name. Equality requires the exact enum carrier and numeric value. Hashes use the underlying Int32 value. JDK Integer operations are qualified to avoid the native Integer flag field collision.

The pinned CoreLib 10.0.12 reference records 31 hashes and 1395 cases, combining all native named values with signed anchors, same-type values, null, scalar boxes, strings, plain objects and five foreign enum types. All 5643 packaged groups pass across direct/interface comparison, capitalized/Java equality/hash and selected IComparable/IFormattable metadata. Earlier formatting checks and the foundation audit are updated for the expanded interface profile, retaining the nineteen named-field checks and requiring comparison/equality/hash signatures. The API preview passes.

IConvertible and ISpanFormattable remain explicitly omitted. Inherited CLR Enum contracts are projected onto the Java immutable carrier; physical enum/boxing identity, other Enum APIs, full messages, language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only; validation files and caches stay on D:.
