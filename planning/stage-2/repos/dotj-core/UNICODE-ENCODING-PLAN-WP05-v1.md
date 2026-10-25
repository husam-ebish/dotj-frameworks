# UnicodeEncoding / UTF-16 reference and implementation plan

Batch 2231 establishes a pinned native reference packet and the next owned UTF-16 implementation plan for DJ-001-WP-05-T2. It adds no Java UnicodeEncoding class and gives no implementation-task acceptance credit. The product remains the existing 97-source JDK-only candidate.

The task explicitly requires mapping UTF encoders, fallback behavior, normalization and culture comparisons. The preceding NormalizationForm query/enum work does not implement text normalization or close that task. WORK-PACKAGES also requires exact public contract mapping, applicable E01/E02/E03/N01 closure, mapped fixtures and a migration example before acceptance. Those requirements remain open.

## Pinned source and runtime

The source is System.Private.CoreLib/src/System/Text/UnicodeEncoding.cs from runtime commit 4271d88e0aebf3d04f188f1334c2220d80555ef6. The 136239366-byte archive SHA-256 is ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115; the selected file SHA-256 is b5a717988edb22bae8688fb5cf9d8efe9d503dfe2918cdb5a9c95578a5768828. The verifier checks the repository archive manifest, actual archive and exact member bytes. Native capture requires runtime 10.0.12 and the previously pinned CoreLib SHA-256. Culture/UI-culture and producer hashes are recorded. Source/hash evidence does not close E01 rights applicability.

## Native reference scope

The corpus includes three constructor signatures, CharSize=2, nineteen declared public method records and eighteen states: the default constructor, eight endianness/BOM/strictness combinations and corresponding mutable clones using AB/CD replacements. It records 1224 whole-array conversion/count rows, 360 maximum-count rows and 324 ordered equality comparisons. Valid and malformed surrogate sequences, odd byte counts, both endian orders, preambles, fallback identities/maxima, read-only state and hashes are represented.

A separate Python contract model validates 1908 conversion/maximum/equality rows plus the eighteen states and declared-method projection. Replacement hash values use process-local seeds: only the unchecked formula from same-process code-page and fallback contributions is checked. No raw .NET/Java replacement hash equality is claimed. Five controls reject an incorrect runtime pin, producer digest, native result, source bytes or fabricated acceptance credit.

Decoder fallback indexes require care. UnicodeEncoding passes the current input pointer to DecoderFallbackBuffer.InternalFallback, which subtracts the unknown-byte length. A pending high surrogate followed by an invalid word can therefore report an index after its own byte offset; a trailing odd byte can also advance that index. The native payload and index are preserved. They must not be reconstructed by simply locating BytesUnknown in the original input.

## Implementation sequence and acceptance boundary

The versioned JSON plan projects all nineteen native declarations while leaving four pointer ABI routes and two specialized stateful factory contracts explicitly open. The first concrete task is an owned stateless UnicodeEncoding/UTF-16 array candidate: constructors/default fallbacks, code-page identity, preamble, maxima, equality/hash, aliases and byte/character conversions against this corpus. Capture range-validation and destination-partial-write behavior before qualifying those entry routes.

Subsequent work must cover inherited span/subclass dispatch and the specialized encoder/decoder state machines. The native encoder is EncoderNLS; the native decoder keeps both a pending byte and a pending high surrogate. Passing stateless rows cannot qualify those state machines, pointer/byref lifetimes, full source ABI or the entire work package. Mapped upstream/designed fixtures, culture comparisons, normalization transforms and applicability decisions still require separate evidence.

This sequence names contracts rather than a fixed number of project batches. The numbered milestone remains 2500; total project batches and project batches remaining remain unknown. No framework qualification, task acceptance or released SDK/feed is implied.

## Dependencies and validation

The Java product uses JDK APIs and gains no third-party runtime dependency. Python and the pinned SDK 10.0.401/runtime 10.0.12 remain development/reference-validation tools. The broader 66-framework dependency graph and public .j distribution model remain unresolved. A portable source-archive override is available through --source-archive or DOTJ_RUNTIME_SOURCE_ARCHIVE; old-machine installation paths are not version requirements.

The reference validator records whether a UnicodeEncoding class is present in the current JAR but never qualifies that implementation. Therefore it remains a reference/plan check when later implementation batches add the class. Canonical packaged builds, compiled API audit, source/class/notice inventory and the foundation gate remain mandatory. Next is Batch 2232, the first owned stateless UTF-16 array candidate, with all remaining acceptance gaps visible.
