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

The [compiled `Int32` signature audit](evidence/int32-declared-signature-audit-v1.json) projects all 53 pinned declared methods to Java shapes: 43 have a candidate declaration and 10 span-based `Parse`/`TryParse` overloads lack a one-to-one projection. It also lists 18 extra public Java methods, including conversion-interface methods and carrier helpers that CLR `Int32` does not declare as public. Projection checks names, staticness, generic arity, return shape and parameter shape; it does not establish value-type ABI or behavior parity. These gaps remain visible in the repeatable foundation gate.

A selected `ReadOnlySpan<T>` carrier now supports character and UTF-8 byte views for the four `Parse` and six `TryParse` CLR span paths. The pinned oracle and packaged consumer check numeric, hexadecimal and invalid inputs. Java erasure collapses those ten distinct CLR overloads into five generic candidate declarations, so the audit still records ten missing one-to-one projected signatures and five collapsed carrier groups. The carrier is a heap object, unlike CLR's byref-like span; arbitrary slicing, lifetime constraints, full UTF-8 error behavior and exact overload identity remain open.

The [erasure contract](evidence/int32-erasure-contract-v1.json) reruns a javac name-clash probe, links each byte/char CLR pair to its single Java carrier, and classifies all 18 extra public Java methods. A future `.j` frontend must resolve the source span element type before backend lowering and keep interface/carrier bridges out of the exact public contract. No compiler consumes this contract yet.

A mutable `Span<T>` carrier now supports the selected `Int32.TryFormat` Char and UTF-8 Byte paths with array-backed subviews. The packaged consumer checks the pinned `42` success and short-buffer failure vectors, written counts and unchanged bytes outside the view. Java erasure maps the two CLR formatting signatures to one supplemental Java carrier; the existing array interface methods remain. The heap carrier and generic overload do not establish CLR span lifetime, interface ABI or exact public signature equivalence.

The formatting carrier now accepts a `ReadOnlySpan<Character>` format view and reads only its selected slice. The packaged consumer also checks pinned `D5` and `X4` results for both destination element types, including negative decimal precision. `ReadOnlySpan<T>` remains heap-backed; source-type validation for `.j` syntax still belongs in the future frontend.

The selected heap carriers now use typed `OfChars` and `OfUtf8Bytes` factories with private array constructors. A [compiled factory audit](evidence/span-factory-types-v1.json) checks all four factory shapes and proves that four mismatched assignments fail Java compilation. Raw types and casts can still bypass Java generic checks; this does not implement CLR span lifetime or `.j` overload resolution.

A selected `System.Globalization.NumberFormatInfo` candidate now supplies group separator, decimal separator and default decimal digits to `Int32` `N` formatting through `IFormatProvider.GetFormat`. The pinned .NET oracle records `12_345:00`, `-42:00` and `42:000`; the packaged Java consumer checks ordinary `ToString` plus Char and UTF-8 Byte span formatting for each. Other format specifiers, provider objects and full culture behavior remain open.

The selected provider also carries a custom negative sign. The pinned .NET oracle confirms that `NumberStyles.Integer` parses `~42` as `-42`, rejects `-42` under that provider, and formats negative `N2` as `~42.00`. The packaged consumer checks string and Char/UTF-8 span parsing and formatting on those paths. Other sign placement and parsing styles remain open.

The same pinned provider also yields `~42` for `D` and `ToString(provider)`, and `~00042` for `D5`. The packaged consumer checks both format strings through the Char and UTF-8 Byte span carrier. Currency, percent and other provider-sensitive formats remain open.

The selected custom negative sign now also reaches `G`, `g2`, `G5` and `R`, all pinned as `~42` by the .NET oracle. The packaged consumer checks ordinary and Char/UTF-8 span formatting for these cases. Percent and broader culture behavior remain open.

The `C` format now consumes selected currency symbol, group separator, decimal separator, default precision and negative pattern settings from `NumberFormatInfo`. The pinned .NET oracle and packaged Char/UTF-8 consumers agree for `USD12_345:000`, `USD12_345`, `~USD12_345:00` and `(USD12_345:00)`. Other currency patterns, variable group sizes and broader culture behavior remain open.

The `P` format now uses selected percent symbol, separators, default precision and positive/negative pattern settings. The pinned .NET oracle and packaged consumers agree for `4_200:000 pct`, `~4_200:00 pct`, `4_200:00pct` and `~4_200:00pct`. Other percent patterns, variable group sizes and broader culture behavior remain open.

The `F`/`f` format now uses selected number decimal separator, default precision and negative sign. The pinned oracle and packaged consumers agree for `~42:000`, `~42:0` and `~42` across ordinary and Char/UTF-8 span formatting. Other numeric provider behavior remains open.

The `E`/`e` format now uses the selected number decimal separator and negative sign. The pinned oracle and packaged consumers agree for `~4:20E+001`, `4:2e+001` and `~4E+001`. Broader numeric culture behavior remains open.

The selected provider positive sign now applies to `NumberStyles.Integer` parsing and positive exponents. The pinned oracle and packaged consumers accept `plus42`, reject `+42` under that provider, and agree on `4.2Eplus001` and `~4.2Eplus001` in ordinary and Char/UTF-8 span formatting. Other NumberStyles and numeric cultures remain open.

The selected `NumberStyles.Number` path now accepts custom group and decimal separators, zero fractional digits and leading/trailing custom signs. The pinned oracle and packaged consumers agree on grouped positive/negative values, reject a nonzero fractional input and reject the standard `+` under the custom provider. Other flag combinations, grouping rules and full culture behavior remain open.

Twelve further pinned `NumberStyles.Number` boundaries now run against Java string and both span carriers. The parser rejects a leading group separator and group characters in the fractional part, while accepting a trailing group separator, an empty integer part before zero fractional digits, and selected trailing signs, matching these .NET 10 observations. Other grouping configurations remain open.

The selected `NumberGroupSizes` carrier now copies arrays at its getter and setter and applies repeated and terminal-zero group configurations to `Int32` `N` formatting. The .NET 10 oracle, packaged string output, and Char/UTF-8 span output agree on `12_34_56_789`, `-12_34_56_789.00`, and `1234_56_789`; selected `NumberStyles.Number` parsing also accepts the repeated-group example. Invalid size vectors and broader culture behavior remain open.

Selected `CurrencyGroupSizes` and `PercentGroupSizes` now use the same defensive-copy carrier and group their respective `Int32` `C` and `P` formats. The oracle and packaged consumer agree on positive and negative custom group-size examples in string and span formatting. Broader culture behavior remains open.

The pinned .NET 10 oracle now covers selected group-size setter boundaries: empty, zero-only and terminal-zero arrays are accepted; negative, over-nine and interior-zero sizes throw `ArgumentException`, while a null array throws `ArgumentNullException`. The packaged Java consumer checks those exception types and accepted assignments. Unobserved error messages and culture behavior remain open.

Selected `NumberStyles.Float` parsing now covers custom decimal and sign tokens, exponent signs, exact integer results, fractional overflow, invalid grouping, and trailing-sign rejection. Fifteen pinned .NET 10 vectors run against packaged string, Char span, and UTF-8 span carriers; the rejected string cases also check `FormatException` versus `OverflowException`. Other `NumberStyles` combinations and broader culture behavior remain open.

The standalone `AllowThousands`, `AllowDecimalPoint`, and `AllowExponent` `NumberStyles` values now parse selected custom-provider input. Twenty-three pinned .NET 10 vectors cover their distinct whitespace, sign, grouping, decimal, and exponent permissions across string and both span carriers, including exact exception types on rejected strings. Composed flags and broader culture behavior remain open.

The named `NumberStyles.Currency` path now handles selected symbol placement, parentheses, custom signs, whitespace, currency or number separators, and integer-only decimal fractions. Sixteen pinned .NET 10 vectors run through packaged string and both span carriers with rejected string error types. Unmapped currency patterns and composed flags remain open.

The named `NumberStyles.Any` path now combines selected currency and number separator rules with decimal, exponent, sign, grouping and parentheses parsing. Seventeen pinned .NET 10 vectors run through packaged string and both span carriers, with fractional overflow cases checked by exception type. Arbitrary composed flags and broader culture behavior remain open.

The `NumberStyles` Java carrier now represents unnamed bitwise combinations through `Or`, while retaining the named values and the selected `System.Type` enum projection. Three composed styles with flag values 68, 67 and 160 have seventeen pinned .NET 10 parse vectors across packaged string and both span carriers. Other flag combinations and the complete CLR enum ABI remain open.

The numeric parser now dispatches combinations drawn from leading and trailing whitespace, leading sign, decimal point, and exponent flags by their bit mask. Three additional combinations (132, 35 and 164) have fifteen pinned .NET 10 vectors across packaged string and both span carriers. Parentheses, grouping with decimal or exponent, and currency composition remain open.

Selected trailing-sign parsing now works alone and with grouping, whitespace and leading-sign flags. Eighteen pinned .NET 10 vectors cover custom trailing signs, double-sign rejection and whitespace permissions in packaged string and both span carriers. Currency composition and broader combinations remain open.

Selected parentheses, grouped-decimal and grouped-exponent flag combinations now parse through a shared noncurrency path. Twenty-one pinned .NET 10 vectors cover sign and whitespace rejection, grouping confined to the integer part, exact fractional results and overflow across packaged string and both span carriers. Broader combinations and culture behavior remain open.

Selected `AllowCurrencySymbol` compositions now route through the flag parser with provider currency separators when the symbol is present. Twenty-five pinned .NET 10 vectors cover symbol placement, forbidden whitespace, grouping, decimal, exponent and custom exponent-sign behavior across packaged string and both span carriers. Broader currency patterns and cultures remain open.

