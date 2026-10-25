# Selected UTF-8 Encoder Convert boundaries and cross-API transitions

Batch 2201 qualifies the selected predefined-fallback Encoder.Convert array behavior beyond the preceding ordinary progress sequences. It adds pinned native controls and a compiled packaged consumer; the implementation already satisfies these controls, so no Java behavior patch is needed.

The fixture has 110 request forms, 1,356 sequences and 4,926 actions. Null source/destination combinations, negative and oversized index/count values and conflicting invalid parameters pin validation priority. Pending-high-surrogate setup and later recovery expose unintended state changes after failed validation. Six UTF-8 configurations cover BOM and strict flags plus replacement and empty fallback settings.

Seventy-two alias controls pass one native managed integer location for both out arguments. The Java consumer passes the same int[] carrier for charsUsed and bytesUsed. The pinned EncoderNLS assignment order leaves the consumed-character count in that location, including when byte and character counts differ. This qualifies that selected carrier alias adaptation, not arbitrary CLR byref identity or source ABI.

Thirty-six cross-API sequences exercise Convert followed by counting, fallback replacement, writing, another conversion and Reset. A partially drained fallback makes GetByteCount throw without consuming the buffered output; a fallback setter rejects the pending buffer; GetBytes can drain it; the setter subsequently succeeds. Full destination arrays, raw output sentinels, completion and fallback Remaining are checked after every action. The consumer passes 32,502 groups.

This bounded qualification does not implement generic-base or custom-provider Convert, Decoder Convert, pointer/span forms, full reflection/source ABI or WP-05 acceptance. No accepted implementation task, framework qualification or rights clearance is credited. Next is selected custom fallback-provider Encoder Convert behavior and callback/capacity recovery against pinned native controls.
