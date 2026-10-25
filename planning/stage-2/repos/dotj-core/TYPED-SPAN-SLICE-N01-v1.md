# Selected typed span slicing

Batch 2101 adds Slice(int) and Slice(int,int) to the Char and Byte Span<T>/ReadOnlySpan<T> carriers. Slices share their backing array and add to the existing offset. Empty end slices are valid. Negative or out-of-view start/length values throw ArgumentOutOfRangeException with a null parameter name. Subtraction-based bounds checks avoid integer overflow before constructing a view.

The pinned .NET 10.0.12 reference records 9,240 cases across mutable/read-only Char/Byte views, both overloads, valid subviews, negative bounds and Int32 extremes. Consumers verify length, emptiness, copied contents, full original storage, exceptions, and alias visibility through mutations. Four invalid generic return assignments must fail compilation for mismatched carriers.

This is a selected heap-view implementation. It does not implement the CLR ref-return indexer, stack/byref lifetime rules, arbitrary element types, pointers, pinning or concurrency guarantees. No implementation task or framework qualification receives acceptance credit. The Java runtime uses JDK APIs only; temporary builds and validation tools stay under D:\AI\Implementation\dotj Frameworks.
