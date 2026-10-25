# Selected invariant custom DateTime buffers

Batch 2077 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

Custom String, Char-array and UTF-8-array formatting now share a private token engine. Array formatting preserves native partial writes until the first append that exceeds destination capacity, continues evaluating the format, and reports final fit separately. Invalid formats can throw after partial writes while preserving the seeded written count. A failed capacity result sets written to zero. Empty trimmed fractions can remove a previously emitted period; its storage may remain beyond the final written range. Offset sign and remaining digits have distinct append boundaries. Quoted literals write character by character.

Typed destination views copy their selected temporary storage back in a finally block, preserving the same mutation on exception and keeping surrounding backing storage intact. No public product signatures or dependencies were added.

The pinned CoreLib 10.0.12 reference records 4128 Char/UTF-8 cases across selected custom tokens, widths, quoted/escaped literals, non-ASCII literal characters, fractions, offsets and malformed formats. All 12384 packaged groups pass through raw arrays and zero/three-offset spans. Checks compare boolean or exception/HResult, written count, complete buffer contents and outside-view sentinels. The earlier custom string corpus and existing standard/temporal buffer gates remain required.

This bounded profile excludes volatile year-one time-only zone formatting, historical/other-zone offsets, arbitrary providers and calendars, complete Unicode/surrogate cases, allocation behavior, CLR span/byref language integration and full foundation/release acceptance. Product runtime dependencies remain JDK-only.
