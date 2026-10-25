# Selected stateless UTF-8 replacement conversion

Batch 2162 implements Encoding/UTF8Encoding selected String-to-byte and byte-to-character conversion, counts, preamble, code page, encoding name and read-only metadata. Parameterless and identifier-emission constructors use replacement behavior; Encoding.UTF8 supplies its native identifier-emitting default. Identifier emission affects GetPreamble and does not prepend bytes to GetBytes. Fresh preamble arrays preserve instance state.

The JDK-only internal codec encodes surrogate pairs and replaces unpaired surrogates with U+FFFD. Decoding replaces each malformed maximal valid prefix, including overlong, surrogate, out-of-range and truncated UTF-8 sequences. Native CoreLib supplies 847 text vectors and 2,464 byte vectors; four constructor/default profiles produce 23,112 consumer groups including backing-array preservation and independent preambles.

Native Byte[] uses the existing unsigned System.Byte[] value adapter. This preserves selected octet values, not CLR array/value ABI. Strict conversion, configurable fallback objects, stateful Encoder/Decoder, buffer/range/span/pointer overloads, logical Type lookup, ICloneable and source identity remain open. Public Encoding/UTF8Encoding are partial candidates; WP-05-T2, E01/E02/E03/N01 and framework qualification remain open. No acceptance credit is assigned.

The reviewed source/class/notice map explicitly includes all eighty product sources and the new Encoding, UTF8Encoding and internal codec classes. The standard SPDX headers and JDK-only distribution audits remain required. E01 notice applicability and release review remain open.
