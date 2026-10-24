# Selected invariant DateTime standard formats

Batch 2070 advances `DJ-001-WP-05-T1`; no implementation task is accepted.

The candidate now supports invariant d/D, f/F, g/G, m/M, t/T and y/Y text through format-only, format/provider and IFormattable paths. Date/time combinations reuse the existing selected Gregorian formatting methods, while month/day and year/month use fixed English invariant-profile names.

Char and UTF-8 array formatting preserve native partial writes when capacity is short: numeric/name chunks and literals are copied only as whole chunks, false returns zero written, and untouched buffer tails remain unchanged. Explicit G formatting uses these native chunks; the existing null/empty default formatting behavior remains independently tested. Name lengths come from the value's actual weekday/month within the selected profile.

The pinned CoreLib 10.0.12 oracle records 324 string cases across nine tick values, all three Kind values and twelve format characters, checking three native string routes. It also records 1,306 buffers across three representative dates and every capacity from zero through one past the required length, in Char and UTF-8. The packaged consumer passes 1,630 groups.

This is an invariant provider-null Java profile compared with native invariant culture/provider results. Batch 2071 separately adds selected round-trip/RFC/UTC profiles. Other cultures/providers/calendars, complete offset/round-trip/RFC coverage, arbitrary custom patterns, complete span/language behavior and release qualification remain open. Product runtime dependencies remain JDK-only.
