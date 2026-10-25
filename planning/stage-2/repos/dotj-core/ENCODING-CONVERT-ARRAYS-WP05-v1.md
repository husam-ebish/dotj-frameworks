# Selected Encoding.Convert array overloads

Batch 2198 adds the two static Encoding.Convert overloads for selected Encoding objects and System.Byte[] carriers. The whole-array overload checks bytes before delegating; the range overload checks srcEncoding, dstEncoding and bytes in that order. Range validation stays with the virtual source GetChars call. The destination receives that exact returned char[] through its virtual allocating GetBytes overload, and the conversion returns the destination array directly.

The pinned native capture and packaged consumer cover 3,786 scenarios and pass 34,074 groups. Seven UTF-8 configurations on each side cover BOM/strict settings, replacement and empty fallbacks. Selected valid/malformed byte inputs exercise whole arrays and padded slices. Combined null/invalid-range requests establish validation order. The 120 derived-dispatch scenarios record source/destination call order, seen indices/counts, source input identity, destination character-array identity, returned destination-array identity, null override results and throwing overrides. A source override may accept an otherwise invalid range; the static facade must not impose an earlier range check.

This is composition of the selected array encoding contracts. It does not add non-UTF-8 encoding implementations, providers, pointer or span conversion overloads, complete metadata/source ABI or WP-05 acceptance. The pinned Encoding.cs semantic reference is retained in the preceding UTF-8 lookup adjacency manifest and notice review remains open. No accepted task or qualified framework is credited.

Next is the native stateful Encoder/Decoder Convert contract and explicit output-carrier mapping before implementing partial-progress conversion.
