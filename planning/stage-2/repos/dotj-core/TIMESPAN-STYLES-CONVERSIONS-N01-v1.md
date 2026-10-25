# Selected TimeSpanStyles IConvertible contracts

Batch 2088 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

TimeSpanStyles implements selected IConvertible contracts using Int32 numeric conversions and enum-specific target dispatch. Self/Object/Enum targets retain the original carrier, String uses enum text, numeric targets use the selected boxed Java carriers and checked ranges, unsupported targets fail, and null targets throw with targetType. TypeCode is Int32; DateTime conversion remains invalid. The provider is ignored by the selected native operations.

The pinned CoreLib 10.0.12 oracle records 448 direct and 700 target conversions over 28 boundary/rounding/flag values. All 2297 packaged groups pass through direct and interface routes, checking values, floating bits, four Decimal words, exceptions/HResults/parameters, result carriers, enum text/value and same-box observations. Emitted native and Java providers throw if queried. Type now projects IComparable, IFormattable and IConvertible and verifies lookup, assignability, instance membership and fresh interface arrays. Earlier formatting/comparison fixtures are updated for the expanded selected profile.

ISpanFormattable remains explicitly omitted. Inherited Enum contracts are projected onto the Java immutable carrier; physical CLR boxing/enum identity, other Enum APIs, complete messages, language integration, full framework acceptance and release qualification remain open. Product runtime dependencies remain JDK-only. All validation intermediates and caches stay on D:.
