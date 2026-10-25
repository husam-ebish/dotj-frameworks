# Selected UTF-8 Preamble property and heap aliases

Batch 2196 adds Encoding.get_Preamble() with the selected ReadOnlySpan<Byte> carrier. The property dispatches through GetPreamble, treats a null returned array as an empty view, propagates getter failures, and preserves live aliases when a derived getter returns a shared array. A derived getter returning a fresh clone preserves the independent earlier view. Built-in UTF-8 preambles remain independent of mutable arrays returned by earlier GetPreamble calls.

ReadOnlySpan gains a selected System.Byte[] backing option through overloads of its existing Java carrier factory OfUtf8Bytes. The factory is an explicit carrier adapter, not a newly claimed CLR public method. Copies and slices read current array entries; the property does not silently snapshot a shared derived preamble. Existing primitive Char/Byte views remain supported. CLR byref/ref-struct lifetime and arbitrary-element semantics remain unqualified.

Thirty pinned native profiles cover constructor flags, the default singleton/clone, shared/clone/null/throwing GetPreamble overrides and backing-array mutation between reads. The packaged consumer passes 612 groups, including three native snapshots, getter calls, backing state and composed slice checks. Existing copy/slice/mutation, numeric and encoding span suites remain regressions.

These selected heap views do not qualify pointer/stack/pinning identity, complete metadata/source ABI or WP-05 acceptance. No accepted task or qualified framework is credited. Next is selected UTF-8 Encoding.GetEncoding lookup overloads, aliases, fallback configurations and explicit boundaries for other code pages.
