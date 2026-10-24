# Selected enum name and membership queries

Batch 2053 advances `DJ-001-WP-01-T1`; no implementation task is accepted.

The pinned CoreLib 10.0.12 reference records 248 query pairs across NumberStyles, TimeSpanStyles, DayOfWeek and DateTimeKind. The packaged Java consumer checks 496 results, including exception class, HResult and ArgumentException parameter names.

GetEnumName accepts the selected signed numeric widths and selected foreign enum carriers by numeric value. IsEnumDefined requires the target enum carrier or its Int32 underlying carrier, while String queries use exact declared names. A NumberStyles combination with value 15 is unnamed and undefined. Boolean and Double membership queries throw InvalidOperationException; numeric width and foreign enum membership mismatches throw ArgumentException without a parameter name.

The implementation scans declared constants for both name and membership queries, avoiding Java Enum casts for numeric flag carriers. Selected foreign enums use the existing numeric-value adapter.

Arbitrary undefined DayOfWeek/DateTimeKind Java values, unsigned and other underlying enum types, full reflection/interface dispatch, language lowering and E01/E02/E03/N01 release qualification remain open. Java numeric adapters do not establish complete CLR enum boxing parity. The product retains JDK-only runtime dependencies.
