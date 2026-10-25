# Selected NumberStyles enum formatting

Batch 2091 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

NumberStyles implements selected IFormattable and default/provider/format/provider-format ToString contracts. G/F prefer exact named values or native-style descending flag decomposition, including Number, Float, Currency, Any, HexNumber and BinaryNumber composites; unknown residual bits return signed decimal. D returns decimal and X returns eight uppercase hexadecimal digits. Null/empty formats select G; case variants are supported and invalid formats throw FormatException. Providers are ignored. The declared-name/numeric get_Name adapter remains unchanged.

FromInt32 is an explicit Java value-input adapter, preserving arbitrary Int32 enum values and reusing named carriers. It is not a declared native NumberStyles member or a complete CLR cast/Enum.ToObject implementation. The existing Or behavior is unchanged. Java Integer operations are qualified because the native Integer flag name shadows java.lang.Integer in this class.

The pinned CoreLib 10.0.12 reference records 281 values and 4215 formatted cases, including all 0-255 values, every native named value, higher composite masks, unknown bits and signed endpoints. All 13208 packaged groups pass across five default/formatted routes and selected interface identity/lookup/assignability/instance/fresh-array tests. Native and Java providers throw if queried. javap verifies the formatting signatures and IFormattable declaration.

Native IComparable, IConvertible and ISpanFormattable remain explicitly omitted. Physical CLR enum/boxing identity, other Enum APIs, language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only; validation files and caches stay on D:.

The foundation API audit now requires the IFormattable declaration, FromInt32 adapter and four formatting signatures while retaining all nineteen named-field checks and the native zero declared-method count. Source line endings are pinned to LF so working and isolated source hashes agree.
