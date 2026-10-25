# Selected UTF-8 destination-buffer behavior

Batch 2166 adds String/Char[] to Byte[] and Byte[] to Char[] destination overloads. Validation preserves null source then null destination precedence, negative source index/count, remaining source length and destination index checks. Capacity failure throws ArgumentException naming the destination array. Successfully converted prefixes remain written when later capacity or strict fallback errors occur; multibyte/scalar output packets are atomic.

Pinned native fixtures record 18,612 cases with null arrays, nonzero offsets, invalid ranges, zero/small/excess capacity, split surrogate and UTF-8 sequences, strict and replacement modes. The packaged consumer checks status/payload, complete destination contents after success or failure, and unchanged source for 55,836 groups. Strict failure indexes remain relative to the selected input slice.

This remains stateless conversion through the selected unsigned Byte[] adapter. Native source/value/array ABI, message parity, stateful conversion and flush, span/pointer overloads, fallback customization, type identity and WP-05-T2 acceptance remain open. Product runtime dependencies remain JDK-only; reference tools and all temporary artifacts remain separate on D:.
