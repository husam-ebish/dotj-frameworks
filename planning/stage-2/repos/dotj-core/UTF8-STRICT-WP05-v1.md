# Selected stateless UTF-8 strict fallback

Batch 2163 adds UTF8Encoding(bool,bool) and strict invalid-input conversion. EncoderFallbackException and DecoderFallbackException expose selected native failure payloads, including invalid UTF-16 character or maximal invalid byte prefix, failure index, null parameter name and ArgumentException HResult. The internal codec distinguishes failure from replacement without changing valid UTF-8 output.

Pinned native fixtures reuse all 847 text and 2,464 byte vectors and independently capture conversion and count failures. Two identifier-emission profiles exercise 18,178 packaged groups, including 1,305 native failure vectors. The prior 23,112 replacement groups also pass.

Exception message equivalence and default constructor payloads have not yet been qualified. Stateful conversion, custom fallback objects, range/buffer/span/pointer overloads, logical type lookup and native serialization/source ABI remain open. This is bounded strict-mode behavior and assigns no task acceptance or release qualification. The next work is constructor/null/range exception boundaries and exact selected type identity.
