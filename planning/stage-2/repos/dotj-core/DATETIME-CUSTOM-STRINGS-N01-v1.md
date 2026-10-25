# Selected invariant custom DateTime strings

Batch 2076 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

Custom ToString formatting now handles invariant numeric and named year/month/day fields; 12/24-hour time, minutes, seconds and AM/PM; era; fixed/trimmed tick fractions; offset and Kind tokens; literal separators, unknown literal characters, quoted/escaped literals and percent custom-token selection. Repeated tokens use selected native widths. Invalid escapes, quotes, percent forms and fractions beyond seven digits throw FormatException. Trimmed empty fractions remove a preceding period.

The pinned CoreLib 10.0.12 oracle records 1770 native cases through three string routes. The packaged consumer checks 5310 groups through provider/single-format/IFormattable calls, including full scalar range and modern-zone offset text. Exception type and HResult are compared. Product public signatures are unchanged.

A separate clock-dependent rule was found in native time-only z formatting for ticks below one day: it uses the current local offset, including for UTC Kind. The implementation uses the current JDK local offset in that branch and tracks whether a date field has been emitted. The pinned source corroborates the rule. That volatile case is excluded from immutable native golden vectors; paired clock/timezone qualification remains open. Historical Local/Unspecified offset formatting is also excluded. This is an explicit limit of the differential coverage.

Custom buffer formatting mutation/exception behavior, provider/calendar/culture semantics, other zones and historical offsets, live time-only offset validation, complete language integration and foundation release acceptance remain open. Existing bounded buffer fixtures remain required; new custom string support does not qualify every buffer path. Product runtime dependencies remain JDK-only.
