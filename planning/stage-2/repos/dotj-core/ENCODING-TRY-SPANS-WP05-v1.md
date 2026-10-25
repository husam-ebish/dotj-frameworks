# Encoding TryGetBytes and TryGetChars heap span projections

Batch 2211 adds the selected public Encoding.TryGetBytes(ReadOnlySpan<Character>, Span<Byte>, int[]) and TryGetChars(ReadOnlySpan<Byte>, Span<Character>, int[]) projections. The one-element int arrays adapt native out parameters. The generic base performs a virtual count, checks capacity, then performs a virtual write; insufficient capacity sets the output count to zero.

UTF8Encoding overrides preserve the existing incremental destination writes. An exact destination-capacity ArgumentException is translated into false and a zero written count. Fallback exceptions propagate and preserve the previous output count. Existing span adapters retain destination writes on exceptions. These projections have explicit Java null/empty output-slot guards; they are adapter boundaries, not native-null-span behavior.

The pinned runtime corpus covers 2,952 guarded source/destination requests under seven configurations (20,664 scenarios). The packaged consumer passes 61,992 groups for result or complete exception payload, destination contents and written slot. Four wrong-carrier compile controls also pass. Tests include replacement, strict, empty/custom replacement templates, sliced UTF-16/UTF-8 inputs, offsets and capacities. Native fixture, producer, input fixture and candidate JAR hashes are bound. All 94 product Java sources, owned-file map, distribution, rights-input audit and retained stateful/stateless encoding regressions pass. The compiled selected CoreLib identity audit passes.

The implementation adds no external runtime dependency. Bounded evidence does not qualify arbitrary custom provider exceptions, generic subclass dispatch, CLR ref-struct/pointer lifetime, complete metadata/source ABI or WP-05 acceptance. E01 applicability, accepted implementation tasks and framework qualification remain open. No rights clearance is credited.

Next is native qualification of generic Encoding.Try span count/write dispatch, callback failures, negative returns and output ordering.
