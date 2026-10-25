# Selected TimeSpanStyles HasFlag

Batch 2090 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

TimeSpanStyles HasFlag maps Int32 bit containment for the same carrier. Zero flags succeed; unknown, composite and sign bits retain numeric meaning independently of the stricter TimeSpan exact-parsing style validator. Null throws ArgumentNullException with flag. Foreign enum types throw ArgumentException with no parameter name before bit testing, including zero-valued foreign flags.

The pinned CoreLib 10.0.12 oracle records 3850 cases across signed anchors, every 0-255 flag value, further unknown/sign-bit flags, null and twelve foreign enum types. All packaged groups pass, comparing booleans and native exception identity/HResult/parameters. javap verifies the deliberate HasFlag(Object) Java signature.

The native parameter is System.Enum; Object is the explicit Java carrier bridge for this bounded enum argument domain. This does not qualify exact CLR parameter/inheritance identity. Non-enum Java Objects are outside the captured native domain. Other Enum APIs, complete messages, equivalent/isolated type contexts, physical boxing, language integration and full release qualification remain open. Product runtime dependencies remain JDK-only. Validation intermediates and caches stay on D:.
