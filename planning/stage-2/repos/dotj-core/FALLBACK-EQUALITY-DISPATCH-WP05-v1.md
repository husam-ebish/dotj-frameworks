# Selected custom fallback equality and hash dispatch

Batch 2183 corrects UTF8Encoding.GetHashCode to use its fixed UTF-8 code page, independently of an overridden CodePage getter. The pinned runtime does not invoke that getter when hashing UTF8Encoding. Controls include a getter returning 90000 and one which throws; neither changes or prevents the native hash.

The capture also records custom encoder/decoder fallback overrides which compare by key, always return false, always return true, throw during comparison, or throw during hashing. Comparison preserves preamble/encoder/decoder short circuiting and can be asymmetric or nonreflexive when the supplied override is. Exceptions and exact custom method invocation order/counts are checked. Hash formulas are checked within each process; raw randomized values are not compared between processes.

Sixty-six native profiles produce 4,554 comparisons against configured encodings, null, a String and a foreign Object. Hash operations record exact encoder/decoder calls and failures. The packaged consumer passes 9,240 groups, including native custom method call counts. Earlier predefined equality/hash and fallback suites remain regressions.

This selected dispatch evidence does not qualify arbitrary reentrancy, custom Encoding subclasses, lowercase host Object interoperability, stateful encoders, full metadata/source ABI or WP-05-T2 acceptance. No accepted task or qualified framework is credited. Next is selected custom fallback slice/count/allocation dispatch and validation order.
