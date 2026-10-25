# Selected small-integer String parsing

Batch 2153 adds String Parse/TryParse overloads with default or explicit format providers to SByte, Byte, UInt16 and UInt32. A package-private Int32 helper validates the selected Integer grammar and accumulates a JDK BigInteger before each carrier checks its native range. This preserves UInt32 values above Int32.MaxValue without decimal rounding. The grammar recognizes ASCII integer whitespace, selected leading signs and native trailing-NUL termination; it rejects decimal/group/exponent syntax and Unicode digit substitutions in this profile.

Pinned CoreLib 10.0.12 records 398 inputs per provider/type across invariant and custom sign profiles. Consumers verify 9,672 groups, including nulls, malformed inputs, range edges, 100-digit values and output reset on ordinary TryParse failure. A further 120 native provider controls are included in that total: requested type and call count, null-return fallback, and propagation of provider-thrown FormatException/OverflowException while preserving the previous output slot. Null String input is handled before querying the provider, matching the reference.

The selected signature audit grows from 104 to 120 direct native declarations. The thirty-type compiled API audit and Int32 declaration audit retain their existing results: 43 directly projected Int32 declarations and ten parsing overloads collapsed through five span carriers. New parsing helpers are not public API.

Arbitrary NumberStyles, span overloads, additional provider/culture profiles, native generic interfaces, CLR value ABI, implementation-task acceptance and release qualification remain open. The product remains JDK-only; all reference tools, caches and temporary artifacts remain on D:.
