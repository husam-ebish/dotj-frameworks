# Generic base Convert array boundary qualification

Batch 2207 qualifies the generic Encoder/Decoder base array Convert implementation against 104 native null/range forms and 3,328 cases. The implementation already satisfies the controls, so the batch adds the native capture, packaged consumer and gate integration without changing Java behavior.

The matrix varies both directions, count multipliers, flush, aliased outputs and prefilled fallback buffers. Invalid source/destination and conflicting negative/oversized ranges pin validation priority and prove callbacks are suppressed before validation succeeds. Output sentinels distinguish validation failure from later count-halving overflow. Full destinations, exact callback traces and fallback Remaining are compared.

Native base Convert computes completion from the consumed-input out location after the virtual write returns. When the two integer outputs alias, a write result can therefore change the completion result: a smaller consumed prefix may still yield completed=true if the aliased write count equals the original input count. The selected Java array-carrier adaptation preserves this observed assignment/evaluation order instead of substituting separate local counters. This does not claim arbitrary CLR byref or source ABI parity.

The packaged consumer passes 20,004 groups: six checks per native case and 36 separate Java output-carrier checks. The Java controls cover null/empty carriers, callback suppression and a subsequent valid conversion for both base classes. Existing 57,600 generic protocol groups and UTF-8 encoder/decoder suites remain regressions. The shared spy component is versioned and its hash is recorded.

Pointer/span Convert, arbitrary callback reentrancy, full reflection/source ABI, E01 applicability and WP-05 acceptance remain open. No accepted implementation task, qualified framework or rights clearance is credited. Next is selected Encoder/Decoder Convert span projection, with explicit native generic-versus-NLS dispatch and pointer-backed adapter boundaries.
