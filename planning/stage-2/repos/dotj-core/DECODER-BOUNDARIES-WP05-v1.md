# Selected Decoder boundaries and recovery evidence

Batch 2190 adds a pinned regression gate for decoder array validation, small destinations, pending prefixes and direct fallback controls. The current selected Decoder implementation already matches these cases; this batch records evidence and does not claim a new Java behavior.

The fixture covers 4,620 request forms under five fallback configurations, producing 23,100 boundary scenarios. Requests include real null inputs/destinations, negative/oversized ranges, validation priority, pending byte prefixes, flush flags, seven capacities and two offsets, partial writes and a subsequent continuation-byte recovery call. Additional forms exercise the count/write overloads without a flush argument. Sixty controls cover stable FallbackBuffer identity, external filling, null/change attempts, count behavior, Reset, replacement and remaining state.

The packaged consumer passes 83,230 groups, including native exception byte payloads and indices, supplied destination state and recovery. Native Decoder count/write operations on externally filled buffers differ from Encoder: the recorded valid-input operations leave that buffered output pending. The consumer preserves those native observations without inventing an encoder-like rejection or drain.

This selected boundary evidence does not qualify arbitrary custom stateful fallback providers, shared-buffer reentrancy, Convert, spans, pointers, complete logical type metadata/source ABI or WP-05-T2 acceptance. No accepted task or qualified framework is credited. Next is public Encoder/Decoder logical type metadata and a compiled declaration gap audit against the pinned twenty-eight native declarations. The Java product remains JDK-only.
