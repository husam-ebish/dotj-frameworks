# Selected NumberStyles HasFlag

Batch 2095 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

NumberStyles HasFlag maps same-carrier Int32 bit containment independently of numeric parsing style validity. Zero, unknown, composite and sign-bit flags retain numeric meaning. Null throws ArgumentNullException with flag; foreign enum types throw ArgumentException with no parameter name before bit testing, including foreign zero values.

The pinned CoreLib 10.0.12 reference records 7025 cases over 25 anchor/all-named values, 268 masks including every 0-255 mask and every named mask, null and twelve foreign enum types. All packaged groups pass, comparing booleans and exception identity/HResult/parameters. javap and the foundation audit require HasFlag(Object); the API preview passes while retaining all nineteen named-field checks.

System.Enum is the native formal parameter. Object is the explicit Java bridge for this bounded enum-carrier domain, not exact physical CLR parameter/inheritance qualification. Non-enum Java Objects are outside the captured native domain. Other Enum APIs, complete messages, equivalent/isolated type contexts, physical boxing, language integration and full release qualification remain open. Product runtime dependencies remain JDK-only; all validation intermediates and caches stay on D:.
