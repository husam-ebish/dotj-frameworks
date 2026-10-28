# Exception serialization Source mutations

Batch 2406: 1458 attempts compare 13122 exact callback, field, cache and error groups. Source callbacks write nullable/empty/raw Source and a side-effect HelpLink before returning null/text or throwing. Returned Source overwrites the callback assignment on success; a thrown getter leaves its assignment available to the next attempt. 486 backing-field null-input controls protect native input identity.

1458 pinned native calls and 1458 Java facade calls pass 13122 exact result/message/holder comparisons. Native producer, complete plan, pinned CoreLib and source archive hashes are verified. The product JAR is byte-identical to Batch 2405; its fresh packaged/API/retained evidence remains applicable; the full 421-check canonical gate remains required before merge.

Selected unthrown base Exception Source callback mutations only; arbitrary reentrancy, thrown/remote stacks, formatter restoration, CLR ABI and acceptance remain open. E01/E02/E03/N01/Q01 remain open. No task/framework acceptance credit. Numbered milestone 2500; total project batches unknown. JDK APIs are product dependencies; Python/.NET are validation tools. Temporary work stays on D. Next: Qualify prepopulated SerializationInfo collision order and partial writes across base and derived exception payloads, including early Source callbacks.
