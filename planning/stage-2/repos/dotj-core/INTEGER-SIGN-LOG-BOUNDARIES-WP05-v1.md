# Selected integer sign and logarithm boundaries

Batch 2152 adds SByte.Log2 and Byte/UInt16/UInt32.Sign. Signed logarithms return the highest set-bit index for nonnegative inputs, including zero; negative inputs use the existing ArgumentOutOfRangeException carrier. Unsigned Sign returns zero for zero and one for positive values.

Pinned CoreLib 10.0.12 records 652 cases, including every SByte/Byte value and power-of-two boundary values for the wider unsigned types. All 128 negative signed-byte inputs verify exception identity, HResult, parameter name, null actual value and invariant English message. Public signatures are checked and the selected signature inventory grows to 104 native declarations.

Other numeric APIs and culture profiles, native generic interfaces, CLR value ABI, task acceptance and release qualification remain open. Runtime dependencies remain JDK-only; validation artifacts and tools stay on D:.