Hexadecimal and binary parsing now accepts selected `AllowHexSpecifier` and `AllowBinarySpecifier` combinations with independently permitted leading or trailing whitespace. Twenty-four pinned .NET 10 input vectors cover exact two's-complement limits, whitespace and invalid text across packaged string and both span carriers; four invalid flag masks throw `ArgumentException` for Parse and TryParse. Other flag validation and radix cultures remain open.

The shared noncurrency parser now receives remaining valid flag masks instead of returning an unsupported-operation error. Twenty-four pinned .NET 10 vectors cover five previously unreachable combinations of leading/trailing signs, grouping, decimal points, exponents, parentheses and whitespace in packaged string and both span carriers. Full grammar parity and edge-case ordering remain open.

Selected invalid radix-style masks now preserve the pinned error order and parameter identity: Parse with null input reports `ArgumentNullException(s)` first, while TryParse validates the style and reports `ArgumentException(style)` even for null input; invalid masks also take precedence over out-of-range text. A valid radix style retains false/zero TryParse behavior for null. Other overload and error-message details remain open.

The Float and extended numeric parsers now evaluate exponents as arbitrary-size integers against the decimal coefficient before constructing a bounded `Int32`. Sixteen pinned .NET 10 vectors cover zero with very large positive or negative exponents, nonzero overflow, and exact signed `Int32` limits in packaged string and both span carriers. Other grammar and culture edges remain open.

Qualification remains open for the CLR value-type ABI, all untested values and overloads, generic numeric interfaces, native integer operations, and the remaining WP-05 numeric, text and time scope. This selected comparison is not a complete Int32 compatibility claim.

Selected `Decimal(int[] bits)` and `Decimal.GetBits` now preserve the 96-bit coefficient, scale, and negative-zero sign. Eight pinned .NET 10 vectors cover integer, scaled, negative, zero, maximum-magnitude and scale-28 values; parsed signed zero and `IConvertible.ToDecimal` retain their bits. The packaged external consumer verifies defensive copies and the pinned invalid-array exception types and parameter identities. Decimal parsing outside these selected vectors, other constructors and operations, and CLR value-type ABI compatibility remain open.

Selected five-argument Decimal construction now combines three signed 32-bit words, a sign, and an integer scale. Nine pinned .NET 10 vectors include negative zero, maximum magnitude, and scale 28. Scales 29 and 255 produce `ArgumentOutOfRangeException(scale)` as pinned; the Java carrier also rejects negative scales. The packaged external consumer checks all selected vectors. Java uses an `int` scale carrier to represent the complete unsigned CLR byte range; CLR ABI, other Decimal constructors and operations remain open.

Selected invariant Decimal parsing now reduces excess scale or a coefficient larger than 96 bits with a single half-even rounding from the original text at each candidate scale. Thirteen pinned .NET 10 boundaries cover scale 29, tiny tie and above-tie fractions, signed zero, maximum magnitude with fractional input, and overflow. The packaged external consumer checks returned bits or `OverflowException`. Full decimal grammar, culture behavior and all untested rounding cases remain open.

Selected `Decimal.Truncate` now discards the fractional component toward zero and preserves a negative-zero sign when appropriate. Ten pinned .NET 10 bit vectors cover positive and negative fractions, signed zero, tiny scale-28 values, maximum magnitudes and trailing zero scale. The packaged external consumer checks all ten results. Other Decimal operations and untested values remain open.

Selected `Decimal.Floor` and `Decimal.Ceiling` now round to integral values in the respective directions while retaining a negative-zero sign on zero results from negative operands. Ten paired .NET 10 bit vectors cover both signs, signed zero, tiny fractions, integral values and maximum magnitudes. The packaged external consumer checks all twenty results. Other operations and untested values remain open.

Selected `Decimal.Round(value, decimals)` now uses half-even rounding for precisions 0â€“28, retains scale when the input already has fewer fractional digits, and preserves negative zero. Twelve pinned .NET 10 bit vectors cover midpoint ties, both signs, unchanged scale, maximum magnitude, and scale-28 rounding; precisions -1 and 29 produce `ArgumentOutOfRangeException(decimals)`. The packaged external consumer checks these results. Other `Round` overloads, rounding modes and untested values remain open.

Selected `MidpointRounding` values 0â€“4 and `Decimal.Round(value, decimals, mode)` now cover half-even, midpoint away from zero, toward zero, floor and ceiling behavior. Twenty-five pinned .NET 10 bit vectors cover midpoint and non-midpoint values of both signs, including negative-zero results; invalid numeric mode values -1 and 5 raise `ArgumentException(mode)` through the Java numeric carrier. The packaged external consumer checks all outcomes. Java enum representation, other `Round` overloads and untested values remain open.

The default-precision `Decimal.Round(value)` and `Decimal.Round(value, mode)` overloads now select precision zero. Eight pinned .NET 10 values yield eight default results and forty mode results, covering midpoint ties, signed zero and maximum magnitudes. The packaged external consumer checks exact result bits. Other rounding-mode and numeric boundaries remain open.

Selected `Decimal.Abs` and `Decimal.Sign` now follow nine pinned .NET 10 bit patterns, including negative zero at scales zero and two, signed scale-28 values and both maximum magnitudes. Absolute value clears the sign bit while retaining the scale; Sign returns zero, one or minus one. The packaged external consumer checks both results. Other operations and untested values remain open.

Selected `Decimal.Negate` now toggles the sign bit while preserving coefficient and scale for ten pinned .NET 10 values, including positive and negative zero. The packaged external consumer checks exact bits. Other operations and untested values remain open.

Selected `Decimal.Add` now retains the larger operand scale when representable, rounds to the 96-bit coefficient and scale-28 bound, preserves the observed zero-sign behavior, and throws `OverflowException` at the pinned limits. Twenty-one .NET 10 operand pairs cover cancellation, signed zero, tiny fractions, maximum magnitudes and fractional carry; the packaged external consumer checks exact result bits or overflow. Other arithmetic combinations and overloads remain open.

Selected `Decimal.Subtract` now retains the larger operand scale when representable, applies the observed left-operand zero sign on cancellation, and throws `OverflowException` at the pinned limits. Eighteen .NET 10 operand pairs cover signed zero, equal operands, tiny fractions and maximum magnitudes; the packaged external consumer checks exact result bits or overflow. Other arithmetic combinations and overloads remain open.

Selected `Decimal.Multiply` now combines scale and coefficient, rounds to the 96-bit and scale-28 bounds, and preserves observed signed-zero behavior. Thirty-eight .NET 10 pairs pin ordinary products, signed zero, maximum magnitude, overflow and tiny products around the observed scale-47/48 underflow boundary. The packaged external consumer compares every result bit pattern or overflow with the oracle. The current large-coefficient zero path is bounded to these observations; full CLR multiplication parity remains open.

Selected `Decimal.Divide` now searches for an exact representable quotient from the operand scale difference, then rounds a repeating quotient to the greatest scale that fits the 96-bit coefficient. Twenty .NET 10 pairs pin exact and repeating fractions, signed zero, scale-preserving results, magnitude limits, underflow, divide-by-zero and overflow. The packaged external consumer compares exact result bits or exception types. Broader division rounding, culture and CLR ABI remain open.

Selected `Decimal.Remainder` now returns the truncated quotient remainder with the dividend sign and observed scale, including negative zero. Twenty .NET 10 pairs pin sign combinations, fractional operands, maximum magnitude, zero dividends and divide-by-zero. The packaged external consumer compares exact result bits or the exception type. Broader remainder parity and CLR ABI remain open.

Selected `Decimal.Compare` now orders values numerically across differing scales and treats signed zero as equal. Twenty .NET 10 pairs pin sign, equality, extrema, scale and tiny-fraction behavior. The packaged external consumer compares each integer result with the oracle. Other comparison overloads and CLR ABI remain open.

Selected static `Decimal.Equals` now compares numeric value across differing scales and signed zero. Twenty .NET 10 pairs pin equal and unequal signs, extrema, scales and fractions. The packaged external consumer compares every boolean with the oracle. Instance and object equality, hashing, operators and CLR ABI remain open.

Selected `Decimal.GetHashCode` now returns zero for all zero encodings and removes representable trailing powers of ten before combining the sign, scale and coefficient words. Twenty .NET 10 values pin equal-value hashes across scales, negative values, extrema and high coefficient words. The packaged external consumer compares exact hash integers with the oracle. Java object equality and hash overrides, other numeric representations and CLR ABI remain open.

Selected `Decimal.Equals(Decimal)` and `Decimal.Equals(Object)` now compare numeric values, return false for null or unrelated objects, and keep equal-value hashes aligned. Java `equals` and `hashCode` delegate to the same value behavior for collection use. Twelve .NET 10 pairs pin signed zero, scale-equivalent values, sign differences, extrema and tiny fractions; the packaged external consumer checks both .NET-style methods and Java overrides. Operators and CLR ABI remain open.

Selected `Decimal.CompareTo(Decimal)` and `Decimal.CompareTo(Object)` now order numeric values across scale and sign, return one for a null object, and reject unrelated objects with `ArgumentException`. Twelve .NET 10 pairs pin typed and boxed comparison results, signed zero, extrema and tiny fractions. The packaged external consumer checks the results and wrong-type exception. Broader interface binding and CLR ABI remain open.

Selected static `Decimal.ToInt32` truncates fractional values toward zero, accepts the signed 32-bit limits and throws `OverflowException` beyond them. Twenty .NET 10 values pin positive and negative fractions, signed zero, tiny fractions, limit crossings and large magnitudes. The packaged external consumer checks each result or exception. Java source using a concrete `Decimal` receiver with `ToInt32(null)` is ambiguous with the existing `IConvertible.ToInt32(IFormatProvider)` method; the selected interface test now casts to `IConvertible` to express that call. Other static conversions, this Java overload collision and CLR ABI remain open.

