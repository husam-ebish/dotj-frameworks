# Selected TimeSpanStyles enum formatting

Batch 2086 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

TimeSpanStyles implements selected IFormattable/default/provider/format/provider-format ToString contracts. G/F return None or AssumeNegative for the named values and decimal text for all other Int32 values; D uses signed decimal and X uses eight uppercase hexadecimal digits. Null/empty formats select G, case variants are supported and invalid formats throw FormatException. Provider lookup is ignored. The existing get_Name adapter and exact-parsing style validation remain unchanged.

The pinned CoreLib 10.0.12 oracle confirms Int32 storage and Flags metadata and captures 263 defaults plus 3945 formatted cases. All 12362 packaged groups pass through three formatted routes, two default routes and selected interface metadata/lookup/assignability/instance/defensive-copy checks. Emitted native and Java providers throw if queried. javap checks the four formatting signatures and IFormattable declaration.

Native inherited Enum formatting is projected onto the Java immutable carrier. IComparable, IConvertible and ISpanFormattable are explicitly recorded as omitted in this selected profile. Physical enum/boxing identity, other Enum methods, language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only. Validation files and caches stay on D:.
