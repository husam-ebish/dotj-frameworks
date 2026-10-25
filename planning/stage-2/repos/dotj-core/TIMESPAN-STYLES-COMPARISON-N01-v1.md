# Selected TimeSpanStyles comparison and equality

Batch 2087 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

TimeSpanStyles implements selected IComparable comparison, capitalized Equals(Object) and GetHashCode contracts alongside Java equality/hash adapters. Comparison is signed Int32 order for the same carrier type, one for null, and native ArgumentException with no parameter name for other types. Equality requires the exact enum carrier and value. Hashes use the underlying Int32 value. Type exposes the supported IComparable/IFormattable profile, lookup, assignability, instance membership and defensive arrays.

The pinned CoreLib 10.0.12 reference records 22 hashes and 792 cases spanning signed endpoints, named/unknown/composite values, null, scalar boxes, strings, plain objects and five foreign enum types. All 3213 packaged groups pass through direct/interface comparison and capitalized/Java equality/hash routes. The earlier formatting verifier is updated for the expanded selected interface profile. javap verifies comparison, equality and hash signatures.

Native IConvertible and ISpanFormattable remain explicitly omitted. Physical CLR enum/boxing identity, other Enum APIs, complete messages, language integration, full framework acceptance and release qualification remain open. Product runtime dependencies remain JDK-only; validation intermediates and caches stay on D:.
