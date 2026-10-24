# Selected round-trip, RFC and UTC DateTime formats

Batch 2071 advances `DJ-001-WP-05-T1`; implementation acceptance remains open.

The candidate supports invariant o/O with seven fractional digits and Kind-specific suffixes, r/R RFC text, u universal-sortable text and U universal-full text. As in the pinned native behavior, r/R and u format the stored fields with their literal GMT/Z markers; U converts to UTC before formatting. Local o/O uses the selected timezone offset and retains the private overlap state, distinguishing both occurrences of a modern autumn 02:30.

The pinned CoreLib 10.0.12 reference records 354 string cases through three native routes and 2,190 Char/UTF-8 buffers. UTC values cover selected full-range endpoints; Unspecified full-range values exclude U. Local/Unspecified UTC conversion and Local suffix checks use modern 2024/2026 W. Europe Standard Time against JDK Europe/Zurich. The packaged consumer passes 2,544 groups and guards that the selected autumn overlap has two distinct offsets.

Native o/O, r/R and u require enough buffer for the complete output; U preserves partial full-date/time chunks using the converted UTC value's weekday/month. Every selected short capacity checks return state, written count and complete buffer contents.

This qualifies selected formatting, not round-trip parsing/styles, historical Local offset parity, all zones/cultures/providers/calendars, arbitrary custom formats, complete span/language behavior or release qualification. No product runtime dependency changes.
