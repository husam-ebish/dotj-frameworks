# Selected boxed value, enum and array membership

Batch 2068 advances `DJ-001-WP-01-T1`; no implementation task is accepted.

ValueType membership uses the logical Type classification added in Batch 2067. Enum membership now uses the corresponding logical enum flag, covering selected reflection and context flag carriers previously omitted from the explicit list. System.Array base membership recognizes selected Java array storage, alongside the existing concrete-array shape checks.

The pinned CoreLib 10.0.12 reference records 1,560 queries across forty values and 39 targets. Samples cover selected primitive/unsigned carriers, Decimal, DateTime, TimeSpan, context and entry structs, a tuple, twelve enum kinds, unnamed/undefined enum values, null/reference values and three array kinds. Enum.ToObject retains the undefined TimeSpanStyles value without PowerShell enum-conversion validation. Targets include Object/ValueType/Enum, concrete selected types, Void, System.Array and concrete arrays.

The packaged consumer passes all groups. Native default SerializationEntry is compared with a Java entry obtained through public SerializationInfo enumeration; only type membership is compared, with no constructor or field-state parity claim. Tuple membership is tested against the selected base/concrete targets, not generic-definition identity. These logical predicates do not establish full CLR boxing, unboxing/casting, array storage, arbitrary user types or language/release qualification. No product runtime dependency changes.
