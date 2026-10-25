# BindingFlags HasFlag: bounded Enum bridge

Batch 2100 adds HasFlag(Object) to the selected BindingFlags Java carrier. A null flag throws ArgumentNullException with parameter flag. A foreign enum carrier throws ArgumentException without a parameter name before testing bits, including zero-valued foreign flags. Same-carrier values use (value & flag) == flag with Int32 bit patterns. Existing lowercase or/has helpers retain their Java adapter boundaries.

The pinned .NET 10.0.12 reference covers 8,323 combinations: 29 receiver values, 274 same-type flag values, null and 12 foreign enum families. The packaged consumer checks results, error types, HResults, parameter names and the compiled bridge signature.

The CLR formal parameter is System.Enum; this Java implementation uses Object because the existing selected carriers do not share a physical CLR Enum representation. This mismatch is explicit and prevents claiming exact public API qualification. Reflection search, CLR loading, language integration, full Enum parity and task acceptance remain open. Runtime dependencies are JDK-only. All validation artifacts and caches stay on D:.
