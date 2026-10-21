# WP-05-T1 selected Int32 bit helpers

Profile: pinned .NET 10.0.12 CoreLib and Java 21 foundation candidate. Status: **provisional**; `DJ-001-WP-05-T1`, E01/E02/E03 and N01 remain open.

The pinned [foundation metadata](evidence/foundation-selected-metadata-v10.0.12.json) records the exact static names, `System.Int32` parameters and return types for `IsEvenInteger`, `IsOddInteger`, `IsNegative`, `IsPositive`, `IsPow2`, `LeadingZeroCount`, `TrailingZeroCount`, `PopCount`, `Log2`, `RotateLeft` and `RotateRight`. The selected behavior covers zero, powers of two, mixed bits, signed extrema, negative `Log2` errors, and rotation counts of -1, 1, 31 and 32.

The Java candidate preserves these method names on `System.Int32`. Its boxed `Int32` carrier represents the CLR value type in these calls; boolean methods return `boolean`, and integer methods return `Int32`. [The packaged consumer](../../../../dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32BitConsumer.java) checks the pinned vectors against the built JAR. The declared-surface inventory records remaining numeric names and overloads separately.

The selected signed arithmetic slice adds `Abs`, `Sign`, `Max`, `Min`, `Clamp`, `CopySign`, `MaxMagnitude` and `MinMagnitude` with pinned `System.Int32` parameter and return identities. The [signed arithmetic consumer](../../../../dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32ArithmeticConsumer.java) checks signed extrema, equal-magnitude tie choices, clamp bounds, and overflow for `Abs(Int32.MinValue)` and positive `CopySign(Int32.MinValue, sign)`.

The selected value identity slice adds both `Equals` overloads and `GetHashCode` with the pinned names and return types. The same consumer checks equal, unequal, null and wrong-type inputs plus zero, positive and negative hashes. `BigMul(Int32, Int32)` returns a Java `long` for the pinned CLR `Int64` result and is checked at signed extrema without 32-bit intermediate overflow.

The selected `DivRem(Int32, Int32)` slice returns a `ValueTuple<Int32, Int32>` with writable `Item1` quotient and `Item2` remainder fields. The oracle and packaged consumer check five signed division pairs, divide-by-zero and minimum-value overflow. `DivideByZeroException` and `OverflowException` inherit `ArithmeticException`; their default messages and HRESULTs are pinned. The Java tuple remains a reference carrier, so CLR value-type ABI and general tuple behavior remain open.

The selected generic `CreateChecked`, `CreateSaturating` and `CreateTruncating` slice covers nine `Int64` inputs across both `Int32` bounds, with checked overflow, saturation and low-bit truncation pinned by the CLR oracle. The Java candidate also accepts its own `Int32` carrier and Java `Integer`; other `INumberBase<TOther>` inputs, generic constraints and full cross-numeric behavior remain open.

The same three methods also cover nine pinned `BigInteger` inputs, including values beyond `Int64` range. The packaged consumer verifies checked overflow, clamping and low-bit truncation for the Java `BigInteger` carrier.

Fourteen pinned `Double` inputs cover fractions around both `Int32` bounds, infinities and `NaN`. Checked creation accepts values whose truncated result fits, while saturating and truncating creation follow the pinned `Double` clamping behavior. The packaged consumer checks all fourteen outcomes.

Fourteen pinned `Single` inputs cover representable values around both `Int32` bounds, extrema, fractions, infinities and `NaN`. The packaged consumer checks the CLR observed checked, saturated and truncated results.

Thirteen pinned `Decimal` inputs cover both decimal extrema, fractional values around the `Int32` bounds and zero. The packaged consumer verifies checked overflow and fractional truncation; both saturating and truncating creation clamp out-of-range decimal inputs in the observed CLR implementation. Remaining numeric source types and generic interface constraints remain open.

An exact declared-method review found that name-level coverage concealed ordinary overload gaps. The candidate now adds typed `CompareTo(Int32)`, `Parse(String, NumberStyles)`, `Parse(String, IFormatProvider)`, `TryParse(String, IFormatProvider, out Int32)`, `ToString()` and `ToString(String)` routes. The oracle and packaged consumer cover selected comparison, parse, error, out-result and formatting behavior. Span and UTF-8 overloads, full culture behavior and CLR generic numeric interface contracts remain open.

The declared field inventory also identifies literal `Int32.MinValue` and `Int32.MaxValue`. The candidate exposes these as public Java `int` constants and checks their compiled declarations and extrema in the packaged consumer. CLR value-type field metadata and the broader `.j` ABI remain open.

The selected generic creation methods now accept product `Byte`, `SByte`, `UInt16` and `UInt32` carriers. Ten pinned CLR inputs cover their endpoints; `UInt32` values above `Int32.MaxValue` overflow in checked creation, clamp in saturating creation and retain their low 32 bits in truncating creation. The packaged consumer checks these paths. Other numeric carriers and complete `INumberBase<TOther>` constraints remain open.

Qualification remains open for the CLR value-type ABI, all untested values and overloads, generic numeric interfaces, native integer operations, and the remaining WP-05 numeric, text and time scope. This selected comparison is not a complete Int32 compatibility claim.
