# DateTime selected representation ledger

| CLR concept | Java candidate | Qualification |
|---|---|---|
| Tick value and Kind | Immutable LocalDateTime and DateTimeKind; existing AddTicks and SpecifyKind construct selected values | Full value, calendar, timezone and language integration remain open |
| Comparison and equality | Static, typed, object/interface and Java equality/hash hooks | Pinned extrema, day boundaries and all three Kind values; boxed wrong-type errors match type, HRESULT and null ParamName |
| Null in object overloads | Object CompareTo(null) returns one and Equals(null) returns false | Typed null is a Java carrier boundary outside the CLR value domain |
| Tick construction and zero initialization | long and long/Kind constructors validate the CLR tick range; no-argument constructor represents default(DateTime) | Valid Kind values and selected range boundaries only; invalid numeric enum values lack a Java enum carrier |
| MinValue, MaxValue and UnixEpoch | Three public static final immutable values with pinned ticks and Kind | Selected field projection, not identical CLR readonly/value-type metadata; component constructors and other creation paths remain separately unqualified |
| Gregorian component construction | Seven non-Calendar signatures, including millisecond/microsecond and Kind overloads; explicit year bounds and managed range exceptions | Pinned one-component and combined-error vectors preserve date/time-before-subsecond validation; alternate calendars, platform leap-second support, invalid numeric Kind and complete constructor qualification remain open |
| DayOfWeek, Date and TimeOfDay | Gregorian weekday and positive tick remainder; midnight Date retains Kind | Pinned extrema and seven consecutive weekdays in five centuries; no timezone conversion or full calendar qualification implied |
| DayOfWeek and DateTimeKind enum projection | Exact CLR names and selected integer values represented by Java enum ordinals; Type lookup, enum names/values and underlying Int32 projection | Selected declared values and query cases only; arbitrary numeric enum carriers and full CLR enum/language semantics remain open |
| Floating-unit addition | Six unit methods accumulate whole units exactly and truncate fractional ticks toward zero; pinned maximum-unit range and Kind retention | Selected IEEE-bit inputs, subticks, NaN, infinities and endpoint neighbors only; wall-clock/DST and full arithmetic qualification remain open |

The product uses JDK APIs only. Pinned .NET and Python/JDK scripts provide development evidence. Broader project dependency resolution and distribution remain open. These selected checks close no implementation task, E01 decision or framework qualification.

Batch-2022 also corrects Batch-2021's recorded plan scope to DJ-001-WP-01-T1, which covers exception-cause mapping; acceptance totals are unchanged.
