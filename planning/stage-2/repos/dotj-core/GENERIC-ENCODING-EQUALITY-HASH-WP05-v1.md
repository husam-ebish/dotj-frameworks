# Generic Encoding equality and hash

Batch 2225 corrects generic Encoding equality and hashing to use the constructor-stored code page. Overriding the public CodePage getter changes the reported value without changing this identity component. Existing fallback value comparisons and UTF8Encoding-specific equality and hash behavior remain in place.

The pinned native fixture records 120 states and 14,400 ordered comparisons. It varies four generic constructor code pages, a reported-code-page override, five fallback profiles, read-only and cloned instances, and four UTF8 constructor combinations. The packaged consumer checks the native unchecked hash formula, null and unrelated values, read-only and reported-code-page properties, and every ordered comparison: 14,880 groups. Ordered pairs preserve observed generic/UTF8 directionality rather than assuming symmetry. The maximum Int32 code page exercises native unchecked hash arithmetic.

Native replacement hashes use a per-process random seed. The fixture includes each fallback contribution and verifies its unchecked Int32 formula. The Java consumer checks that formula using Java-local fallback hashes; raw random values are not compared across processes. The pre-change candidate reproduces the reported-code-page hash formula mismatch. The corrected 96-source candidate passes this consumer and retained encoding, distribution, rights-input and compiled API audits. Native producer, fixture, consumer and JAR hashes bind the evidence. New evidence and source files use explicit LF attributes.

This qualifies only the selected equality/hash behavior. Arbitrary provider overrides, complete metadata/source ABI, E01 applicability, accepted implementation tasks and framework qualification remain open. The Java product still uses JDK APIs only; the .NET reference oracle is a development tool.

Next is the generic Encoding IsAlwaysNormalized contract and its selected normalization-form enum surface.