Selected static `Decimal.IsNegative` and `Decimal.IsPositive` now report the encoded sign, including negative zero. Twelve .NET 10 bit patterns pin zero at multiple scales, nonzero signs, tiny fractions and extrema. The packaged external consumer compares both booleans with the oracle. Other number predicates and CLR ABI remain open.

Selected static `Decimal.IsInteger`, `Decimal.IsEvenInteger` and `Decimal.IsOddInteger` now check numeric integrality and parity across signed zero and differing scales. Fourteen .NET 10 bit patterns pin integral and fractional values, signs, tiny fractions and maximum magnitudes. The packaged external consumer compares all three booleans with the oracle. Other number predicates and CLR ABI remain open.

Selected static `Decimal.ToInt64` truncates fractional values toward zero, accepts the signed 64-bit limits and throws `OverflowException` beyond them. Twenty .NET 10 values pin positive and negative fractions, signed zero, tiny fractions, both limit crossings and large magnitudes. The packaged external consumer checks each result or exception. The Java concrete-receiver null-literal overload collision also applies to `ToInt64`; other static conversions and CLR ABI remain open.

Selected static `Decimal.ToUInt32` truncates fractions toward zero, accepts values from zero through 4294967295, and throws `OverflowException` outside that range. Twenty .NET 10 values pin negative fractions that truncate to zero, positive and negative whole values, unsigned limit crossings and large magnitudes. The packaged external consumer checks each result or exception. The Java concrete-receiver null-literal overload collision also applies here; other static conversions and CLR ABI remain open.

Selected static `Decimal.ToUInt64` truncates fractions toward zero, accepts values from zero through 18446744073709551615, and throws `OverflowException` outside that range. Twenty .NET 10 values pin negative fractions that truncate to zero, positive and negative whole values, unsigned limit crossings and large magnitudes. The packaged external consumer checks each result or exception. The Java concrete-receiver null-literal overload collision also applies here; other static conversions and CLR ABI remain open.

Selected static `Decimal.ToByte`, `ToSByte`, `ToInt16` and `ToUInt16` truncate fractions toward zero and enforce their respective 8-bit and 16-bit ranges. Twenty .NET 10 values pin signed zero, sign changes, each boundary and nearby overflows. The packaged external consumer checks all four results or exception types for every vector. The Java concrete-receiver null-literal overload collision also applies to these methods; other static conversions and CLR ABI remain open.

Selected static `Decimal.ToDouble` and `ToSingle` now follow the .NET 10 coefficient-word conversion order: convert the low 64 and high 32 bits to double, combine them using 2^64, divide by the double power of ten, then apply the sign; `ToSingle` casts that double result. Twenty .NET 10 bit patterns pin raw binary64 and binary32 results for signed zero, fractions, tiny values, integer word boundaries and maximum magnitudes. The packaged external consumer checks exact raw bits. The Java concrete-receiver null-literal overload collision also applies here; broader rounding parity and CLR ABI remain open.

Selected static `Decimal.CopySign` now takes the magnitude and scale from its value operand and the encoded sign from its sign operand, including negative zero. Twenty .NET 10 pairs pin positive and negative zero, ordinary values, tiny fractions, fractional scales and extrema. The packaged external consumer compares exact result bits with the oracle. Other generic-number operations and CLR ABI remain open.

Selected static `Decimal.Max` and `Min` now return the numerically greater and lesser operands. For equal values, `Max` retains the first operand's exact bits and `Min` retains the second operand's bits. Twenty .NET 10 pairs pin signed zero, equal values at different scales, ordinary values, tiny fractions and extrema. The packaged external consumer compares exact result bits with the oracle. Other extrema operations and CLR ABI remain open.

Selected static `Decimal.MaxMagnitude` and `MinMagnitude` now compare absolute values. At equal magnitude, `MaxMagnitude` takes the right operand when the left has a negative sign, otherwise the left; `MinMagnitude` takes the left when it has a negative sign, otherwise the right. Twenty-two .NET 10 pairs pin signed zero, opposite signs, equal negative values with differing scales, tiny fractions and extrema. The packaged external consumer compares exact result bits with the oracle. Other generic-number operations and CLR ABI remain open.

Selected static `Decimal.IsCanonical` now accepts every scale-zero encoding, including zero, and accepts a scaled encoding when its coefficient is not divisible by ten. Twenty .NET 10 bit patterns pin scaled zero, trailing-zero coefficients, signs, high-word values and extrema. The packaged external consumer compares each boolean with the oracle. Other generic-number operations and CLR ABI remain open.

Selected static `Decimal.Clamp` now returns the lower bound below the range, the upper bound above it, and the original value inside or equal to the bounds. Twenty .NET 10 triples pin signed zero, equal numeric values with different scales, fractional inputs, extrema and reversed bounds; reversed bounds produce `ArgumentException`. The packaged external consumer compares exact result bits or exception type. Other generic-number operations and CLR ABI remain open.

Selected static `Decimal.ToOACurrency` now multiplies by 10,000, rounds half-even to integral currency units, and rejects values outside the signed 64-bit range. Twenty .NET 10 encodings pin signed and scaled zero, midpoint ties on both signs, tiny fractions, ordinary values and overflow at Decimal extrema. The packaged external consumer compares exact currency units or `OverflowException`. Other currency conversion behavior and CLR ABI remain open.

Selected static `Decimal.FromOACurrency` now divides signed 64-bit currency units by 10,000, removes trailing coefficient zeros for nonzero values, and preserves the .NET scale-four encoding of zero. Twenty .NET 10 currency inputs pin all removable scales, both signs and signed 64-bit extrema. The packaged external consumer compares exact Decimal bits. Other currency conversion behavior and CLR ABI remain open.

Selected parameterless `Decimal.ToString()` now exposes invariant decimal text for the Java candidate. Twenty pinned .NET 10 encodings cover signed zero, preserved fractional scale, tiny fractions, high coefficient words and extrema. The packaged external consumer compares parameterless and null-provider text with the oracle. Culture-specific providers, formatting strings and CLR ABI remain open.

Selected `Decimal.ToString(format, provider)` now recognizes invariant `G` and `F2` text. `G` retains the encoded scale; `F2` prints two fractional digits and rounds midpoint values away from zero. Twenty .NET 10 encodings pin signed zero, midpoint ties on both signs, tiny fractions, scaled values and extrema. The packaged external consumer compares exact text. Other format strings, culture-specific providers and CLR ABI remain open.

Selected fixed point Decimal formatting now accepts `F`/`f` and `F`/`f` with one or two precision digits. Twenty .NET 10 value and format pairs pin precisions 0, 1, 3, 4 and 28, default precision, midpoint rounding on both signs, signed zero and extrema. The packaged external consumer compares exact invariant text. Other format families, culture-specific providers and CLR ABI remain open.

Selected invariant number formatting now accepts `N`/`n` with default or one or two precision digits. It rounds fixed decimals away from midpoint ties and groups the integer part in threes. Twenty .NET 10 value and format pairs pin grouping boundaries, both signs, rounded zero, precision 0â€“4, default precision and extrema. The packaged external consumer compares exact invariant text. Culture-specific separators, other format families and CLR ABI remain open.

Selected invariant percent formatting now accepts `P`/`p` with default or one or two precision digits. It multiplies by 100, rounds away from midpoint ties, groups the integer part, and appends a space and percent sign. Twenty .NET 10 value and format pairs pin both signs, rounded zero, fractional and grouped values, precisions 0â€“4 and extrema. The packaged external consumer compares exact text. Culture-specific percent patterns, other format families and CLR ABI remain open.

Selected invariant exponential formatting now accepts `E`/`e` with default or one or two precision digits. It rounds the mantissa away from midpoint ties, adjusts the exponent when rounding crosses ten, and prints at least three exponent digits. Twenty .NET 10 value and format pairs pin zero, tiny fractions, rounding carry, both signs, uppercase and lowercase output and extrema. The packaged external consumer compares exact text. Other format families, culture-specific providers and CLR ABI remain open.

Selected invariant currency formatting now accepts `C`/`c` with default or one or two precision digits. It uses the invariant currency sign `Â¤`, groups the integer part, and encloses negative rounded values in parentheses. Twenty .NET 10 value and format pairs pin signs, rounded zero, grouping boundaries, precision 0â€“4 and extrema. The packaged external consumer compares exact text. Culture-specific currency patterns, other format families and CLR ABI remain open.

Selected custom Decimal formatting now accepts zero placeholders before and optionally after a decimal point, such as `0000.00`. It rounds midpoint values away from zero, pads integer digits to the placeholder count, and suppresses the sign when rounding yields zero. Twenty .NET 10 value and format pairs pin padding, signs, midpoint rounding, tiny fractions and extrema. The packaged external consumer compares exact text. Optional placeholders, custom sections, culture-specific symbols and CLR ABI remain open.

Selected custom Decimal formatting now accepts a required integer zero followed by one to 99 optional fractional `#` placeholders, such as `0.##`. It rounds to the placeholder count, removes trailing fractional zeros, and omits the decimal point when no fraction remains. Twenty .NET 10 value and format pairs pin signs, tiny rounded values, trailing zeros, fractional rounding and extrema. The packaged external consumer compares exact text. Other custom patterns, sections, culture-specific symbols and CLR ABI remain open.

