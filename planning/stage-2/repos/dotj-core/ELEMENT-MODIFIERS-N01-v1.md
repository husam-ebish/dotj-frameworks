# Selected symbolic element modifiers

Plan scope: `DJ-001-WP-01-T1`, in progress. These are Type metadata carriers, not executable pointer or by-reference storage.

The 48-case pinned CLR corpus covers Stopwatch, Object, String, DateTime, Int32 and Void elements with direct, array, by-reference and pointer inputs, followed by MakeByRefType or MakePointerType. It retains factory errors, cache/element identity, names, namespace, classification, base/type-code queries, assignability, subclass and instance results.

For these successful symbolic types, CLR reports IsClass true and IsSubclassOf(Object) true despite BaseType being null and Object assignability being false. The Java carrier preserves this distinction. Reapplying modifiers to a by-reference input and invalid Void-array inputs retain the selected TypeLoadException behavior and HResult.

Raw memory, dereferencing, by-reference lifetime, runtime argument/return lowering, arbitrary generic composition, full reflection and E01/E02/E03/N01 release qualification remain open. No implementation task is accepted by the bounded result.
