# Selected Byte standard formatting

Batch 2131 advances DJ-001-WP-05-T1 and the N01 public-name mapping without task acceptance credit.

Byte adds IFormattable and ToString(String)/ToString(String,IFormatProvider), while its existing provider and Java text routes preserve selected native output. Numeric formatting delegates to Int32, with explicit eight-bit masking for hexadecimal/binary output, lowercase bare decimal normalization, round-trip aliases, and FormatException for invalid standard letters. The carrier preserves unsigned byte values 0 through 255, including hexadecimal/binary precision padding. NumberFormatInfo negative/positive signs and separators are honored, including through IConvertible.ToString(provider).

The pinned CoreLib 10.0.12 reference records 3,184 format rows and 512 default/provider rows. All 256 unsigned-byte values cover selected bit formats; twelve anchors add general, decimal, fixed, grouped, scientific, round-trip and invalid-specifier cases across invariant/custom numeric symbols. The Java consumer checks 11,601 groups through concrete, IFormattable, IConvertible and Java text routes. Type reports the selected IConvertible/IFormattable projection with fresh arrays, lookup, assignability and instance behavior. Other native numeric interfaces remain explicitly omitted.

This is a bounded formatting profile, not complete numeric API, format/culture support, CLR value/boxing identity or release qualification. Product dependencies remain JDK APIs only. Python, PowerShell and .NET are reference/development tools. Temporary artifacts and caches remain under D:\AI\Implementation\dotj Frameworks.
