# Selected OLE Automation DateTime conversion evidence

Batch 2057 advances `DJ-001-WP-05-T1` through reference validation of the existing candidate. No product implementation change or acceptance credit is claimed.

The pinned CoreLib 10.0.12 oracle captures 125 imports and 141 exports. Inputs include adjacent binary64 values around range limits and signed fractional days, NaN and infinities, subnormal values, millisecond rounding thresholds, and selected DateTime tick boundaries across all three Kind values. Returned doubles are compared by raw bit pattern; tick counts are retained as decimal strings without JSON floating conversion.

Each conversion and its round trip has a separate result. An import just inside the negative input limit can succeed while exporting its result throws OverflowException because the resulting date precedes the export range. Year-one subday values, negative fractional-day normalization and millisecond precision likewise need not preserve the original input under round trip.

The packaged consumer passes 266 groups, checking ticks, Kind, exact output bits and selected exception type/HResult/parameter names. The existing implementation matches the bounded corpus. COM transport, marshaling, arbitrary providers, all binary64 inputs, language representation and E01/E02/E03/N01 release qualification remain open. The Java product has no new runtime dependency.
