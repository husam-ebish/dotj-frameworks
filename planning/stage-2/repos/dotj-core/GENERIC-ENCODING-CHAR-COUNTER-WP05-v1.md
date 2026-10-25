# Generic Encoding char counter and abstract contract

Batch 2224 makes GetCharCount(Byte[]) the native whole-array facade and makes GetCharCount(Byte[], int, int) the required abstract counter. Whole-array null input is rejected before delegating the original array, index zero and full length. The range callback owns range validation and can return negative counts. UTF8Encoding explicitly preserves its preceding selected range behavior. The earlier span-override consumer adds a rejecting range counter stub, matching its native abstract implementation.

The native corpus records 1,344 cases across whole/range counting, heap spans, default decoder counts with both flush values, character allocation and string routes. A minimal Java subclass implements only the six native abstract methods. The packaged consumer passes 2,695 groups, including exact declared abstract signatures and all outcomes/traces. A separate compile control rejects a subclass supplying only the whole-array counter. The producer uses explicit typed argument arrays and the verifier rejects binding-only exception classes.

The six abstract signatures are the two range counters, two array destination writers and two maximum-count methods, projected with UTF-16 char arrays and unsigned-byte object arrays. This closes that selected abstract contract, not the complete Encoding API or source ABI. The 96-source owned map, distribution/rights-input audits, selected compiled API audit and all retained generic/default/UTF8/custom/stateful regressions pass under serialized scratch access. No public signature or class inventory is added; two methods change their abstract/default roles.

CoreLib, producer, fixture, versioned consumers and JAR hashes are bound and LF-pinned. Direct pointer overrides, arbitrary reentrancy, full metadata/source ABI, E01 applicability and WP-05 task acceptance remain open. No accepted implementation task, qualified framework or rights clearance is credited.

Next is generic Encoding equality and hashing over stored code pages, reported CodePage overrides, provider values/references, read-only clones and comparisons with UTF8 encodings.