Selected `Decimal.Parse(text, NumberStyles.Float, provider)` now accepts invariant exponent notation alongside signed, decimal and whitespace forms. Twenty .NET 10 texts pin positive and negative exponents, signed zero, scale-28 underflow rounding, maximum magnitude, overflow and malformed forms; the packaged external consumer compares exact result bits or exception type. Other styles, provider-specific separators and CLR ABI remain open.

Selected `Decimal.Parse(text, NumberStyles.Number, provider)` now accepts invariant grouping, decimal notation and leading or trailing signs. Twenty .NET 10 texts pin grouped magnitudes, signed zero, permissive group lengths, trailing signs, scale-28 rounding, malformed placement and overflow; the packaged external consumer compares exact result bits or exception type. Provider-specific separators and other style combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.Integer, provider)` now accepts signed invariant integers with surrounding whitespace. Twenty .NET 10 texts pin leading zeros, signed zero, maximum positive and negative magnitudes, overflow, and rejected decimal, group, exponent, trailing sign and parentheses forms; the packaged external consumer compares exact result bits or exception type. Provider-specific signs and other style combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.Currency, provider)` now accepts invariant `Â¤` placement, parentheses, selected leading and trailing signs, grouping and decimal notation. Twenty .NET 10 texts pin accepted currency forms, signed zero, overflow and malformed forms; the packaged external consumer compares exact result bits or exception type. Provider-specific currency patterns and other style combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.Any, provider)` now combines invariant currency symbol, parentheses, grouping, trailing sign, decimal and exponent forms. Twenty .NET 10 texts pin mixed forms, signed zero, underflow, overflow and malformed forms; the packaged external consumer compares exact result bits or exception type. Provider-specific tokens and arbitrary composed styles remain open.

Selected `Decimal.Parse(text, NumberStyles.Number/Float, provider)` paths now recognize a `NumberFormatInfo` with custom group, decimal and sign tokens. Twenty .NET 10 texts pin grouped and exponent forms, trailing signs, signed zero, scale-28 rounding, token rejection and overflow; the packaged external consumer compares exact result bits or exception type. Other provider types, currency tokens and arbitrary styles remain open.

Selected `Decimal.Parse(text, NumberStyles.Currency, provider)` now recognizes a `NumberFormatInfo` with a custom currency symbol, currency grouping and decimal separators, and sign tokens. Twenty .NET 10 texts pin symbol placement, parentheses, signed zero, token rejection, maximum magnitude and overflow; the packaged external consumer compares exact result bits or exception type. Other currency patterns and provider types remain open.

Selected `Decimal.Parse(text, NumberStyles.Any, provider)` now selects custom number or currency separators from a `NumberFormatInfo` and accepts selected exponent, symbol, parentheses and sign forms. Twenty .NET 10 texts pin both separator families, mixed-token rejection, signed zero, maximum magnitude and overflow; the packaged external consumer compares exact result bits or exception type. Other separator overlaps and provider types remain open.

Selected `Decimal.Parse(text, NumberStyles.None, provider)` now accepts only unsigned ASCII digits with no whitespace. Twenty .NET 10 texts pin leading zeros, maximum magnitude, overflow and rejection of signs, whitespace, decimal, grouping and exponent forms; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowThousands, provider)` now accepts unsigned integer digits with invariant comma grouping and no whitespace. Twenty .NET 10 texts pin permissive group lengths and repeated separators, leading zeros, maximum magnitude, overflow and rejected sign, decimal and exponent forms; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowDecimalPoint, provider)` now accepts unsigned invariant decimal notation with no whitespace. Twenty .NET 10 texts pin omitted integer or fractional digits, scale-28 rounding, maximum magnitude, overflow and rejected sign, grouping and exponent forms; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowExponent, provider)` now accepts unsigned integer mantissas with optional signed invariant exponents and no whitespace. Twenty .NET 10 texts pin positive and negative exponent signs, scale-28 underflow, maximum magnitude, overflow and rejected leading signs, decimals and grouping; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowLeadingSign, provider)` now accepts optional invariant leading signs on integer digits with no whitespace. Twenty .NET 10 texts pin signed zero, leading zeros, maximum positive and negative magnitudes, overflow and rejected trailing signs, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowTrailingSign, provider)` now accepts optional invariant trailing signs on integer digits with no whitespace. Twenty .NET 10 texts pin signed zero, leading zeros, maximum positive and negative magnitudes, overflow and rejected leading signs, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowParentheses, provider)` now accepts integer digits optionally enclosed in parentheses to indicate a negative value. Twenty .NET 10 texts pin negative zero, leading zeros, maximum magnitude, overflow and rejected signs, whitespace, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowLeadingWhite, provider)` now accepts ASCII numeric whitespace before unsigned integer digits. Twenty .NET 10 texts pin spaces, tabs, line breaks, maximum magnitude, overflow and rejection of trailing whitespace, nonbreaking space, signs, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowTrailingWhite, provider)` now accepts ASCII numeric whitespace after unsigned integer digits. Twenty .NET 10 texts pin spaces, tabs, line breaks, maximum magnitude, overflow and rejection of leading whitespace, nonbreaking space, signs, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Other standalone flag combinations remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowCurrencySymbol, provider)` now accepts the invariant `Â¤` token before or after unsigned integer digits, or digits alone, without whitespace. Twenty .NET 10 texts pin symbol placement, maximum magnitude, overflow and rejected signs, whitespace, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Custom currency symbols and other flag combinations remain open.

Selected composed `NumberStyles` values 36, 96 and 3 now combine leading sign with decimal point, grouping with decimal point, and leading with trailing whitespace respectively. Twenty .NET 10 texts pin allowed combinations, sign and separator rejection, nonbreaking space, and overflow; the packaged external consumer compares exact result bits or exception type. Other composed flag values remain open.

Selected `Decimal.Parse(text, NumberStyles.AllowCurrencySymbol, provider)` now recognizes a custom `NumberFormatInfo.CurrencySymbol` before or after unsigned integer digits. Twenty .NET 10 texts pin `USD` placement, bare digits, maximum magnitude, overflow and rejection of duplicate or invariant symbols, signs, whitespace, decimals, grouping and exponents; the packaged external consumer compares exact result bits or exception type. Other provider types remain open.

Selected `Decimal.TryParse` string and style/provider overloads now return a success flag and reset the out value to zero on invalid text, overflow or null input. Twenty .NET 10 vectors pin exact result bits across simple, Number, Float and Integer modes; the packaged external consumer checks both the flag and out value. Span overloads, additional style combinations and CLR out-parameter ABI remain open.

The `Decimal.TryParse(text, provider, out value)` projection now delegates to Number-style parsing with custom group, decimal and sign tokens. Twenty .NET 10 vectors pin accepted and rejected provider tokens, signed zero, scale-28 rounding, maximum magnitude, null input and overflow; the packaged external consumer checks both the success flag and out bits. Span overloads and CLR out-parameter ABI remain open.

Selected Char `ReadOnlySpan` `Decimal.TryParse` simple and style/provider overloads now use the existing span view carrier, including nonzero offsets. Twenty .NET 10 Char-span vectors pin success flags and exact out bits across simple, Number, Float and Integer modes; the packaged external consumer checks each result from a sliced Char view. UTF-8 span behavior and CLR out-parameter ABI remain open.

Selected `Decimal.Parse` span overloads now accept the shared Char and UTF-8 byte view carrier. Twenty .NET 10 UTF-8 span vectors pin `TryParse` success and out bits plus `Parse` result bits or exception type across simple, Number, Float and Integer modes; the packaged external consumer uses nonzero byte-view offsets. Other span styles and CLR out-parameter ABI remain open.

The `Decimal.TryParse(span, provider, out value)` projection now delegates to Number-style parsing for both Char and UTF-8 byte views. Twenty .NET 10 vectors pin custom group, decimal and sign tokens, signed zero, scale-28 rounding, overflow and failed out-value reset; the packaged external consumer checks nonzero-offset views in both carriers. CLR out-parameter ABI remains open.

The `Decimal.Parse(text, provider)` projection now delegates to Number-style parsing for String and Char or UTF-8 `ReadOnlySpan` views. Twenty .NET 10 vectors pin custom separators and signs, exact decimal bits, null input, invalid tokens and overflow; the packaged external consumer checks nonzero-offset span views and exception types. Broader provider behavior and CLR span ABI remain open.

Selected `Decimal.ToString(provider)` and general-format output now honor a custom NumberFormatInfo decimal separator and negative sign. Twelve .NET 10 vectors pin scaled zeros, positive and negative values, and scale-28 values; a packaged external consumer checks both overloads. Other format specifiers and provider implementations remain open.

Selected `Decimal.ToString("F", provider)` fixed-format output now uses the provider's decimal digit count, decimal separator and negative sign. Twelve .NET 10 vectors pin default and explicit precision, scaled zero, positive and negative values; a packaged external consumer checks exact text. Other format specifiers and provider implementations remain open.

Selected `Decimal.ToString("N", provider)` number-format output now uses the provider's grouping and decimal separators, decimal digit count, and negative sign. Twelve .NET 10 vectors pin default and explicit precision, grouped and ungrouped values, and signs; a packaged external consumer checks exact text. Custom group sizes, other number patterns and provider implementations remain open.

Selected `Decimal.ToString("P", provider)` percent-format output now uses the provider's grouping and decimal separators, decimal digit count, percent symbol, and negative sign. Twelve .NET 10 vectors pin default and explicit precision, grouped and ungrouped values, and signs; a packaged external consumer checks exact text. Custom group sizes, other percent patterns and provider implementations remain open.

