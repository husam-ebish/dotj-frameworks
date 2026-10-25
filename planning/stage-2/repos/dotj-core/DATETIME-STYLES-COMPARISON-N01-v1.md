# Selected DateTimeStyles comparison and equality

Batch 2081 advances DJ-001-WP-05-T1; no task or release gate is accepted.

The immutable DateTimeStyles carrier implements IComparable. CompareTo returns signed numeric ordering for the exact carrier type, returns one for null and throws the native ArgumentException with no parameter name for other types. Equals(Object) and the Java equals adapter require the exact enum carrier and numeric value. GetHashCode projects the native Int32 hash; the existing Java hashCode adapter returns the same numeric hash. Type exposes the supported IComparable/IFormattable profiles and corresponding lookup, assignability and instance tests.

The pinned CoreLib 10.0.12 reference records 22 hashes and 792 cases spanning full signed endpoints, undefined and composite styles, null, scalar boxes, strings, plain objects and five other enum types. The packaged consumer passes 3213 groups across direct/interface comparison, capitalized/Java equality, capitalized/Java hashes and defensive interface metadata. The earlier 12362 formatting groups also pass after updating their selected interface projection to include the newly supported IComparable contract. Native IConvertible and ISpanFormattable remain explicitly omitted.

Inherited CLR Enum contracts are projected onto the Java carrier. Physical enum/language identity, other Enum methods, the remaining interfaces, complete messages and full framework/release qualification remain open. Product runtime dependencies remain JDK-only.
