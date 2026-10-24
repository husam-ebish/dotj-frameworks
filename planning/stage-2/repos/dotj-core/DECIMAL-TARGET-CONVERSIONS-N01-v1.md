# Selected Decimal target and floating conversions

Batch 2062 advances `DJ-001-WP-05-T1`; no task acceptance is claimed.

Decimal.ToType now uses the selected shared dispatcher for checked primitive, String and Object conversions and managed invalid-target errors. Decimal self conversion retains its existing fresh carrier and preserves coefficient, scale and signed zero.

Instance IConvertible ToDouble and ToSingle now use the existing static native-profile conversion algorithm. A before/after probe confirms that -0.00 previously lost its sign in both instance floating conversions. It also confirms that 1.0000000596046447753906250001 previously converted directly to the Single above 1.0, while the pinned native double-then-Single route produces 1.0. The instance and static routes now agree on the selected native results.

The pinned CoreLib 10.0.12 reference records 1,242 calls across 54 Decimal strings and 23 target types. Cases include Decimal extrema, signed and unsigned integer rounding limits, half-even values, signed zeros, small magnitudes and selected floating halfway neighborhoods. The packaged consumer checks exact Single/Double bits, all four Decimal.GetBits words for Decimal results, logical carriers, text and selected exception class/HResult/parameter names.

The profile uses invariant culture and null providers. Complete floating input coverage, arbitrary providers, full messages, physical boxing identity, language integration and release qualification remain open. No new product runtime dependency is introduced.
