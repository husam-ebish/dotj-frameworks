# Selected custom stateful Decoder protocol

Batch 2193 preserves custom fallback creation for incomplete UTF-8 prefixes before retaining them between writing calls. It also reproduces the native two-stage reset when fallback output cannot fit a destination: fallback consumption resets first, then the enclosing overflow path resets again. A throwing reset interrupts that sequence at its actual point. Count calls, pending-prefix recovery, externally filled buffers and null/throwing factories retain their recorded behavior.

Forty-four emitted native provider/buffer profiles combine four output strings and eleven adversarial behaviors. Seven sequences per profile produce 1,496 calls. The packaged consumer passes 5,236 groups, including exact factory and five buffer-method counters, failures, return values and supplied destinations. Reflection invokes native getters to preserve their exceptions; the consumer explicitly maps a null buffer member dereference while retaining the nullable getter result.

The earlier ordinary decoder partitions/boundaries and custom encoder protocol remain regressions. Eight SHA-256-pinned source members preserve shared encoder/decoder algorithm adjacency, including DecoderNLS and Encoding.Internal; the notice-review queue links the affected sources. This is reference and review evidence, not rights clearance. E01 remains open.

Arbitrary shared-buffer reentrancy, other encodings, Convert, spans/pointers, complete metadata/source ABI and WP-05-T2 acceptance remain open. No accepted task or qualified framework is credited. Next is selected stateful Encoder/Decoder span count/write overloads through the existing span carriers, with native bounded views, partial destinations and flush transitions.
