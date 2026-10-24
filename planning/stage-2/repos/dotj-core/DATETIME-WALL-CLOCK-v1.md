# Selected DateTime wall-clock candidate

Plan scope: `DJ-001-WP-05-T3`, in progress. No implementation-task acceptance credit is granted.

| Contract | Candidate mapping | Qualification boundary |
|---|---|---|
| DateTime.UtcNow | Static `get_UtcNow()` reads the JDK UTC wall clock, truncates nanoseconds to 100 ns ticks and returns Utc Kind | Clock source precision, leap-second/platform details and all host configurations are unqualified |
| DateTime.Now | Static `get_Now()` converts the current UTC value through the existing JDK system-zone mapping and returns Local Kind | Windows and JDK zone identifiers can differ; DST ambiguity and hidden CLR local-state bits remain open |
| DateTime.Today | Static `get_Today()` retains Local Kind and selects local midnight from Now | Paired validation accepts either native midnight boundary across a date transition |
| Monotonic deadlines | No DateTime wall-clock value is defined as a monotonic deadline source | Monotonic implementation and qualification remain open |

The external packaged consumer runs between pinned .NET 10.0.12 property reads. Twenty-four host samples check clock envelopes, Kind and date/time decomposition. The evidence records both native and Java zone identifiers, actual clock values, JAR and consumer hashes, and the pinned CoreLib/Java executable hashes. Wall-clock reads may move backwards; the evidence records that condition and does not assert monotonicity.

This live host check supplies bounded evidence rather than a fixed timestamp golden file. Separate modern DST evidence samples 2024/2026 W. Europe/Zurich transitions, overlap-state retention, direct gap/overlap conversion and daylight queries. Selected file-time and binary evidence also checks modern import/export, overlap retention and subsequent arithmetic. These records include the Windows zone serialization hash and JDK zone-rules version; they do not qualify arbitrary or historical zone rules or full-range boundary saturation.

The binary corpus separately retains two historical Local encodings, including `-1`. These test native validity, Kind and normalized binary values only. Their exact local ticks are outside the qualified comparison scope because Windows and JDK historical timezone rules differ. This also corrects the earlier consumer's assumption that every negative binary value was invalid.

Arbitrary cultures/zones, precise clock resolution, complete native API mapping, source-language lowering and E01/E02/E03/N01 release qualification remain open. The product uses JDK APIs only; the pinned .NET runtime and PowerShell are validation tools.

Selected saturation evidence covers UTC/local conversion endpoints and file-time imports. Four negative-offset cases use native TimeZoneInfo converter calls for America/New_York, with the reference member, input Kind and output Kind retained separately from the candidate DateTime carrier. In particular, the native nonlocal-zone converter returns Unspecified while the candidate ToLocalTime contract returns Local. This is an explicitly bounded alternative behavior oracle, not proof of exact native member equivalence for that zone. Six historical results check Kind and normalized UTC/binary only; exact historical local tick parity remains open.
