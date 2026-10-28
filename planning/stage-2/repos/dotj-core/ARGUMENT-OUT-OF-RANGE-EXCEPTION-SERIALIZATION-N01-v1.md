# ArgumentOutOfRangeException ActualValue serialization

Batch 2401: 672 payloads across seven nullable messages, eight parameter names, three actual-value carriers, two context flags and pre/post Message observation plus two null-info controls compare 28904 exact groups. ActualValue is declared Object even when null or a primitive/string carrier; serialization preserves its identity.

674 pinned native calls and 674 Java facade calls pass 28904 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The previous JAR omits ActualValue; the candidate adds the native declared Object field without formatting it; the full 416-check canonical gate remains required before merge.

Selected unthrown public-constructor payloads only; hostile formatting callbacks, arbitrary carriers, formatter restoration, thrown/remote stacks, CLR ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify ActualValue serialization with hostile ToString callbacks and mutable object identity without forcing Message formatting.
