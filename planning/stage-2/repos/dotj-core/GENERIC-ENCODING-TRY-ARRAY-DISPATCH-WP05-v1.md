# Generic Encoding Try spans through array callbacks

Batch 2218 qualifies the complete generic Encoding.TryGetBytes/TryGetChars heap span path through array callbacks, complementing the earlier direct span-override corpus. Native and candidate now compose virtual counting, the capacity decision and the corrected pointer-backed writer adapter. Insufficient capacity skips the writer and assigns zero; callback failures preserve the written slot and isolate the temporary destination. Negative writer returns are rejected by the generic Encoding pointer-result path.

The pinned runtime corpus records 1,152 cases varying direction, multiplier, count/write callback modes, four source lengths, four destination capacities and two view offsets. The packaged consumer passes 4,608 groups for success/exception, written slot, full guarded destination and exact ordered array trace. Synthetic callback overruns use an explicit logical native exception adapter. No additional product change is needed after the preceding generic span correction.

The fixture binds runtime 10.0.12, CoreLib and producer hashes. The differential binds fixture, consumer and candidate JAR hashes. Native and differential bytes are LF-pinned. All product sources, build scripts and ownership mapping reproduce from the preceding prepared tree; the unchanged 95-source JAR retains the earlier encoding/API audit results. The canonical queue still reruns the full foundation gate before merge.

This is bounded generic Try integration through selected array callbacks. Arbitrary pointer overrides, CLR lifetime/pinning, reentrancy, full metadata/source ABI, E01 applicability and WP-05 task acceptance remain open. No accepted implementation task, qualified framework or rights clearance is credited.

Next is generic Encoding.GetChars/GetString array allocation behavior and range overloads, including callback dispatch, allocation failures and range validation, while preserving the qualified UTF8 paths.
