# Selected Encoding cloning and read-only state

Batch 2169 adds the native System.ICloneable Clone() declaration and selected Encoding implementation. New encodings remain read-only. Clone creates a distinct writable instance, preserves constructor options and copies subclass fields through the JVM's shallow-clone mechanism. Cloning a clone remains distinct and writable. The Java Cloneable marker supports this internal mechanism and is not a native public contract.

Six pinned native profiles cover four UTF8Encoding constructor modes, Encoding.UTF8 and a generated subclass with a marker field. The packaged consumer passes 42 groups across direct and ICloneable dispatch, read-only state, identifier/code page, cloned runtime class, subclass field and strict/replacement conversion behavior.

Native Encoding.UTF8 has an internal UTF8EncodingSealed source runtime type and returns public UTF8Encoding from Clone. The selected candidate preserves the public cloned result; exact internal singleton runtime identity remains unqualified. Native fallback-reference sharing is recorded but awaits fallback-object implementation. Logical ICloneable type lookup, interface reflection, additional implementors, fallback customization, source/CLR ABI and WP-05-T2 acceptance remain open. No accepted task or framework qualification is credited.
