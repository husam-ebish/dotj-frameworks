# Selected unsigned integer Log2

Batch 2151 adds static Log2 to Byte, UInt16 and UInt32. Zero returns zero, and positive values return the index of the highest set bit. UInt32 calculations preserve the full unsigned 32-bit range through Java long storage.

Pinned CoreLib 10.0.12 covers every Byte value plus 46 UInt16 and 94 UInt32 values around powers of two, totaling 396 consumer groups. Compiled signatures are checked and the selected signature audit grows to 100 native declarations. The signed negative Log2 domain remains outside this batch.

Other APIs, native generic interfaces, CLR value ABI, task acceptance and release qualification remain open. Product runtime dependencies remain JDK-only; temporary builds and validation tools stay on D:.
