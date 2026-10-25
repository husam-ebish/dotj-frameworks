# Selected UTF-8 Decoder Convert arrays

Batch 2203 implements the selected predefined-fallback UTF-8 Decoder.Convert array overload. It reports consumed bytes, written UTF-16 units and completion through the selected output-array carriers. The decoder retains incomplete UTF-8 prefixes when not flushing and preserves an old prefix if its initial drain throws or cannot fit. This differs from the Encoder's consumed pending-surrogate failure behavior.

Fallback conversion preserves native partial destination writes even when that fallback makes no committed progress. A failed fallback does not count its bytes or partially written characters as consumed/written progress; a later caller may overwrite those uncommitted destination entries. Decoder fallback output is drained fully or reset instead of being retained between Convert calls. The selected implementation uses a bounded destination snapshot and copies it back through exceptional completion.

The packaged probe passes 54,686 groups over 2,880 pinned native sequences and 10,080 conversion calls. It checks both outputs, completion, complete guarded destinations, exception identity/HResult/parameter, recovery and Reset across six UTF-8/fallback profiles. Twelve Java output-carrier controls and two explicit custom-provider boundary controls are separate from native byref claims. The declaration inventory becomes 20/28 selected projections with eight pointer/span gaps.

Generic Decoder-base and custom-provider Convert remain explicit unsupported boundaries. Output aliases, complete null/range priority, strict fallback payloads, cross-API transitions, pointer/span forms, full reflection/source ABI and task acceptance require further qualification. The combined source-adjacency record already pins DecoderNLS, DecoderFallback, UTF8Encoding and Encoding.Internal; E01 applicability remains open. No accepted task, qualified framework or rights clearance is credited.

Next is Decoder Convert boundary qualification, including output aliases, strict unknown-byte/index payloads and transitions through counting, writing, fallback setters and Reset.
