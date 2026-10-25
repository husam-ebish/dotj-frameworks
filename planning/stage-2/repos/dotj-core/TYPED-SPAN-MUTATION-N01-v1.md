# Selected Span Clear and Fill

Batch 2102 adds Clear() and Fill(T) to mutable Char/Byte spans. Both operations affect only the selected backing-array range. Clear writes the selected element's zero value. Fill accepts Character or System.Byte through the typed factory and generic carrier. Java null/wrong-erased-carrier inputs are rejected as adapter-domain errors, outside CLR Char/Byte value inputs.

The pinned .NET 10.0.12 reference records 336 cases across 21 subviews, empty views, clearing and Char/Byte fill values including high bytes and surrogate code units. The consumer verifies the complete backing array so changes outside a view fail. Two wrong-element Fill calls must fail compilation for generic type mismatch.

Other element types, CLR byref lifetimes, ref returns, pointers, pinning, concurrency, full API qualification and acceptance remain open. The Java product remains JDK-only. All intermediate builds and reference tools stay on D:.
