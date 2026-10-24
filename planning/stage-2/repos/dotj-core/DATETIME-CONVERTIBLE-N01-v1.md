# Selected DateTime IConvertible candidate

Batch 2058 advances `DJ-001-WP-05-T1`; full implementation acceptance remains open.

The candidate preserves its DateTime value through ToDateTime and ToType(DateTime/Object), including the stored daylight-saving overlap state. ToDateTime and ToType(DateTime) retain the existing fresh Java carrier behavior and copy the private overlap flag; ToType(Object) returns the existing immutable carrier. Full CLR value-copy and boxing identity are separate qualification work. Null ToType targets now report ArgumentNullException with the native targetType parameter name.

The pinned CoreLib 10.0.12 oracle records 1,332 calls across 36 values: tick boundaries with all Kind values and modern W. Europe/Europe Zurich gap/overlap samples in 2024 and 2026. It checks thirteen invalid primitive conversions, TypeCode, invariant text, and 21 target types including null. Two overlap pairs retain identical local ticks but distinct UTC values after conversion. The packaged consumer verifies type/HResult/parameter errors, selected ticks/Kind/text and modern overlap binary/UTC results.

Direct historical Local values compare ticks/Kind and conversions without asserting historical offset parity. Arbitrary providers/cultures, other timezone histories, complete boxing/value-copy and language semantics, and E01/E02/E03/N01 release qualification remain open. No acceptance credit or new product runtime dependency is introduced.
