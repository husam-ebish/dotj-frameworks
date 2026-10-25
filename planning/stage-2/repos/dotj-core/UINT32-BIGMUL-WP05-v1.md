# UInt32 full-width multiplication

Batch 2158 adds BigMul using the existing foundation convention that System.UInt64 values are carried by JDK BigInteger. Both UInt32 operands retain their unsigned range, so the maximum product is represented without signed-long overflow. The existing logical UInt64 instance projection is checked.

Pinned CoreLib 10.0.12 supplies 49,284 products across 94 power-of-two boundary values plus 128 deterministic full-range samples. Consumers check exact decimal products, nonnegative 64-bit range and the compiled return signature. The selected method inventory grows to 139 direct projections plus forty native parsing overloads represented through typed bridges.

Physical CLR UInt64 value ABI, generic-interface constraints, implementation-task acceptance and release qualification remain open. The product remains JDK-only; temporary files and reference tools remain on D:.
