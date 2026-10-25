# Small-integer quotient and remainder

Batch 2157 adds DivRem to SByte, Byte, UInt16 and UInt32. It returns the existing typed ValueTuple carrier with quotient in Item1 and remainder in Item2. A zero divisor raises the selected DivideByZeroException with native HResult. Signed-byte -128 / -1 returns (-128, 0), preserving the native quotient narrowing behavior.

Pinned CoreLib 10.0.12 supplies every SByte and Byte pair and all pairs of the existing wider power-of-two boundary values: 142,024 cases, including 652 divide-by-zero cases. Packaged consumers compile the typed tuple signatures and verify both result fields or exact exception identity/HResult. The signature audit now records 138 direct projections and forty native parsing overloads represented through typed bridges.

The Java tuple is a heap object with fields; CLR value-copy/tuple ABI and native generic interfaces remain outside this bounded evidence. Other numeric APIs, implementation-task acceptance and release qualification remain open. Runtime dependencies remain JDK-only; all temporary validation artifacts stay on D:.
