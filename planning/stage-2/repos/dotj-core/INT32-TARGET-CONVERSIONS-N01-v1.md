# Selected Int32 target conversions

Batch 2060 advances `DJ-001-WP-05-T1`; no implementation task is accepted.

Int32.ToType now dispatches selected primitive, Decimal, String and Object targets through the existing checked IConvertible operations. Numeric return values use the candidate's existing logical carriers, including SByte/Byte/UInt16/UInt32 wrappers and the BigInteger UInt64 carrier. Self/Object conversions retain the existing immutable value. A package-internal dispatcher supports these selected mappings without adding a public Java method.

Null targets throw ArgumentNullException with targetType. Unsupported targets, including interfaces, Enum, ValueType, DBNull, TimeSpan and array types, throw InvalidCastException. Checked numeric range failures retain OverflowException. The pinned CoreLib 10.0.12 reference records 506 calls across 22 input values and 23 targets, including signed/unsigned width limits and binary32 precision boundaries. The packaged consumer checks Java carrier categories, numeric text/character/Boolean values, exact floating result bits and selected exception class/HResult/parameter names.

This is an invariant provider-null profile. Arbitrary providers, complete messages, physical CLR boxing/value-copy identity, other source types and language/release qualification remain open. The package-internal dispatcher alone grants no qualification to another source type. Product runtime dependencies remain JDK-only.
