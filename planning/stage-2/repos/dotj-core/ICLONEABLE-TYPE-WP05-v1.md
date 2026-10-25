# Selected ICloneable and Encoding interface metadata

Batch 2170 adds logical ICloneable lookup and interface/class flags, plus Encoding/UTF8Encoding GetInterfaces/GetInterface projection and assignability. The JVM Cloneable marker is hidden from these selected native interface lists. ICloneable has no base type or inherited interfaces; Encoding and UTF8Encoding each expose the native ICloneable contract.

Pinned CoreLib records three owner metadata rows, 42 interface-name queries, 36 assignability/subclass pairs and 42 instance cases. The packaged consumer verifies 162 groups including canonical and assembly-qualified ICloneable lookup and the compiled parameterless Object Clone() declaration.

The evidence explicitly records additional native String/Array implementors as unqualified. Their complete interface lists and Clone invocation/lowering remain separate work. Full member reflection, fallback objects, internal Encoding.UTF8 runtime identity, source/CLR ABI and WP-05-T2 acceptance remain open. No accepted task or framework qualification is credited. Next is the source-derived encoder/decoder fallback contract and buffer inventory before customization implementation.
