# Selected BindingFlags inherited enum formatting

Batch 2096 advances DJ-001-N01-T2; no implementation task or release gate is accepted.

BindingFlags now maps inherited default/provider/format/provider-format ToString and selected IFormattable behavior. G/F prefer exact names or descending named-mask decomposition; unknown residual bits use signed decimal. D returns decimal and X eight uppercase hexadecimal digits. Null/empty formats select G, case variants are accepted and invalid formats throw FormatException. Providers are ignored. FromInt32 is a documented Java value-input adapter, not a native BindingFlags declaration or complete Enum.ToObject/cast implementation.

The pinned CoreLib 10.0.12 oracle records 289 values and 4335 formatted cases, including every named flag, all 0-255 values, higher masks, unknown bits and signed endpoints. All 13584 packaged groups pass through default/formatted routes and selected interface identity, lookup, assignability, instance and defensive-array checks. Native/Java providers throw if queried. javap verifies the four formatting signatures and IFormattable declaration.

The existing get_Name behavior (including null for unnamed combinations), lowercase or/has Java helpers and their host boundaries remain unchanged. This work maps inherited CLR Enum contracts onto the existing Java immutable carrier; it does not implement reflection search behavior or CLR loading/IL execution. Native IComparable, IConvertible and ISpanFormattable remain explicitly omitted in this profile. Physical enum/boxing identity, language integration, complete acceptance and release qualification remain open. Product runtime dependencies remain JDK-only; all validation intermediates and caches stay on D:.
