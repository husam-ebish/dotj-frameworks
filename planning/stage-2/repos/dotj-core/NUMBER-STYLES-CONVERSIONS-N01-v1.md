# Selected NumberStyles IConvertible contracts

Batch 2093 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

NumberStyles implements selected IConvertible contracts. Int32 numeric conversions provide checked ranges, floating and Decimal values, TypeCode and invalid DateTime conversion. Enum-specific ToType preserves the original carrier for self/Object/Enum targets, emits enum flag text for String, and retains native errors for unsupported/null targets. The provider is ignored in the selected native routes.

The pinned CoreLib 10.0.12 reference contains 624 direct and 975 target cases over 39 values, including every named value, range limits and floating rounding anchors. All 3199 packaged groups pass through direct/interface routes, comparing primitive values, floating bits, Decimal words, exception identity/HResult/parameters, result carriers, enum text/value and same-box observations. Native and Java providers throw if queried. Type now projects IComparable/IFormattable/IConvertible; earlier enum fixtures and the foundation API audit require the expanded profile and conversion signatures. The API preview passes.

ISpanFormattable remains explicitly omitted. These inherited CLR Enum contracts are projected onto a Java immutable carrier; physical enum/boxing identity, other Enum APIs, full messages, language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only. Validation intermediates and caches stay on D:.