Selected `Decimal.ToString("C", provider)` currency-format output now uses the provider's grouping and decimal separators, decimal digit count, and currency symbol with the default positive and negative patterns. Twelve .NET 10 vectors pin default and explicit precision, grouped and ungrouped values, and signs; a packaged external consumer checks exact text. Custom group sizes, other currency patterns and provider implementations remain open.

Selected `Decimal.ToString("E", provider)` exponential-format output now uses the provider's decimal separator, negative sign and positive sign in the mantissa and exponent. Twelve .NET 10 vectors pin default and explicit precision, zero, positive and negative exponents, and signs; a packaged external consumer checks exact text. Other provider implementations remain open.

Selected `Decimal.ToString(custom, provider)` zero-placeholder output now uses the provider's decimal separator and negative sign for required and optional fractional placeholders. Twelve .NET 10 vectors pin padded integers, scaled values, optional trailing digits and signs; a packaged external consumer checks exact text. Broader custom-format syntax and provider implementations remain open.

Selected `Decimal.ToString("N", provider)` now honors repeated and terminal-zero `NumberGroupSizes` sequences instead of always grouping every three digits. Twelve .NET 10 vectors pin positive and negative values at two scales under `[3,2]` and `[3,2,0]`; a packaged external consumer checks exact text. Other number patterns and provider implementations remain open.

Selected `Decimal.ToString("C", provider)` now honors repeated and terminal-zero `CurrencyGroupSizes` sequences. Twelve .NET 10 vectors pin positive and negative values at two scales under `[3,2]` and `[3,2,0]`; a packaged external consumer checks exact text. Other currency patterns and provider implementations remain open.

Selected `Decimal.ToString("P", provider)` now honors repeated and terminal-zero `PercentGroupSizes` sequences. Twelve .NET 10 vectors pin positive and negative values at two scales under `[3,2]` and `[3,2,0]`; a packaged external consumer checks exact text. Other percent patterns and provider implementations remain open.

Selected `Decimal.ToString("C", provider)` now honors currency negative patterns 0 through 3 and a custom negative sign. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; a packaged external consumer checks exact text. Other currency patterns and provider implementations remain open.

Selected `Decimal.ToString("C", provider)` now also honors currency negative patterns 4 through 7. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; the packaged external consumer checks exact text. Other currency patterns and provider implementations remain open.

Selected `Decimal.ToString("C", provider)` now also honors currency negative patterns 8 through 11. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; the packaged external consumer checks exact text. Other currency patterns and provider implementations remain open.

Selected `Decimal.ToString("C", provider)` now also honors currency negative patterns 12 through 16. Fifteen .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; the packaged external consumer checks exact text. All seventeen currency negative patterns are represented in bounded vectors; other provider implementations remain open.

Selected `Decimal.ToString("P", provider)` now honors percent positive patterns 0 through 3. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; a packaged external consumer checks exact text. Percent negative patterns and other provider implementations remain open.

Selected `Decimal.ToString("P", provider)` now honors percent negative patterns 0 through 3. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; a packaged external consumer checks exact text. Remaining percent negative patterns and other provider implementations remain open.

Selected `Decimal.ToString("P", provider)` now also honors percent negative patterns 4 through 7. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; the packaged external consumer checks exact text. Remaining percent negative patterns and other provider implementations remain open.

Selected `Decimal.ToString("P", provider)` now also honors percent negative patterns 8 through 11. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; the packaged external consumer checks exact text. All twelve percent negative patterns are represented in bounded vectors; other provider implementations remain open.

Selected Decimal parsing and formatting now resolve `NumberFormatInfo` through `IFormatProvider.GetFormat`. Twelve .NET 10 vectors pin exact bits and general and number-format text through a non-NumberFormatInfo wrapper provider; a packaged external consumer checks the same wrapper behavior. Broader provider contracts and Decimal semantics remain open.

The `NumberFormatInfo.CurrencyPositivePattern` projection now exposes patterns 0 through 3, and selected `Decimal.ToString("C", provider)` uses them. Twelve .NET 10 vectors pin each pattern across ungrouped, grouped and fractional values; a packaged external consumer checks exact text. Broader provider contracts and Decimal semantics remain open.

Selected `Int32.ToString("C", provider)` now also honors currency positive patterns 0 through 3. Twelve .NET 10 vectors pin each pattern for small, grouped and maximum values; a packaged external consumer checks exact text. Other currency formatting behavior remains open.

Selected `Int32.ToString("C", provider)` now also honors currency negative patterns 2 through 5. Twelve .NET 10 vectors pin each pattern for small, grouped and minimum values; a packaged external consumer checks exact text. Other currency negative patterns remain open.

Selected `Int32.ToString("C", provider)` now also honors currency negative patterns 6 through 9. Twelve .NET 10 vectors pin each pattern for small, grouped and minimum values; the packaged external consumer checks exact text. Other currency negative patterns remain open.

Selected `Int32.ToString("C", provider)` now also honors currency negative patterns 10 through 16. Twenty-one .NET 10 vectors pin each pattern for small, grouped and minimum values; the packaged external consumer checks exact text. All seventeen currency negative patterns are represented in bounded Int32 vectors, while other culture behavior remains open.

Selected `Int32.ToString("P", provider)` now honors percent positive patterns 0 through 3. Twelve .NET 10 vectors pin each pattern for small, grouped and maximum values; a packaged external consumer checks exact text. Other percent formatting behavior remains open.

Selected `Int32.ToString("P", provider)` now also honors percent negative patterns 2 through 5. Twelve .NET 10 vectors pin each pattern for small, grouped and minimum values; a packaged external consumer checks exact text. Other percent negative patterns remain open.

Selected `Int32.ToString("P", provider)` now also honors percent negative patterns 6 through 9. Twelve .NET 10 vectors pin each pattern for small, grouped and minimum values; the packaged external consumer checks exact text. Other percent negative patterns remain open.

Selected `Int32.ToString("P", provider)` now also honors percent negative patterns 10 and 11. Twelve .NET 10 vectors pin the two patterns across six negative values; the packaged external consumer checks exact text. All twelve percent negative patterns are represented in bounded Int32 vectors, while other culture behavior remains open.

Selected `Int32.ToString("N", provider)` now honors `NumberFormatInfo.NumberNegativePattern` values 0 through 4. Fifteen .NET 10 vectors pin each pattern across small, grouped and minimum negative values; a packaged external consumer checks exact text. Decimal number patterns and other culture behavior remain open.

Selected `Decimal.ToString("N", provider)` now honors `NumberFormatInfo.NumberNegativePattern` values 0 through 4. Fifteen .NET 10 vectors pin each pattern across small, grouped and fractional negative values; a packaged external consumer checks exact text. Other Decimal culture behavior remains open.

The `NumberFormatInfo.NumberNegativePattern` property now has a selected boundary contract: default 1, accepted values 0 through 4, and `ArgumentOutOfRangeException` for four invalid inputs while preserving the last valid value. A .NET 10 oracle and packaged external consumer agree on those cases; broader globalization behavior remains open.

Selected `Decimal.ToString("N2", provider)` rounding near negative zero is pinned across all five negative patterns. Twenty .NET 10 vectors confirm that rounded zero loses the negative decoration, while `-0.005` retains it after rounding to `0.01`; the packaged consumer matches. Broader rounding and globalization behavior remains open.

