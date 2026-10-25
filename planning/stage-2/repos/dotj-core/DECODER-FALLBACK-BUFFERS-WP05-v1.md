# Selected decoder fallback buffers

Batch 2173 adds DecoderFallbackBuffer and replacement/exception factories. Replacement buffers emit one replacement string per fallback call, preserve cursor/Remaining/rewind/reset behavior and reject recursion with bytesUnknown parameter identity. Empty replacement fallback returns false without resetting its existing cursor state. Null source byte arrays are accepted by replacement buffers.

Exception fallback normalizes a null byte array to an empty payload; nonnull arrays retain reference identity. Arbitrary Int32 indexes and selected HResult/parameter/byte payload fields are preserved. Native calls use reflection with explicit argument arrays to retain genuine nulls rather than PowerShell argument conversions.

Eight profiles with 44 transitions produce 1,416 packaged groups checking factory distinction, before/result/after state and unchanged byte inputs. Native private buffer runtime names remain unqualified. Error message parity, integration with configurable UTF-8 conversion, full logical reflection/source ABI and WP-05-T2 acceptance remain open. The explicit source/class map includes the new base and both private buffer classes. No task or framework qualification is credited. Next is writable Encoding fallback setters and selected replacement/exception conversion and capacity behavior.
