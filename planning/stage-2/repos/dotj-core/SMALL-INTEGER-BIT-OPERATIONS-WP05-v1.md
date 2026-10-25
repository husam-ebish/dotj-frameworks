# Selected small-integer bit operations

Batch 2149 adds LeadingZeroCount, TrailingZeroCount, PopCount, RotateLeft, RotateRight, IsPow2, IsEvenInteger and IsOddInteger to SByte, Byte, UInt16 and UInt32. Operations mask to each native bit width; rotations wrap signed offsets modulo 8, 16 or 32. Signed-byte results retain two's-complement values, while IsPow2 rejects negative signed values.

Pinned CoreLib 10.0.12 covers all 256 values for each byte carrier, 46 UInt16 and 94 UInt32 values around power-of-two boundaries, and 27 offsets including both Int32 extremes. Packaged consumers check 18,256 groups through eight methods per carrier. The signature audit grows to 92 selected declarations, with four typed span erasure bridges and 99 remaining methods outside its selected scope.

Other arithmetic/parsing APIs, native generic interfaces, CLR value ABI, task acceptance and release qualification remain open. The product remains JDK-only; reference tools and all temporary artifacts remain on D:.
