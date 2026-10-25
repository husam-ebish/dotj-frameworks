# Selected NumberStyles Char span formatting

Batch 2094 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

NumberStyles implements the selected ISpanFormattable Char-array contract and typed Char destination/format views. Format validation precedes writes; successful operations copy the complete enum text; short destinations return false, written zero and unchanged storage. Invalid formats preserve the seeded written count. Provider lookup is ignored. Public ReadOnlySpan text/copy operations supply cross-package view access.

The pinned CoreLib 10.0.12 reference includes 1982 buffers over 26 anchors/all named values and 84 Span/ReadOnlySpan Char/Byte text cases. All 8097 packaged groups pass through raw arrays, interface calls, zero/three-offset destination views, offset format views and text adapters. Two Byte-view misuse programs fail compilation. Full storage, outside-view sentinels, written state, exceptions and four-interface metadata are checked. Explicit negative native checks reject UTF-8 interface assignability and instance membership. Earlier enum fixtures and the foundation audit now require the complete four-interface profile and both Char formatting signatures; the API preview passes.

These are inherited Enum contracts projected onto a Java immutable carrier. Physical CLR/ref-struct/boxing identity, other Enum APIs, complete messages, arbitrary memory, language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only. Validation files and caches stay on D:.
