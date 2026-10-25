# Selected UTF-8 logical type identity

Batch 2168 maps Encoding, UTF8Encoding, EncoderFallbackException and DecoderFallbackException into logical Type lookup, including case-insensitive names and inherited array/assembly name parsing. It preserves Encoding abstractness, both fallback exceptions' sealed flags, namespace/full/assembly names and native base types. Native Encoding/UTF8Encoding are not marked serializable in the pinned runtime; the existing exception/array serializability rules remain applicable.

Pinned CoreLib supplies eight base/vector-array shapes, 96 lookup cases, 36 assignability/subclass pairs and 42 instance tests. The packaged consumer passes 222 groups including canonical case-insensitive identity. Both the separate Type build and complete packaged product build, including external identity and 1,600 concurrent canonical construction tests, pass.

The fixture retains complete native interface names as unqualified metadata. Encoding's ICloneable contract and the larger native array interface set are not implemented by these selected lookups. Full member reflection, native serialization, source/CLR ABI and WP-05-T2 acceptance remain open. No accepted implementation task or framework is credited. The next concrete work is Encoding Clone/read-only behavior and its ICloneable contract.

The compile-only typeof lowering probe now reads the reviewed Type build source profile instead of maintaining a duplicate transitive source list. Its independent consumer passes with the complete selected dependency set.
