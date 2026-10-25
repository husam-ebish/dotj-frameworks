# Selected small-integer Char and UTF-8 span parsing

Batch 2154 adds Parse(ReadOnlySpan<T>, provider), TryParse(ReadOnlySpan<T>, output) and TryParse(ReadOnlySpan<T>, provider, output) to SByte, Byte, UInt16 and UInt32. The selected heap-view factory domain is Char or UTF-8 Byte. Java generic erasure collapses six native overloads into three typed parsing methods per carrier; the native output type remains fixed to that numeric carrier.

Pinned CoreLib 10.0.12 captures 868 text/byte sources, including 398 existing String inputs in both encodings, malformed UTF-8, multibyte signs, and eleven focused configured-sign profiles. The base matrix uses invariant, custom ASCII and Unicode numeric signs; seven minus variants and four non-alias controls also check ASCII-hyphen leniency. The finite sign rule is independently documented in the hash-verified pinned runtime source archive, System/Globalization/NumberFormatInfo.cs. It is implemented in the shared Integer grammar, with String-parsing regressions retained.

Consumers verify 47,136 groups through direct and offset heap views. They preserve backing storage, check native values/errors and output slots, and include 144 native format-provider controls across Char/Byte inputs. Four mismatched numeric output arrays must fail compilation. All 9,672 String-parsing regression groups also pass with explicit UTF-8 fixture decoding.

The signature audit distinguishes 120 direct declaration projections from 24 native parsing overloads represented through twelve typed parsing bridges. Four existing formatting bridges remain separate. This records Java adaptation rather than exact native generic/ABI equivalence.

Arbitrary NumberStyles, additional culture/provider profiles, native generic interfaces, CLR byref lifetimes, implementation-task acceptance and release qualification remain open. Runtime dependencies remain JDK-only; all reference tooling, generated consumers and temporary artifacts stay on D:.