Selected `Int32.ToString("N", provider)` now supports precision 1001 and 1024, beyond the earlier 1000 limit. Six .NET 10 vectors check three negative patterns at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("D", provider)` now supports precision 1001 and 1024. Six .NET 10 vectors check negative, zero and positive values at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("x"/"X")` now supports precision 1001 and 1024. Twelve .NET 10 vectors check negative, zero and positive values in both cases against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("B")` now supports precision 1001 and 1024. Six .NET 10 vectors check negative, zero and positive values at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("F", provider)` now supports precision 1001 and 1024. Six .NET 10 vectors check negative, zero and positive values with custom number decimal separator and sign at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("C", provider)` now supports precision 1001 and 1024. Six .NET 10 vectors check negative, zero and positive values with custom currency symbol, decimal separator and patterns at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("P", provider)` now supports precision 1001 and 1024. Six .NET 10 vectors check negative, zero and positive values with custom percent symbol, decimal separator and patterns at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString("E", provider)` now supports precision 1001 and 1024. Six .NET 10 vectors check negative, zero and positive values with custom number decimal separator and exponent signs at both precisions against a packaged external consumer. The implementation guard remains bounded at 2048; higher precision and broader format semantics remain open.

Selected `Int32.ToString` standard formats D, N, x, B, C, F, P and E now support precision 2049. Eight .NET 10 vectors check one negative value across those formats against a packaged external consumer. The implementation guards remain bounded at 4096; higher precision and broader format semantics remain open.

Selected `Decimal.ToString("F", provider)` now accepts explicit precision 100 and 101. Six .NET 10 vectors check positive, negative and zero values with custom number decimal separator and sign against a packaged external consumer. Explicit precision above 4096 and broader Decimal format semantics remain open.

Selected `Decimal.ToString("N", provider)` now accepts explicit precision 100 and 101. Six .NET 10 vectors check positive, negative and zero values against a packaged external consumer. Explicit precision above 4096 and broader Decimal number semantics remain open.

Selected `Decimal.ToString("P", provider)` now accepts explicit precision 100 and 101. Six .NET 10 vectors check positive, negative and zero values against a packaged external consumer. Explicit precision above 4096 and broader Decimal percent semantics remain open.

Selected `Decimal.ToString("C", provider)` now accepts explicit precision 100 and 101. Six .NET 10 vectors check positive, negative and zero values against a packaged external consumer. Explicit precision above 4096 and broader Decimal currency semantics remain open.

Selected `Decimal.ToString("E", provider)` now accepts explicit precision 100 and 101. Six .NET 10 vectors check positive, negative and zero values against a packaged external consumer. Explicit precision above 4096 and broader Decimal exponential semantics remain open.

Selected `Decimal.ToString` standard formats F, N, P, C and E now report `FormatException` for explicit precision strings that exceed Java integer parsing. Ten .NET 10 vectors check two oversized strings across all five formats against a packaged external consumer. Other format error cases remain open.

Selected `Decimal.ToString` standard formats F, N, P, C and E now have precision-1024 comparison evidence. Ten .NET 10 vectors check positive and negative fractional values in all five formats against a packaged external consumer. Explicit precision above 4096 and broader Decimal format semantics remain open.

Selected `Decimal.ToString` standard formats F, N, P, C and E now support precision 4097. Five .NET 10 vectors check one negative fractional value across all five formats against a packaged external consumer. The implementation guards remain bounded at 8192; higher precision and broader Decimal semantics remain open.

Selected `Decimal.ToString` formats F, N, P, C and E accept explicit precision 100 with both six-digit and thirty-two-digit leading-zero spellings. Ten .NET 10 vectors check exact text against a packaged external consumer. Other precision syntax and culture behavior remain open.

Selected `Int32.ToString` formats D, N, x, B, C, F, P and E accept explicit precision 100 with both six-digit and thirty-two-digit leading-zero spellings. Sixteen .NET 10 vectors check exact text against a packaged external consumer. Other precision syntax and culture behavior remain open.

Selected `Int32.ToString("G"/"g", provider)` now honors explicit significant-digit precision, including scientific notation, rounding, exponent letter case and custom provider signs/separator. One hundred eight .NET 10 vectors cover nine signed, zero and midpoint values at six precisions in both cases; a packaged external consumer checks exact text. Broader general-format cases remain open.

Selected `Int32.ToString("G"/"g", provider)` now also has extrema and power-of-ten rounding evidence. Forty-eight .NET 10 vectors cover six values at four precisions in both cases; a packaged external consumer checks exact text. Broader general-format cases remain open.

Selected `Int32.ToString("R"/"r", provider)` now accepts both round-trip specifier cases. Ten .NET 10 vectors cover minimum, maximum, zero and signed values with a custom negative sign; a packaged external consumer checks exact text. Other format behavior remains open.

Selected `Int32.ToString("R"/"r", provider)` now also honors explicit significant-digit precision. Sixteen .NET 10 vectors cover 0, 1, 2 and 10 digits in both letter cases, including scientific notation and custom signs; a packaged external consumer checks exact text. Broader round-trip format cases remain open.

Selected `Decimal.ToString("G"/"g", provider)` now supports explicit significant-digit precision, including `G0`, fixed/scientific selection, rounding, exponent letter case and provider symbols. Eighty-four .NET 10 vectors cover six Decimal bit patterns at seven precision states in both cases; a packaged external consumer checks exact text. Plain `G` retains the prior stored-scale behavior, while `G0` removes trailing zeros. Broader general-format cases remain open.

Selected `Decimal.ToString("G"/"g", provider)` now also has midpoint-rounding and fixed/scientific boundary evidence. Forty-two .NET 10 vectors cover seven Decimal bit patterns at three precisions in both cases; a packaged external consumer checks exact text. Broader general-format cases remain open.

Selected `Decimal.ToString("R"/"r", provider)` now accepts both round-trip specifier cases and explicit precision 0 and 1. Thirty .NET 10 vectors cover five Decimal bit patterns across six spellings, including stored trailing zeros and scientific text; a packaged external consumer checks exact text. Broader round-trip format cases remain open.

Selected `Decimal.ToString("G"/"R", provider)` now also has minimum, maximum and scale-28 magnitude evidence. Twenty-four .NET 10 vectors cover four extreme Decimal bit patterns at precisions 0, 1 and 10; a packaged external consumer checks exact text. Broader formatting behavior remains open.

Selected `Decimal.ToString("G"/"R", provider)` now also has negative-zero and stored-scale evidence. Forty .NET 10 vectors cover five Decimal bit patterns across plain and explicit precision formats; a packaged external consumer checks exact text. Broader formatting behavior remains open.

Selected `Int32` and `Decimal` formatting now recognizes `G-1`, `g-1`, `R-1`, `r-1`, `Gx` and `Rx` as custom literal formats with provider negative signs. Four oversized numeric precision spellings still report `FormatException`. Forty .NET 10 vectors cover both signs and both types; a packaged external consumer checks text and exception classes. Broader custom format grammar remains open.

Selected `Int32` and `Decimal` formatting now recognizes letter-only custom format strings of length two or more as literals, including `abc`, `xyz`, `Qx`, `hello`, `GG`, `RR`, `ee` and `FF`. Thirty-two .NET 10 vectors cover both signs and both types with provider negative signs; a packaged external consumer checks exact text. Broader custom format grammar remains open.

Selected `Int32` and `Decimal` formatting now recognizes a one-character backslash escape and whole single- or double-quoted custom literals. Thirty-two .NET 10 vectors cover eight escaped or quoted spellings, both signs and both types with provider negative signs; a packaged external consumer checks exact text. Broader custom format grammar remains open.

Selected `Int32` and `Decimal` formatting now supports three quoted-text forms around one mandatory digit: `'item '0`, `0' units'` and `'['0']'`. Eighteen .NET 10 vectors cover negative, zero and positive values for both types with provider negative signs; a packaged external consumer checks exact text. Broader mixed numeric/literal grammar remains open.

Selected `Int32` and `Decimal` formatting now supports `0\Q`, `0\%`, `0\G` and `\Q0` escaped numeric forms. Twenty-four .NET 10 vectors cover negative, zero and positive values with provider negative signs; a packaged external consumer checks exact text. Broader escaped numeric grammar remains open.

Selected `Int32` and `Decimal` formatting now supports three positive, negative and zero custom sections: `0;(0);'zero'`, `0;[0];'none'` and `0;'minus '0;'zero'`. Eighteen .NET 10 vectors check section selection and rounding through a packaged external consumer. Broader custom section grammar remains open.

Selected `Int32` and `Decimal` formatting now supports `0.0`, `0.00` and `0.##` decimal-place custom formats with provider decimal separators and negative signs. Eighteen .NET 10 vectors cover negative, zero and positive values through a packaged external consumer. Broader decimal-place custom grammar remains open.

Selected `Decimal` formatting now supports `0.###` alongside `0.##` and `0.00` rounding boundaries. Twenty-seven .NET 10 vectors cover negative and positive ties, near-zero values and custom separators through a packaged external consumer. Broader optional decimal-place grammar remains open.

Selected `Decimal` formatting now supports four and five optional decimal places via `0.####` and `0.#####`. Eighteen .NET 10 vectors cover ties and near-zero rounding with provider separators through a packaged external consumer. Broader optional decimal-place grammar remains open.

Selected `Decimal` formatting now supports six and ten optional decimal places. Eighteen .NET 10 vectors cover high-precision rounding, ties and near-zero values with provider separators through a packaged external consumer. Broader optional decimal-place grammar remains open.

Selected `Decimal` formatting now supports twelve and twenty-eight optional decimal places. Eighteen .NET 10 vectors cover full scale 28 values, signed tiny values and rounding to zero with provider separators through a packaged external consumer. Broader optional decimal-place grammar remains open.

Selected `Decimal` formatting now supports three and four mandatory decimal places via `0.000` and `0.0000`. Eighteen .NET 10 vectors cover ties, near-zero rounding and provider separators through a packaged external consumer. Broader mandatory decimal-place grammar remains open.

Selected `Decimal` formatting now supports twenty-eight and thirty-two mandatory decimal places. Eighteen .NET 10 vectors cover full scale 28 values, tiny signed values and zero padding with provider separators through a packaged external consumer. Broader mandatory decimal-place grammar remains open.

Selected `Int32` formatting now supports mandatory custom fractional places from one through thirty-two, including pinned three, four, six and twenty-eight place forms. Twelve .NET 10 vectors cover negative, zero and positive values with provider separators through a packaged external consumer. Broader Int32 custom decimal grammar remains open.

Selected `Int32` formatting now supports one through twenty-eight optional fractional placeholders. Fifteen .NET 10 vectors cover both 32-bit extrema, negative, zero and positive values with provider negative signs through a packaged external consumer. Broader Int32 custom decimal grammar remains open.

Selected `Int32` custom zero padding now uses the provider negative sign. Fifteen .NET 10 vectors cover two, three and five digit patterns across extrema, negative, zero and positive values through a packaged external consumer. Broader custom digit grammar remains open.

Selected `Decimal` custom zero padding now rounds to integer digits and uses the provider negative sign. Fifteen .NET 10 vectors cover two, three and five digit patterns with positive, negative and rounded-zero values through a packaged external consumer. Broader custom digit grammar remains open.

Selected `Int32` and `Decimal` formatting now supports one through three optional integer placeholders, including empty output for zero. Eighteen .NET 10 vectors cover both signs and zero with provider negative signs through a packaged external consumer. Broader optional integer grammar remains open.

Selected `Int32` and `Decimal` formatting now supports mixed mandatory and optional integer placeholders: `#0`, `0#`, `##0` and `0##`. Twenty-four .NET 10 vectors cover sign, zero, padding and rounding through a packaged external consumer. Broader mixed integer grammar remains open.

Selected `Int32` and `Decimal` formatting now supports `#,##0` and `#,##0.00` with provider group and decimal separators. Twelve .NET 10 vectors cover negative, zero and positive values through a packaged external consumer. Broader grouping grammar remains open.

