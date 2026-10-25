# Selected MethodImplAttributes format contracts

Batch 2113 advances DJ-001-N01-T2 without implementation acceptance credit.

Adds invariant G/F/D/X enum formatting, null/empty defaults, case-insensitive specifiers and FromInt32. MethodImplAttributes is not marked Flags in pinned CoreLib. G chooses the first named alias for exact values and signed decimal for unnamed values. F decomposes unsigned masks using the last matching alias: G(3) is CodeTypeMask while F(3) is Runtime; G(4) is ManagedMask while F(4) is Unmanaged. Both zero formats use IL. Formatting ignores the Java carrier's retained alias name so Managed, Runtime and Unmanaged constants still match their native boxed enum values. D is signed decimal; X is eight uppercase hexadecimal digits. Invalid formats throw FormatException; providers are ignored.

The oracle records all 18 declared fields as well as 282 unique values. Consumers explicitly format each named constant with G/F/D/X to catch alias behavior that FromInt32 alone cannot establish.

The pinned .NET 10.0.12 CoreLib reference and independent packaged Java consumer cover 13,327 groups. Evidence binds the reference script, runtime hash and tested JAR hash. Earlier profile checks are updated only when a newly implemented interface expands the supported projection. Native capture and Java consumer inputs include unnamed and signed anchor values rather than named values alone.

This is bounded inherited enum behavior. Physical enum/boxing identity, complete public API signatures, all remaining Enum APIs, language integration, reflection execution, full acceptance and framework release qualification remain open. Product runtime dependencies are JDK APIs only. Python, PowerShell and .NET are reference/development tools; all temporary artifacts and caches stay under D:\AI\Implementation\dotj Frameworks.
