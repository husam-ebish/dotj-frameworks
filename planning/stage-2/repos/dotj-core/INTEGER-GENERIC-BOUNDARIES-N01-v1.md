# Integer generic constraint acceptance boundary

Batch 2160 records twelve native CreateChecked/CreateSaturating/CreateTruncating declarations and their INumberBase<TOther> constraints. The pinned .NET runtime rejects String, Boolean and DateTime generic instantiations with ArgumentException in all 36 controls.

The packaged Java consumer records the corresponding constraint gap: each method has an Object type-variable bound, those source expressions compile, and all 36 calls fail at runtime with UnsupportedOperationException. Together with twelve reflection controls, all 48 checks preserve this limitation as evidence. This is boundary qualification work, not native generic compatibility or accepted implementation-task credit.

The small-integer method inventory covers 191 native declarations through 151 direct projections and forty erasure-collapsed parsing signatures. Native generic constraints, distinct source identities, CLR value ABI, E01/E02/E03/N01 decisions and task acceptance remain open. Foundation qualification remains 0/66; implementation acceptance remains 0/1,092. The next independent implementation area is WP-05-T2: native Encoding/UTF8Encoding contracts and invalid-input fallback behavior, including explicit stateful and pointer-overload gaps.

The product remains JDK-only. Python, PowerShell and the pinned .NET runtime are development/reference tools. All temporary artifacts and toolchains stay under the project directory on D:.