Selected custom grouped `Int32` and `Decimal` formats now use a leading provider negative sign independently of `NumberNegativePattern`. Twenty .NET 10 vectors cover all five patterns for `#,##0` and `#,##0.00` through a packaged external consumer. Broader grouping grammar remains open.

Selected custom `Int32` and `Decimal` grouping now supports provider group sizes of `[2]`, `[3,2]` and `[4]` for `#,##0`, `#,##0.00` and `#,##0.000`. Eighteen .NET 10 vectors cover negative values and rounding through a packaged external consumer. Broader grouping grammar remains open.

Selected custom `Int32` and `Decimal` grouping now supports terminal-zero group sizes `[3,0]`, `[2,0]` and `[3,2,0]` for `#,##0` and `#,##0.0000`. Twelve .NET 10 vectors cover negative values and rounding through a packaged external consumer. Broader grouping grammar remains open.

Selected grouped `Int32` and `Decimal` custom formats now support five and six mandatory fractional places. Twelve .NET 10 vectors cover signs, zero, provider separators and rounding through a packaged external consumer. Broader grouped custom precision remains open.

Selected grouped `Int32` and `Decimal` custom formats now support ten and twenty-eight mandatory fractional places. Twelve .NET 10 vectors cover signs, zero, provider separators, padding and rounding through a packaged external consumer. Broader grouped custom precision remains open.

Selected grouped `Int32` and `Decimal` custom formats now support one, three and ten optional fractional placeholders. Eighteen .NET 10 vectors cover signs, zero, provider separators and trailing-zero removal through a packaged external consumer. Broader grouped optional-fraction grammar remains open.

Selected grouped `Decimal` optional-fraction formatting now covers two and twenty-eight places at ties and near-zero boundaries. Eighteen .NET 10 vectors verify rounding and sign removal after rounding to zero through a packaged external consumer. Broader grouped optional-fraction grammar remains open.

Selected grouped `Int32` and `Decimal` custom formatting now covers `#,##0.0` and a twenty-eight-place optional pattern at numeric extrema. Twelve .NET 10 vectors cover minima, maxima and zero with provider separators through a packaged external consumer. Broader grouped custom grammar remains open.

Selected `Decimal` custom and grouped formatting now handles stored negative zero at scales zero, two and twenty-eight like positive zero. Twenty-five .NET 10 vectors cover `0` and four grouped patterns through a packaged external consumer. Broader signed-zero custom grammar remains open.

Selected grouped `Int32` and `Decimal` custom formats now support mixed mandatory and optional fractional placeholders in `#,##0.0#` and `#,##0.00##`. Twelve .NET 10 vectors cover signs, zero and trailing-zero preservation through a packaged external consumer. Broader mixed fractional grammar remains open.

Selected grouped `Decimal` mixed-fraction formatting now supports three and four required digits followed by three and four optional digits. Eighteen .NET 10 vectors cover ties and near-zero rounding through a packaged external consumer. Broader mixed fractional grammar remains open.

Selected grouped `Decimal` mixed-fraction formatting now supports ten required plus ten optional places and fourteen required plus fourteen optional places. Eighteen .NET 10 vectors cover scale twenty-eight values, tiny signed values and zero through a packaged external consumer. Broader mixed fractional grammar remains open.

Selected ungrouped `Int32` and `Decimal` custom formats now support mixed mandatory and optional fractional placeholders in `0.0#`, `0.00##` and `0.000###`. Eighteen .NET 10 vectors cover signs, zero and trailing-zero preservation through a packaged external consumer. Broader mixed fractional grammar remains open.

Selected ungrouped `Decimal` custom formatting now supports `0.#` and mixed mandatory/optional rounding near zero. Eighteen .NET 10 vectors cover ties, zero and provider separators through a packaged external consumer. Broader ungrouped mixed fractional grammar remains open.

Selected `Int32` and `Decimal` custom percent formatting now distinguishes scaled `0%` and `0.0%` from escaped `0\%`. Eighteen .NET 10 vectors cover signs, zero, rounding and provider decimal separators through a packaged external consumer. Broader custom percent grammar remains open.

Selected custom percent formatting now uses `NumberFormatInfo.PercentSymbol` for scaled percent placeholders while `0\%` keeps a literal percent sign. Eighteen .NET 10 vectors cover `Int32` and `Decimal` with a custom symbol through a packaged external consumer. Broader custom percent grammar remains open.

Selected custom percent formatting now supports two mandatory or two optional fractional places using the provider percent symbol. Twelve .NET 10 vectors cover `Int32` and `Decimal` signs, zero and trailing-zero behavior through a packaged external consumer. Broader custom percent precision remains open.

Selected custom `Decimal` percent formatting now supports optional fractional precision through twenty-eight places. Eighteen .NET 10 vectors cover ties, near-zero rounding and provider percent symbols through a packaged external consumer. Broader custom percent precision remains open.

Selected custom `Int32` and `Decimal` percent formatting now supports mixed required and optional fractional places in `0.0#%` and `0.00##%`. Twelve .NET 10 vectors cover signs, zero and provider percent symbols through a packaged external consumer. Broader custom percent grammar remains open.

Selected custom `Decimal` percent mixed-fraction formatting now has eighteen pinned rounding vectors for `0.000###%` and `0.0000####%`. They cover ties and near-zero values with a provider percent symbol through a packaged external consumer. Broader custom percent grammar remains open.

Selected custom `Decimal` percent mixed-fraction formatting now supports twenty required plus twenty optional places and thirty required plus thirty optional places. Eighteen .NET 10 vectors cover scale twenty-eight values, tiny signed values and zero through a packaged external consumer. Broader custom percent grammar remains open.

Selected `Int32` and `Decimal` custom grouped percent formatting now supports `#,##0%` and `#,##0.00%` with provider group sizes and percent symbols. Twelve .NET 10 vectors cover signs, zero and rounding through a packaged external consumer. Broader grouped percent grammar remains open.

Selected custom grouped percent formatting keeps its leading provider negative sign across five `NumberNegativePattern` and `PercentNegativePattern` settings. Twenty .NET 10 vectors cover `Int32` and `Decimal` through a packaged external consumer. Broader grouped percent grammar remains open.

Selected grouped custom `Int32` and `Decimal` percent formatting now supports three required or three optional fractional places with provider group sizes and percent symbols. Twelve .NET 10 vectors cover signs, zero and trailing-zero behavior through a packaged external consumer. Broader grouped percent grammar remains open.

Selected grouped `Decimal` percent formatting has fourteen pinned rounding vectors at three required or optional fractional places. They cover positive and negative values near a fractional boundary and small nonzero values through a packaged external consumer. Broader grouped percent rounding remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports mixed required and optional fractional places in `#,##0.0#%` and `#,##0.00##%`. Twelve .NET 10 vectors cover signs, zero, provider grouping and percent symbols through a packaged external consumer. Broader grouped percent grammar remains open.

Selected grouped `Decimal` mixed-percent formatting has fourteen pinned rounding vectors across two mixed placeholder patterns. They cover positive and negative boundary values and small nonzero values through a packaged external consumer. Broader grouped percent rounding remains open.

Selected grouped `Decimal` percent formatting now supports twenty or thirty required places followed by the same number of optional places. Eighteen .NET 10 vectors cover scale twenty-eight values, tiny signed values and zero through a packaged external consumer. Broader grouped percent grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for two provider group-size sequences. They cover signs, zero, grouping and the custom percent symbol through a packaged external consumer. Broader provider grouping combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for zero-terminated provider group sizes. They cover signs, zero and the stop-grouping rule through a packaged external consumer. Broader provider grouping combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for two-character provider group and decimal separators. They cover required and mixed optional digits through a packaged external consumer. Broader provider separator combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for an empty provider percent symbol. They cover signs, zero and required fractional places through a packaged external consumer. Broader provider symbol combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for an empty provider group separator with two group sizes. They cover signs, zero and required fractional places through a packaged external consumer. Broader provider separator combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for a multi-character provider negative sign. They cover two fractional patterns and all signs through a packaged external consumer. Broader provider sign combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has eighteen pinned vectors for three input digit widths. They cover grouping onset, signs and mixed fractional placeholders through a packaged external consumer. Broader width combinations remain open.

Selected grouped `Int32` percent formatting now has eighteen pinned vectors for both integer range endpoints, near-zero values and three grouped percent patterns. They run through a packaged external consumer. Broader integral formatting combinations remain open.

Selected grouped `Decimal` percent formatting now has eighteen pinned vectors for both decimal range endpoints, tiny nonzero values and two grouped percent patterns. They run through a packaged external consumer. Broader decimal formatting combinations remain open.

Selected grouped `Int32` and `Decimal` mixed-percent formatting now has twenty pinned vectors across five negative-pattern settings. They verify provider pattern interaction through a packaged external consumer. Broader grouped percent pattern combinations remain open.

Selected grouped `Decimal` percent formatting now has eighteen pinned vectors for zero, signed zero and small values that round to zero or retain optional digits. They run through a packaged external consumer. Broader zero-formatting combinations remain open.

