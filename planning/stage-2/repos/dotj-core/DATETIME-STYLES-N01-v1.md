# Selected DateTimeStyles and ISO parsing

Batch 2073 advances `DJ-001-WP-05-T1`; no implementation task or release gate is accepted.

The immutable Int32 DateTimeStyles carrier exposes ten named native values and Java FromInt32/Or/value/name adapters. Arbitrary numeric values are retained for native validation. Logical Type identity, base/value/enum flags, names and underlying values are mapped; full enum formatting/interfaces and language identity remain open.

Four style-bearing CLR signatures are added: String and Character-view Parse/TryParse with provider and styles. Existing provider/default adapters select None. The selected ISO parser now accepts Z/z and numeric HH:mm offsets, enforces the selected native fourteen-hour offset limit, and applies AssumeLocal, AssumeUniversal, AdjustToUniversal and RoundtripKind. Modern local conversion retains overlap state. Whitespace/default-date flags are accepted for the selected full-date grammar; this does not implement all native whitespace or time-only grammars.

Invalid bits and incompatible assumptions/RoundtripKind combinations throw ArgumentException with styles before input/output changes. Valid failed TryParse resets to default DateTime; invalid styles preserve the seeded output. Java null style/view carriers and out-array storage are host adaptations outside CLR enum/span/out domains. Null String arguments require an explicit String cast when Java overload selection is ambiguous.

The pinned CoreLib 10.0.12 oracle records 1,514 native String/span cases, including every 0–255 style combination on a modern anchor, invalid numeric values, selected ISO errors, fractions, gaps/folds and offsets. The packaged consumer passes 4,543 groups through String and zero/offset Character views, checking ticks/Kind, selected modern binary/UTC state, exception identity/HResult/parameters and out state. The public signature preview also passes. The explicit source/class map and standalone Type/typeof build dependencies include the new product carrier.

Full-range scalar cases avoid historical local conversion comparisons. Other zones, historical Local offsets, culture/providers, exact-format style overloads, complete ISO/general grammar, allocation/byref/language semantics and release qualification remain open. Product runtime dependencies remain JDK-only.
