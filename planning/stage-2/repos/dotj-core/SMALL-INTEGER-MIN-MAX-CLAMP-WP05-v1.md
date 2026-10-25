# Selected small-integer Min, Max and Clamp

Batch 2148 adds static Min, Max and Clamp to SByte, Byte, UInt16 and UInt32. Comparisons use each carrier's full native value range, including unsigned UInt32 values above Int32.MaxValue. Clamp validates the bound ordering before choosing the input or an immutable bound carrier. Java null checks are adapter behavior outside the native value-argument domain.

Pinned CoreLib 10.0.12 records 196 value pairs and 686 clamp cases per type across fourteen values and seven bound anchors. Consumers verify 3,528 groups, both Min/Max argument orders, endpoint/interior results and invalid-bound ArgumentException identity, HResult and parameter name. The signature audit expands from twelve to fifteen selected projections per type, totaling sixty selected declarations; 131 remaining methods stay outside this audit scope.

Other arithmetic APIs, native generic interfaces, physical CLR boxing/value identity, implementation-task acceptance and release qualification remain open. Product dependencies remain JDK-only, and all validation intermediates stay on D:.
