# ActualValue serialization callback boundaries

Batch 2402: 448 payloads and two null-info controls compare 19832 exact metadata, identity, callback and error groups. A Reflection.Emit native object and a Java spy throw on ToString; 112 positive controls prove each spy is active after serialization, while payload capture leaves the mutable call counter untouched.

450 pinned native calls and 450 Java facade calls pass 19832 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to Batch 2401 and its packaged/API/retained evidence remains applicable; the full 417-check canonical gate remains required before merge.

Selected unthrown constructor payloads and explicit ToString spies only; arbitrary custom serializers, formatter restoration, stack/CLR ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Implement and qualify CultureNotFoundException invalid culture name/id serialization with native declared types and raw-message behavior.
