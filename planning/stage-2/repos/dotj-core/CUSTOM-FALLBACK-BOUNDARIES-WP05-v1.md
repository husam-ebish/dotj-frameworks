# Selected custom fallback factory boundaries

Batch 2178 preserves native failure types when a custom UTF-8 fallback factory returns null, throws InvalidOperationException, returns an exception buffer, or constructs a replacement buffer with malformed UTF-16. Null buffers now produce the logical System.NullReferenceException with its pinned HResult. Factory exceptions propagate without replacing them with Java failures.

Custom fallback draining terminates at the first NUL sentinel. Embedded NUL output can leave unread buffer state: encoder count operations stop there, while a writing pass rejects pending output with ArgumentException(bytes). An initial NUL can produce empty output. These behaviors differ from directly installed predefined replacement fallbacks; the native custom-provider path is tested independently.

Twenty native emitted provider profiles combine five replacement strings and four factory modes. They record 2,320 operations, 200 capacity results, factory counts, setter reference identity and destination contents. The packaged consumer passes 5,520 groups. This evidence includes ordinary valid input which must not create buffers, invalid input, embedded NUL and unpaired surrogate replacements. The preceding UTF-8 suites remain required regressions.

This is bounded candidate evidence. Arbitrary custom buffer methods, misleading Remaining values, exceptions during buffer consumption, changing buffers between count/write passes, stateful Encoder/Decoder APIs, complete metadata/source ABI and WP-05-T2 acceptance remain open. No accepted task or framework is credited. Next is direct custom buffer protocol validation against the pinned runtime.
