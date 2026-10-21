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

Qualification remains open for the CLR value-type ABI, all untested values and overloads, generic numeric interfaces, native integer operations, and the remaining WP-05 numeric, text and time scope. This selected comparison is not a complete Int32 compatibility claim.
