# Selected UInt16 UTF-8-span formatting

Batch 2143 adds IUtf8SpanFormattable projection and selected raw-array/interface/typed-view formatting. Short buffers return false with zero written and preserve storage; offset views preserve surrounding units. Invalid formats are checked before writes.

Pinned CoreLib 10.0.12 records 2,448 formatting buffers across fourteen numeric anchors and seventeen formats. Packaged consumers check 9,793 groups. The invariant and Unicode symbol providers expose byte-length differences, including multibyte signs and decimal separators. Existing character-span, formatting and comparison checks remain in the full gate. One generic Span<T> destination bridges Java erasure of the CLR Char/Byte overloads; typed format input remains a character span.

Other numeric APIs, formats/cultures, native generic interfaces, CLR byref lifetimes, task acceptance and release qualification remain open. The product remains JDK-only; development tools and intermediate artifacts stay on D:.
