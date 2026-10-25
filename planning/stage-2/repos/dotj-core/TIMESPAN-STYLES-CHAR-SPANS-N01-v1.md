# Selected TimeSpanStyles Char span formatting

Batch 2089 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

TimeSpanStyles implements the selected ISpanFormattable Char-array contract and typed Char destination/format-view overload. It validates format before touching written state or storage, writes the complete selected enum text on success, and returns false with written zero and no writes when capacity is short. Invalid formats preserve the seeded written count. Provider lookup is ignored. Typed views use public ReadOnlySpan text/copy operations across the Java package boundary.

The pinned CoreLib 10.0.12 reference records 1052 buffer cases and 84 mutable/read-only Char/Byte text cases. All 4377 packaged groups pass through arrays, interface dispatch, zero/three-offset destination views, offset format views and capitalized/Java text routes. Complete buffers, outside-view sentinels, written counts, exceptions and four-interface metadata are compared. Two Byte-view misuse programs fail compilation. Explicit native negative checks require UTF-8 assignability and instance membership to be false. Earlier enum fixtures now use the complete four-interface profile.

The selected interfaces are inherited CLR Enum contracts projected onto a Java carrier. Other Enum APIs, full messages, physical CLR/ref-struct/boxing identity, arbitrary memory, language integration and release qualification remain open. Product runtime dependencies remain JDK-only. All validation intermediates and caches stay on D:.
