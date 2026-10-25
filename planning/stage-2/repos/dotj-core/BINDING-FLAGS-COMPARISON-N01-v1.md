# Selected BindingFlags inherited comparison contracts

Batch 2097 advances DJ-001-N01-T2; no implementation task or release gate is accepted.

BindingFlags maps inherited IComparable comparison, capitalized Equals(Object)/GetHashCode and Java equality/hash adapters. Same-carrier values compare in signed Int32 order; null compares lower than an instance; other types throw ArgumentException with no parameter name. Equality requires the exact carrier/value; hashes use the underlying Int32 value. Type projects the supported IComparable/IFormattable profile and corresponding lookup, assignability, instance and fresh-array behavior.

The pinned CoreLib 10.0.12 oracle records 34 hashes and 1632 cases, combining all named values with signed anchors, same-type values, null, scalar boxes, strings, objects and five foreign enum types. All 6597 packaged groups pass through direct/interface comparison and capitalized/Java equality/hash routes. Earlier formatting checks are updated for the expanded selected interface profile. javap verifies the selected signatures.

IConvertible and ISpanFormattable remain explicitly omitted. This inherited-contract mapping does not implement reflection search or CLR loading/IL execution. Physical enum/boxing identity, other Enum APIs, complete messages, language integration, full acceptance and release qualification remain open. Product runtime dependencies remain JDK-only. Validation intermediates and caches stay on D:.
