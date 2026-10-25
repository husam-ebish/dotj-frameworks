# Native stateful Convert contract and selected output carrier plan

Batch 2199 records the six declared public Encoder/Decoder Convert overloads and a pinned .NET 10.0.12 UTF-8 array-conversion baseline. It does not implement Java stateful Convert or count declaration presence as behavioral parity.

The native fixture covers 5,760 sequences, 20,160 direct conversion calls and 5,760 resets across both directions, six UTF-8/fallback configurations, pending input, flush modes, two destination offsets and capacities 0, 1, 2, 3, 4 and 8. There are 472 partial successful conversions and 3,584 failures, including writes before failure. Subsequent recovery calls and a reset followed by empty conversion expose retained-state behavior. Destination guards and sentinel-initialized output values are recorded on success and failure.

Reflection.Emit bridges call the native Convert methods directly with managed addresses into output arrays. This avoids relying on MethodInfo.Invoke to copy ref/out arguments back after an exception. The captured native calls leave the initialized output sentinels unchanged on the recorded failures; the destination may already have changed. That observation must not be replaced by a generic assumption that out values are zeroed on failure.

The selected Java adapter plan uses separate one-element int[] arrays for the two integer outputs and a one-element boolean[] for completed, consistent with the existing candidate TryParse output-array convention. Native names/order are charsUsed, bytesUsed, completed for Encoder and bytesUsed, charsUsed, completed for Decoder. This is an explicit carrier convention, not a claim about CLR managed references, source ABI or pointer lifetime. Null/short Java output arrays require explicit adapter controls when implemented.

The verifier passes 192,284 integrity controls, checks the six native overload declarations, records candidate declaration availability separately, and always sets candidateBehaviorQualifiedByThisBaseline=false. The combined stateful fallback source-adjacency manifest already pins Encoder, EncoderNLS, Decoder, DecoderNLS and Encoding.Internal. E01 applicability remains open. No accepted task, framework qualification or rights clearance is credited.

Next is selected Encoder Convert implementation against this baseline, including partial input/output progress, pending state, output adapters and explicit boundaries for unimplemented forms. Decoder Convert, spans, pointers and complete qualification remain separate open work.
