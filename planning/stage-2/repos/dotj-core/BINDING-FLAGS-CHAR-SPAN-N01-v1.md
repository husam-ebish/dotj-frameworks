# BindingFlags character-span formatting

Batch 2099 extends the selected BindingFlags Java carrier with ISpanFormattable. The raw char-array adapter and typed Span<Character>/ReadOnlySpan<Character> overload preserve enum formatting, ignored providers, short-buffer false/zero results, unchanged destinations on insufficient capacity, and format exceptions before buffer mutation. Type reports the four supported enum interfaces and explicitly excludes IUtf8SpanFormattable.

The pinned .NET 10.0.12 reference records 2,244 buffer cases and 84 span text cases. Packaged consumers exercise 9,145 groups through raw arrays, interface calls and offset views. Two mismatched Byte carrier calls must fail compilation for a type mismatch. The initial negative probe used a nonexistent None field; it was corrected to the existing Default field and rerun, so rejection now tests carrier typing.

This is bounded Char/Byte heap-view interoperability. CLR byref lifetimes, physical enum identity, other Enum members, language integration, complete API qualification and acceptance remain open. The product uses only JDK APIs; validation tools and temporary artifacts remain on D:.
