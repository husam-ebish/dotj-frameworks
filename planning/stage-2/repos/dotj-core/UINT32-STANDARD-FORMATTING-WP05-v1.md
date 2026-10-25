# Selected UInt32 standard formatting

Batch 2136 advances DJ-001-WP-05-T1 without implementation acceptance credit.

UInt32 adds IFormattable and the standard format overloads. Decimal, hexadecimal and binary routes use the complete unsigned 32-bit value held in a Java long, with selected precision padding. Other selected numeric formats use the Decimal implementation; round-trip formats select general formatting. The existing default/provider routes remain valid for these nonnegative values. Type reports the selected IConvertible/IFormattable projection.

The pinned CoreLib 10.0.12 corpus records 3,700 format rows and 532 default/provider records across 266 selected values, including low-byte coverage, Int32 signed-boundary neighbors and UInt32 maximum. Twenty anchors add standard general, decimal, fixed, grouped, scientific, round-trip and invalid-specifier cases under invariant/custom numeric symbols. Packaged consumers check 13,229 groups, including interfaces and compiled signatures.

Other numeric interfaces, formats, precision/culture domains, CLR value/boxing identity and release qualification remain open. Product dependencies remain JDK APIs only. Reference/development tools and temporary artifacts stay on D:.
