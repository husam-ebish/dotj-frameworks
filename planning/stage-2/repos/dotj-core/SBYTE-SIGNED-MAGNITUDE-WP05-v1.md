# Selected SByte signed magnitude

Batch 2150 adds Abs, Sign, CopySign, MaxMagnitude and MinMagnitude. Abs and positive CopySign reject the unrepresentable magnitude of -128 with OverflowException. Negative CopySign preserves -128. Magnitude ties choose the positive value for MaxMagnitude and the negative value for MinMagnitude.

Pinned CoreLib 10.0.12 covers Abs/Sign for every signed-byte value and three pair operations across 23 anchors, totaling 2,099 consumer groups. Public signatures and overflow exception identity/HResult are checked. The small-integer signature audit grows to 97 selected native declarations, leaving 94 outside this selected scope.

Java null checks and immutable carrier references remain adapter behavior outside native value identity. Other arithmetic/parsing APIs, native generic interfaces, task acceptance and release qualification remain open. The product remains JDK-only, with all reference tools and temporary artifacts on D:.
