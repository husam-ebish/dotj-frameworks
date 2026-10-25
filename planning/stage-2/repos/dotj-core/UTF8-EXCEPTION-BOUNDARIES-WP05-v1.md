# UTF-8 exception constructors and null boundaries

Batch 2164 corrects fallback exception default/null-message construction and the GetByteCount(String) null argument identity. Eighteen native constructor vectors cover null versus empty messages, custom messages, inner exceptions and DecoderFallbackException byte-array/index arguments. Native byte-array payloads preserve reference identity, accept null, and preserve negative or maximum indexes without validation. Ten strict/replacement null calls preserve native ArgumentNullException parameter names, messages and HResults.

The packaged consumer passes all 28 controls. Prior conversion suites remain required gates. Native conversion error message equivalence, range/buffer/span/pointer overloads, configurable fallback, stateful conversion, logical type lookup and source/CLR ABI remain open. This candidate work assigns no WP-05-T2 acceptance or framework qualification.
