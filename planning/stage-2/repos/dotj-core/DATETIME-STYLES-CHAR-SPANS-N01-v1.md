# Selected DateTimeStyles Char span formatting

Batch 2084 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

DateTimeStyles implements the selected ISpanFormattable Char-array adapter and a typed Char-view overload. Formatting validates the format first; a short destination returns false with written zero and no writes; success copies the complete selected G/F/D/X text. Invalid formats preserve the seeded written count and storage. The typed view uses public ReadOnlySpan copy operations and a Char format view. The provider remains ignored.

Span/ReadOnlySpan ToString now returns selected Char contents or the native Byte view descriptor, with a Java toString adapter. This supplies public format text access across Java package boundaries without exposing private storage helpers.

The pinned CoreLib 10.0.12 oracle records 1264 real ISpanFormattable buffer cases and 84 mutable/read-only Char/Byte text cases. The packaged consumer passes 5225 groups across raw arrays, interface dispatch, zero/three-offset destination views, offset format views and both text routes; complete storage, written state, exceptions and outside-view sentinels are checked. Two Byte-view misuse programs fail compilation. Type enumerates the four native interfaces and checks lookup, assignability, instance membership and defensive copies.

This batch also corrects an overbroad earlier IsInstanceOfType condition that included DateTimeStyles in IUtf8SpanFormattable. Explicit pinned native negative checks now require both UTF-8 assignability and instance membership to be false; the Char-only overloads and compile rejections guard the supported domain. Earlier enum fixtures now compare the complete four-interface profile.

Inherited Enum methods are projected onto the Java immutable carrier. Other Enum APIs, complete messages, physical CLR/ref-struct/boxing identity, arbitrary memory, full language integration and release qualification remain open. Product runtime dependencies remain JDK-only.
