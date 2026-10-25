# Selected typed Span copying

Batch 2083 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

Span and ReadOnlySpan now expose selected Length/IsEmpty getters plus CopyTo/TryCopyTo for the same generic destination element carrier. Char and Byte storage copies preserve complete code units/bytes, including zero, high-byte values and isolated UTF-16 surrogates. Copying uses a selected source snapshot before writing, preserving native overlap behavior in both directions. A short destination is untouched: TryCopyTo returns false; CopyTo throws ArgumentException with destination. Null destination and raw-erasure element mismatch checks are Java-host adaptations outside CLR ref-struct domains.

The pinned CoreLib 10.0.12 oracle invokes real Span/ReadOnlySpan constructors, properties and copy methods through emitted delegates. It records 7056 mutable/read-only, Char/Byte, copying/trying, independent/overlapping cases across twenty-one valid source and destination views, including empty tail slices and complete storage checks. All packaged groups pass; four mismatched-element Java programs are rejected. javap verifies selected getters/copy signatures; the broader public API preview passes.

The snapshot allocation is a Java carrier implementation choice and is not native allocation/lifetime parity. CLR byref/ref-struct identity, stack/pointer memory, concurrency, other element types, complete methods, language integration and foundation/release qualification remain open. These copy primitives support future typed formatting use across Java package boundaries. Product runtime dependencies remain JDK-only.
