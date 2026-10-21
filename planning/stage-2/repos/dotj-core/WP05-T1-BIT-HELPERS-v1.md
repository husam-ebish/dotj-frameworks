# WP-05-T1 selected Int32 bit helpers

Profile: pinned .NET 10.0.12 CoreLib and Java 21 foundation candidate. Status: **provisional**; `DJ-001-WP-05-T1`, E01/E02/E03 and N01 remain open.

The pinned [foundation metadata](evidence/foundation-selected-metadata-v10.0.12.json) records the exact static names, `System.Int32` parameters and return types for `IsEvenInteger`, `IsOddInteger`, `IsNegative`, `IsPositive`, `IsPow2`, `LeadingZeroCount`, `TrailingZeroCount`, `PopCount`, `Log2`, `RotateLeft` and `RotateRight`. The selected behavior covers zero, powers of two, mixed bits, signed extrema, negative `Log2` errors, and rotation counts of -1, 1, 31 and 32.

The Java candidate preserves these method names on `System.Int32`. Its boxed `Int32` carrier represents the CLR value type in these calls; boolean methods return `boolean`, and integer methods return `Int32`. [The packaged consumer](../../../../dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32BitConsumer.java) checks the pinned vectors against the built JAR. The declared-surface inventory records remaining numeric names and overloads separately.

The selected signed arithmetic slice adds `Abs`, `Sign`, `Max`, `Min`, `Clamp`, `CopySign`, `MaxMagnitude` and `MinMagnitude` with pinned `System.Int32` parameter and return identities. The [signed arithmetic consumer](../../../../dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32ArithmeticConsumer.java) checks signed extrema, equal-magnitude tie choices, clamp bounds, and overflow for `Abs(Int32.MinValue)` and positive `CopySign(Int32.MinValue, sign)`.

Qualification remains open for the CLR value-type ABI, all untested values and overloads, generic numeric interfaces, native integer operations, and the remaining WP-05 numeric, text and time scope. This selected comparison is not a complete Int32 compatibility claim.
