# DateTime selected representation ledger

| CLR concept | Java candidate | Qualification |
|---|---|---|
| Tick value and Kind | Immutable LocalDateTime and DateTimeKind; existing AddTicks and SpecifyKind construct selected values | Full value, calendar, timezone and language integration remain open |
| Comparison and equality | Static, typed, object/interface and Java equality/hash hooks | Pinned extrema, day boundaries and all three Kind values; boxed wrong-type errors match type, HRESULT and null ParamName |
| Null in object overloads | Object CompareTo(null) returns one and Equals(null) returns false | Typed null is a Java carrier boundary outside the CLR value domain |

The product uses JDK APIs only. Pinned .NET and Python/JDK scripts provide development evidence. Broader project dependency resolution and distribution remain open. These selected checks close no implementation task, E01 decision or framework qualification.

Batch-2022 also corrects Batch-2021's recorded plan scope to DJ-001-WP-01-T1, which covers exception-cause mapping; acceptance totals are unchanged.
