# Selected core Type flags

Batch 2064 advances `DJ-001-WP-01-T1`; implementation acceptance remains open.

The pinned CoreLib 10.0.12 oracle records 151 cases across 37 selected base types, vector/pointer/by-reference factories and three generic parameters. Each successful case checks serializable, sealed, value, primitive, enum, class and abstract metadata plus TypeCode. A Void vector retains the native factory error. FormatterConverter is omitted from this CoreLib-only probe because it resolves from a separate assembly.

Void is now excluded from IsPrimitive. Selected value types report sealed, while explicitly mapped sealed references include NumberFormatInfo, SerializationInfo, SerializationInfoEnumerator and NullableAttribute. Serializable metadata now includes selected primitive values, Object/ValueType/Enum bases, Decimal/DateTime/TimeSpan, DictionaryEntry, ValueTuple and the selected List/Dictionary definitions. Pointer, by-reference and generic-parameter forms remain non-serializable. Native StreamingContext, SerializationEntry and NumberFormatInfo are non-serializable in this pinned profile and retain that result.

These are logical CLR metadata flags, not inferences from Java final/interface modifiers. Serializable metadata grants no serialization implementation or distribution qualification. Arbitrary types, other assemblies, full reflection/language behavior and release acceptance remain open. No product runtime dependency changes.
