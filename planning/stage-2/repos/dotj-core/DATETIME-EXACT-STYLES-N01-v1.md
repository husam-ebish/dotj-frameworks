# Selected DateTime exact parsing styles

Batch 2074 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

Four String/Character-view ParseExact and TryParseExact signatures add DateTimeStyles. Existing adapters select None. Selected formats are yyyy-MM-dd, yyyy-MM-dd HH:mm:ss, yyyy-MM-ddTHH:mm:ss.fffffff, s, o and O. Round-trip formats require seven fractional digits and accept uppercase Z or numeric offsets. Kind, modern zone and overlap conversion reuse the bounded ISO style profile.

Pinned native validation checks invalid styles before input/output and uses parameter name style, while ordinary parsing uses styles. Failed TryParseExact resets default state; invalid styles and nonempty input with an invalid single-character format preserve the seeded output while throwing. AllowInnerWhite permits selected token spacing and leading space. AllowTrailingWhite also permits the selected literal date/time space to be absent, as observed in the pinned native reference.

The pinned CoreLib 10.0.12 reference contains 2452 real String/span cases. The packaged consumer checks 7356 String and zero/offset Character-view groups, including all 0-255 style combinations on a round-trip anchor, invalid flags, format/null/error precedence, exact fractions, offsets and modern DST state. Public signatures are audited independently.

Arbitrary custom formats, format arrays, provider/culture grammars, historical and other-zone local conversions, full enum and language/byref identity, and release qualification remain open. Java null style/view and output-array storage are host adaptations outside CLR domains. Product runtime dependencies remain JDK-only.
