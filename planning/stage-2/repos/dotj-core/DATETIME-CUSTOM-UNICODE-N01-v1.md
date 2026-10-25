# Selected DateTime custom Unicode formatting

Batch 2078 advances DJ-001-WP-05-T1; no acceptance task or release gate is accepted.

The selected custom formatter preserves UTF-16 code units in strings and Char buffers. The pinned native UTF-8 custom path throws ArgumentOutOfRangeException with parameter ch and null ActualValue for ordinary surrogate characters, including a valid pair handled as two characters. An escaped character instead follows the native one-byte cast; this can produce a byte sequence that is not valid UTF-8. The candidate now keeps a separate byte trace so final copying preserves those bytes rather than re-encoding them as text. Prefix writes, growth/failure behavior, written state and exceptions remain aligned through raw arrays and offset spans.

Golden JSON stores format and Char output as integer UTF-16 code-unit arrays to preserve supplementary and isolated-surrogate cases without serializer substitution. The pinned CoreLib 10.0.12 corpus includes 60 string cases and 3960 Char/UTF-8 buffer cases across quoted, ordinary, escaped, percent and malformed forms, including BMP characters with non-ASCII low bytes and zero-byte casts. The packaged consumer passes 12060 groups through three string routes and array/zero-offset/three-offset buffer routes. It checks exception type/HResult/parameter/ActualValue, written counts, all storage and surrounding sentinels.

These are bounded native custom-format observations, not a claim about every .NET UTF-8 API. Arbitrary culture/calendar/provider behavior, complete Unicode coverage, historical/other-zone offsets, volatile time-only offsets, language identity/byref lifetimes, performance and foundation release qualification remain open. Product runtime dependencies remain JDK-only.
