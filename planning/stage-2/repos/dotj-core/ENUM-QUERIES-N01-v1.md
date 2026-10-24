# Selected enum name and membership queries

Batch 2053 advances `DJ-001-WP-01-T1`; no implementation task is accepted.

The pinned CoreLib 10.0.12 reference records 248 query pairs across NumberStyles, TimeSpanStyles, DayOfWeek and DateTimeKind. The packaged Java consumer checks 496 results, including exception class, HResult and ArgumentException parameter names.

GetEnumName accepts the selected signed numeric widths and selected foreign enum carriers by numeric value. IsEnumDefined requires the target enum carrier or its Int32 underlying carrier, while String queries use exact declared names. A NumberStyles combination with value 15 is unnamed and undefined. Boolean and Double membership queries throw InvalidOperationException; numeric width and foreign enum membership mismatches throw ArgumentException without a parameter name.

The implementation scans declared constants for both name and membership queries, avoiding Java Enum casts for numeric flag carriers. Selected foreign enums use the existing numeric-value adapter.

Arbitrary undefined DayOfWeek/DateTimeKind Java values, unsigned and other underlying enum types, full reflection/interface dispatch, language lowering and E01/E02/E03/N01 release qualification remain open. Java numeric adapters do not establish complete CLR enum boxing parity. The product retains JDK-only runtime dependencies.

Batch 2054 adds 162 pinned failure cases for nine non-enum receivers: Object, String, Int32, Void, Enum, ValueType and weekday array/pointer/by-reference types. Null arguments precede receiver validation for GetEnumName and IsEnumDefined. Unsupported GetEnumName argument categories also precede receiver validation, while IsEnumDefined checks its receiver after null. The four collection/underlying-type queries reject non-enum receivers with enumType. Exceptions retain native HResult and parameter names. Shape receivers use explicit Type factories; this does not qualify general name lookup for pointer/by-reference types.
