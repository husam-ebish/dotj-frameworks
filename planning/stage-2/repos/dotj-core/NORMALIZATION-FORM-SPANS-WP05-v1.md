# NormalizationForm selected Char span formatting

Batch 2229 implements the selected ISpanFormattable array bridge and heap-Span overload on the provisional NormalizationForm carrier. Formatting uses the preceding G/F/D/X contract. Sufficient capacity writes the complete result and count; insufficient capacity returns false, writes zero and preserves the buffer. Invalid format exceptions preserve the previous count and buffer. Heap slices preserve prefix/suffix sentinels. Provider queries remain unused.

The pinned native corpus contains 1580 buffers across fourteen Int32 values, thirteen formats, capacity boundaries and whole-array versus offset-slice destinations. Its Reflection.Emit bridge calls ISpanFormattable directly with a throwing provider. The packaged consumer compares outcomes, exact exceptions, written counts and every destination character. Four native interface assignability checks and the absent UTF8 interface produce 3165 groups; a separate compile control rejects IUtf8SpanFormattable assignment. The enum exposes character formatting without claiming UTF8 formatting.

The class inventory remains 97 Java sources. Both builders, owned-map binding, distribution/rights-input checks, compiled API audit and retained encoding/enum consumers remain required. CoreLib, producer, fixture, consumer and JAR hashes bind the evidence; LF attributes cover source and evidence. No new Java runtime library is added.

These are heap-carrier character buffers. Byref lifetimes, UTF8 formatting, complete enum ABI, normalization transforms, E01 applicability, task acceptance and framework qualification remain open. No acceptance credit is claimed. Next is signed HasFlag behavior and null/unrelated enum arguments.
