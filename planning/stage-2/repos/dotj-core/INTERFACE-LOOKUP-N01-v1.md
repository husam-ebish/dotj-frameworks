# Selected core interface lookup

Batch 2066 advances `DJ-001-WP-01-T1`; no implementation task is accepted.

Twenty selected class/interface profiles now use a common GetInterface lookup rule: unqualified leaf names are allowed, namespace names retain exact case, and ignoreCase applies to the leaf. Null retains ArgumentNullException with fullname; selected missing names return null. The duplicate String, Int32 and DBNull lookup branches are replaced by this rule, including correction of DBNull's previous namespace-insensitive result.

String and Int32 now enumerate their selected logical interface lists. The selected marker/conversion interfaces enumerate no parents, while ISpanFormattable enumerates IFormattable. Existing Byte/SByte/UInt16/UInt32/Decimal lists remain restricted to IConvertible. Existing DateTime/TimeSpan and exception profiles retain their declared selected scope.

The pinned CoreLib 10.0.12 reference records twenty profiles and 448 name lookups; the packaged consumer checks 468 groups. The oracle verifies that every selected interface exists natively, retains every omitted native interface name, guards corpus shape and preserves true null through reflection invocation. Profiles cover full/leaf names, case combinations, namespace case, missing/empty/null names and both case flags.

These are partial logical interface projections. Native generic/math and other omitted interfaces, their lookup/dispatch, direct String carrier conversions, full reflection and language/release qualification remain open. Enumeration of selected interfaces does not qualify full native interface coverage or physical Java interface adaptation. No product runtime dependency changes.
