# TimeSpan selected representation ledger v1

Reference: .NET 10.0.12, CoreLib SHA-256 `1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678`. The pinned [oracle](evidence/timespan-contract-v10.0.12.json) supplies metadata and bounded vectors. This ledger does not close N01 or qualify a public .j API.

| CLR concept | Current Java candidate representation | Qualification |
|---|---|---|
| Immutable value and zero initialization | Final class with final tick storage; zero constructor represents the zero-initialized CLR value | Full value-type, boxing, null and language lowering remain open |
| Public constants and readonly values | Same 25 public names, widths and values; primitive constants and immutable TimeSpan objects use static final fields | Selected field projection only; CLR field metadata categories are not identical |
| Property access | Existing CLR-style get_ accessor names | Source property lowering remains unqualified |
| Constant-format ToString and IFormattable | Exact overload names and interface dispatch; null/empty/c/t/T ignore providers as CLR does | General g/G, custom formats and culture/language integration remain open |
| Boxed comparison, equality and hashing | Object overloads and Java equals/hashCode hooks compared with pinned CLR outcomes | Selected ordering, value/hash results and exception type/ParamName only; typed null carriers remain outside the CLR value domain |
| Int32/Int64 single-unit factories | Exact int/long overload widths and checked integer ranges | Bounded pinned vector coverage only |
| Five composite integer factory declarations | Same full parameter widths, with exact intermediate accumulation before range checking | Bounded pinned vector coverage only |
| Omitted trailing zero defaults | Ten additional Java prefix overloads forward to the five full composite signatures | Syntax representation, not ten additional CLR declarations; oracle verifies actual CLR optional/default metadata before testing prefixes |
| TryParse out result | Existing one-element TimeSpan array carrier | Full out-parameter and invalid-carrier lowering remain open |

Composite arithmetic normalizes signed and out-of-unit-range components by their combined value. It uses JDK BigInteger for the bounded Int128 calculation domain rather than overflowing an intermediate long. Public component constructors retain their separately observed CLR arithmetic semantics; they are not reused as composite factory implementations.

Named arguments, operators, interfaces, full parsing/formatting/culture behavior, source-language integration and release rights remain open. A passing selected vector or candidate gate does not make this type or an implementation task accepted.
