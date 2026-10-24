# Selected TimeSpanStyles exact parsing candidate

Plan scope: `DJ-001-WP-05-T1`, in progress. No implementation task is accepted.

| Native concept | Selected Java carrier | Boundary |
|---|---|---|
| TimeSpanStyles Int32 enum | Immutable named None/AssumeNegative values; FromInt32 retains arbitrary values | FromInt32, values and numeric/name accessors are explicit Java adapters; full enum reflection/language behavior remains open |
| Style-bearing exact parsing | String or Char-view input, single String/Char-view format or String format array; ParseExact and TryParseExact | Eight style-bearing signatures use the existing selected parsing profiles and out-array carrier |
| Validation order | Invalid styles throw ArgumentException with ParamName styles before input checks and output reset | Direct CLR delegates retain the seeded output on failure; null Java style carriers are a host adaptation outside the native value-type domain |
| AssumeNegative | Negates custom-pattern magnitude, including the valid MinValue magnitude | Selected c/t/T and invariant g/G formats retain their native sign rules; non-null culture providers remain outside the general profile |

The oracle records 1,862 native String cases. Candidate verification applies them through 5,138 String and Character-view groups, with explicit input/format slices and format-array null/empty coverage. Character views reuse selected native String results; this does not qualify every CLR span lifetime, allocation or source-language behavior.

The source/class inventory explicitly includes the new carrier and the standalone Type/typeof build dependencies. Product runtime dependencies remain JDK-only.

Selected enum Type projection now maps class/array identity, enum/value/sealed flags, Enum base, Int32 underlying type/type code, declared names and values, underlying-value arrays, name/defined queries and selected relationships/instances. Ninety-two native groups include undefined Int32 carrier values and null/name error behavior. Returned name/value arrays are copied. Native enum interfaces are retained as omitted scope; their dispatch is not qualified by these Type queries.

Full enum reflection and interface dispatch, cultures/providers, runtime by-reference semantics, complete parsing profiles and E01/E02/E03/N01 release qualification remain open.