Selected grouped `Decimal` percent formatting now has eighteen pinned vectors at twenty required or twenty optional fractional places. They cover tiny values around the rounding boundary and scale twenty-eight values through a packaged external consumer. Broader high-precision formatting remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports a quoted alphabetic prefix or suffix around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader literal grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports paired quoted alphabetic prefix and suffix literals around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader literal grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports one escaped alphabetic prefix or suffix character around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader escape grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports paired escaped alphabetic prefix and suffix characters around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader escape grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports a quoted literal on one side and an escaped character on the other around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader mixed literal grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports quoted punctuation around `#,##0.00%`. Twelve .NET 10 vectors cover bracket and parenthesis affixes across signs and zero through a packaged external consumer. Broader quoted literal grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for spaces inside quoted prefix and suffix literals. They cover signs, zero and provider symbols through a packaged external consumer. Broader quoted literal grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for digits inside quoted prefix and suffix literals. They cover signs, zero and provider symbols through a packaged external consumer. Broader quoted literal grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports escaped exclamation, question-mark and parenthesis affixes around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader escape grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports escaped digit affixes around `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader escape grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports an escaped space before or after `#,##0.00%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader escape grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports quoted affixes around `#,##0.0#%` and `#,##0.###%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader affixed custom percent grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports escaped affixes around `#,##0.0#%` and `#,##0.###%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader affixed custom percent grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports quoted or escaped affixes around no-fraction `#,##0%`. Twelve .NET 10 vectors cover signs, zero and provider symbols through a packaged external consumer. Broader affixed custom percent grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for quoted or escaped affixes with a multi-character provider negative sign. They cover sign placement, zero and provider symbols through a packaged external consumer. Broader affix and sign combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for quoted or escaped affixes with a custom or empty provider percent symbol. They cover signs and zero through a packaged external consumer. Broader affix and symbol combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve pinned vectors for quoted or escaped affixes with two provider group-size sequences. They cover signs, zero and stop-grouping behavior through a packaged external consumer. Broader affix and grouping combinations remain open.

Selected grouped `Decimal` percent formatting now has eighteen pinned rounding vectors for quoted or escaped affixes around mixed or optional fractional patterns. They cover signed values near rounding boundaries through a packaged external consumer. Broader affixed rounding remains open.

Selected grouped `Decimal` percent formatting now has eighteen pinned vectors for quoted or escaped affixes at both decimal range endpoints and tiny nonzero values. They run through a packaged external consumer. Broader affixed extreme-value formatting remains open.

Selected grouped `Decimal` percent formatting now has eighteen pinned vectors for quoted or escaped affixes around zero, signed zero and tiny values. They run through a packaged external consumer. Broader affixed zero-formatting behavior remains open.

Selected grouped `Decimal` percent formatting now supports affixed patterns with twenty or thirty required places followed by the same number of optional places. Eighteen .NET 10 vectors cover scale twenty-eight and tiny signed values through a packaged external consumer. Broader affixed precision grammar remains open.

Selected grouped `Decimal` percent formatting now has eighteen pinned rounding vectors at twenty required or optional fractional places with quoted or escaped affixes. They cover tiny boundary values through a packaged external consumer. Broader affixed high-precision rounding remains open.

Selected grouped `Decimal` percent formatting now supports mixed quoted and escaped affixes around twenty or thirty required places followed by optional places. Eighteen .NET 10 vectors cover tiny and scale twenty-eight values through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Decimal` percent formatting now has eighteen .NET 10 rounding vectors for mixed quoted and escaped affixes around required and optional fractional places. They cover positive and negative rounding boundaries through a packaged external consumer. Broader mixed affix rounding remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for mixed quoted and escaped affixes with a custom or empty provider percent symbol. They cover both signs and zero through a packaged external consumer. Broader mixed affix and symbol combinations remain open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for mixed quoted and escaped affixes with two provider group-size sequences. They cover both signs, zero and stop-grouping behavior through a packaged external consumer. Broader mixed affix grouping remains open.

Selected grouped `Decimal` percent formatting now has eighteen .NET 10 vectors for mixed quoted and escaped affixes at both decimal range endpoints and tiny signed values. They run through a packaged external consumer. Broader mixed affix extreme-value formatting remains open.

Selected grouped `Decimal` percent formatting now has eighteen .NET 10 vectors for mixed quoted and escaped affixes around zero, signed zero and tiny values. They run through a packaged external consumer. Broader mixed affix zero formatting remains open.

Selected grouped `Decimal` percent formatting now has eighteen .NET 10 high-precision rounding vectors for mixed quoted and escaped affixes. They cover twenty required or optional fractional places and tiny boundary values through a packaged external consumer. Broader mixed affix high-precision behavior remains open.

Selected grouped `Int32` and `Decimal` percent formatting now supports punctuation in mixed quoted and escaped affixes. Twelve .NET 10 vectors cover signs and zero through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for digit literals in mixed quoted and escaped affixes. They cover both signs and zero through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for whitespace literals in mixed quoted and escaped affixes. They cover both signs and zero through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for parentheses literals in mixed quoted and escaped affixes. They cover both signs and zero through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for exclamation literals in mixed quoted and escaped affixes. They cover both signs and zero through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for question-mark literals in mixed quoted and escaped affixes. They cover both signs and zero through a packaged external consumer. Broader mixed affix grammar remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for mixed quoted and escaped affixes with a multi-character provider negative sign. They cover both signs and zero through a packaged external consumer. Broader mixed affix sign behavior remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for mixed quoted and escaped affixes with an empty provider negative sign. They cover positive, negative and zero values through a packaged external consumer. Broader mixed affix sign behavior remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twenty .NET 10 vectors for mixed quoted and escaped affixes across provider negative patterns zero through four. They run through a packaged external consumer. Broader mixed affix negative-pattern behavior remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for mixed quoted and escaped affixes with multi-character provider group and decimal separators. They cover both signs and zero through a packaged external consumer. Broader mixed affix separator behavior remains open.

Selected grouped `Int32` and `Decimal` percent formatting now has twelve .NET 10 vectors for mixed quoted and escaped affixes with an empty provider group separator. They cover both signs and zero through a packaged external consumer. Broader mixed affix separator behavior remains open.

`NumberFormatInfo.NumberDecimalSeparator` now rejects an empty string with `ArgumentException` and parameter `value`, matching .NET 10. The packaged consumer checks the exception and parameter. This boundary was found while probing mixed-affix provider separators.

`NumberFormatInfo.CurrencyDecimalSeparator` now rejects an empty string with `ArgumentException` and parameter `value`, matching .NET 10. The packaged consumer checks the exception and parameter.

`NumberFormatInfo.PercentDecimalSeparator` now rejects an empty string with `ArgumentException` and parameter `value`, matching .NET 10. The packaged consumer checks the exception and parameter.

`NumberFormatInfo.NumberGroupSeparator` now has pinned .NET 10 and packaged Java checks for an accepted empty string and a null `ArgumentNullException` with parameter `value`. Other separator boundaries remain open.

`NumberFormatInfo.CurrencyGroupSeparator` now has pinned .NET 10 and packaged Java checks for an accepted empty string and a null `ArgumentNullException` with parameter `value`. Other separator boundaries remain open.

`NumberFormatInfo.PercentGroupSeparator` now has pinned .NET 10 and packaged Java checks for an accepted empty string and a null `ArgumentNullException` with parameter `value`. Other separator boundaries remain open.

All three `NumberFormatInfo` decimal-separator setters now have pinned .NET 10 and packaged Java null checks: each throws `ArgumentNullException` with parameter `value`. Other provider setter boundaries remain open.

`NumberFormatInfo.PositiveSign` and `NegativeSign` now have pinned .NET 10 and packaged Java checks for accepted empty strings and null `ArgumentNullException` results with parameter `value`. Other provider setter boundaries remain open.

`NumberFormatInfo.CurrencySymbol` now has pinned .NET 10 and packaged Java checks for an accepted empty string and a null `ArgumentNullException` with parameter `value`. Other symbol boundaries remain open.

`NumberFormatInfo.PercentSymbol` now has pinned .NET 10 and packaged Java checks for an accepted empty string and a null `ArgumentNullException` with parameter `value`. Other symbol boundaries remain open.

`NumberFormatInfo.PerMilleSymbol` now exposes the .NET 10 default U+2030 symbol, accepts an empty string, and rejects null with `ArgumentNullException` and parameter `value`. The packaged consumer checks each boundary. Per-mille custom formatting remains open.

Selected `Int32` and `Decimal` custom `0‰` formatting now scales by one thousand and uses the provider negative sign and per-mille symbol. Twelve .NET 10 vectors cover signed integers, decimal rounding boundaries, and zero through a packaged consumer. Grouped and fractional per-mille patterns remain open.

Selected `Int32` and `Decimal` custom `0‰` formatting now has twelve .NET 10 vectors for a custom or empty provider `PerMilleSymbol` across both signs and zero. The packaged consumer checks the provider symbol path. Broader per-mille grammar remains open.

Selected `Int32` and `Decimal` per-mille formatting now supports `0.00‰` and `0.##‰` with provider decimal separator, negative sign, and per-mille symbol. Twenty-four .NET 10 vectors cover signed values, zero, and decimal rounding through a packaged consumer. Grouped per-mille patterns remain open.

Selected `Int32` and `Decimal` per-mille formatting now supports `#,##0‰` and `#,##0.00‰` with provider grouping, decimal separator, sign and per-mille symbol. Twelve .NET 10 vectors cover both signs and zero through a packaged consumer. Broader grouped per-mille grammar remains open.

Selected grouped `Decimal` per-mille formatting now has eighteen .NET 10 vectors for optional and mixed fractional placeholders, signed rounding boundaries, and zero through a packaged consumer. Broader grouped per-mille precision remains open.

Selected grouped `Decimal` per-mille formatting now has eighteen .NET 10 vectors for twenty or thirty required places followed by optional places. They cover tiny signed values and scale twenty-eight through a packaged consumer. Broader grouped per-mille precision remains open.

Selected grouped `Int32` and `Decimal` per-mille formatting now has twelve .NET 10 vectors for two provider group-size sequences, including stop grouping. They cover both signs and zero through a packaged consumer. Broader grouping combinations remain open.
