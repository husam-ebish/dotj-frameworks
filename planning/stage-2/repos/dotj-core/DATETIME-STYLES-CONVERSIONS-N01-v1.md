# Selected DateTimeStyles IConvertible contracts

Batch 2082 advances DJ-001-WP-05-T1; no task or release gate is accepted.

DateTimeStyles implements the selected IConvertible contract. Its underlying Int32 supplies numeric conversion and checked-range behavior, floating conversions, Decimal bits, TypeCode and invalid DateTime conversion. Enum-specific ToType preserves the original carrier for self/Object/Enum targets and uses enum flag text for String; unsupported targets and null target types retain native failures. The provider is ignored by these selected native enum operations.

The pinned CoreLib 10.0.12 oracle records 448 direct and 700 target conversions over 28 values, including signed endpoints, range boundaries and single-precision rounding anchors. Its emitted provider throws if queried. All 2297 packaged groups pass through direct/interface routes, checking primitive values, floating bits, four Decimal words, exception identity/HResult/parameters, boxed Java result carriers, enum text/value and native same-box observations. Type now projects IComparable, IFormattable and IConvertible with corresponding lookup, assignability, instance and defensive-copy behavior. Earlier formatting/comparison fixtures are updated for the expanded selected interface profile.

ISpanFormattable remains explicitly omitted. Inherited CLR Enum contracts are projected onto a Java immutable carrier; physical CLR boxing/type identity, other System.Enum APIs, complete messages, language/byref integration and full framework/release qualification remain open. Product runtime dependencies remain JDK-only.
