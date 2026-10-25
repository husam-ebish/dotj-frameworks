# Selected writable UTF-8 fallback customization

Batch 2174 adds selected EncoderFallback/DecoderFallback setters to writable Encoding clones. Read-only rejection precedes null validation. Successful setters retain the supplied fallback object; failed setters preserve the old reference. Original encodings and Encoding.UTF8 remain read-only.

UTF-8 conversion now follows the selected replacement/exception objects. Empty replacements omit invalid input, multi-character replacements preserve UTF-16 scalar boundaries, strict exceptions preserve indexes/payloads, and GetMaxByteCount/GetMaxCharCount incorporate replacement MaxCharCount with overflow-safe validation. Destination overloads retain partial replacement writes: separate ASCII replacement characters may be written before capacity failure, while surrogate pairs are atomic.

Pinned CoreLib supplies 72 setter cases and 25 encoder/decoder combinations covering 300 text, 500 byte, 550 capacity and 2,400 destination cases. Separate conversion/count/string results and destination contents produce 7,594 packaged groups. Existing default and strict conversion suites remain required regressions.

Support is limited to the predefined replacement and exception fallback classes. Custom fallback subclasses fail explicitly with UnsupportedOperationException and remain unqualified. Stateful Encoder/Decoder operation, full type/member metadata, hash algorithms, private runtime identities, source/CLR ABI and WP-05-T2 acceptance remain open. This batch assigns no task acceptance or framework qualification. Next is the selected logical type and API-surface inventory for fallback objects and buffer bases.
