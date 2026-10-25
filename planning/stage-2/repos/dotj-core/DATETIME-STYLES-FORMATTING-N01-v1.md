# Selected DateTimeStyles enum formatting

Batch 2080 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

DateTimeStyles now maps default, provider, format and format/provider ToString routes and implements IFormattable. G/F formatting selects an exact named value or the selected descending flag decomposition, including composite AllowWhiteSpaces. Unknown residual bits fall back to signed decimal text. D uses signed decimal; X uses eight uppercase hexadecimal digits. Empty/null formats select G; upper/lowercase G/F/D/X are supported; invalid formats throw FormatException. The Java get_Name adapter remains the declared-name/numeric accessor rather than composite formatting.

The pinned CoreLib 10.0.12 oracle captures 263 default values and 3945 formatted cases. A dynamically emitted native IFormatProvider throws if queried; all selected enum formatting routes ignore it. The Java consumer uses an equivalent throwing provider. All 12362 groups pass, checking three formatted routes, two default routes, exception type/HResult, selected interface identity/lookup/assignability/instance membership and defensive interface arrays. javap checks the four public ToString signatures and IFormattable declaration.

Native inherited Enum formatting is projected onto the Java immutable value carrier. This does not establish physical CLR enum identity or a complete System.Enum implementation. Type exposes the supported IFormattable interface; the other native IComparable, IConvertible and ISpanFormattable contracts are explicitly recorded as omitted. Those contracts, reflection/language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only.
