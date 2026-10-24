# Selected array factory and metadata candidate

Plan scope: `DJ-001-WP-01-T1`, in progress. No implementation-task acceptance credit is granted.

| Native operation | Selected Java behavior | Evidence boundary |
|---|---|---|
| Type.MakeArrayType() | Creates a single-dimensional vector; rejects Void and by-reference element types | Selected class, primitive/value and pointer element types |
| Type.MakeArrayType(rank) | Accepts ranks 1 through 32; rank 1 produces a non-vector `[*]` type | Selected ranks 1, 2, 3 and 32 |
| Invalid rank | Rank below 1 throws IndexOutOfRangeException before element validation; rank above 32 throws TypeLoadException | Int32 extrema, -1, 0 and 33 are compared with pinned CLR type/HResult results |
| Element constraints | Void and by-reference elements fail with TypeLoadException for valid ranks; pointer elements, including Void pointers, retain selected array metadata | Metadata only; no pointer or rectangular runtime storage/language qualification |
| Metadata | Names, namespace, rank, vector/variable-bound flags, base/element identity, class/value flags and sealed status | 110 pinned cases; qualified type-cache identity only for the tested factory paths |

The existing selected reference/value-vector relationship matrix checks covariance, invariance and runtime component matching. Higher-rank runtime instance carriers, arbitrary generic/raw/jagged representations, full allocation semantics, source-language lowering and E01/E02/E03/N01 release qualification remain open. A passing factory or metadata gate does not qualify the framework.

Batch 2055 adds selected name lookup for array, pointer and by-reference compositions. Recursive suffix resolution now uses the selected core-name resolver for its element, enabling plain names such as System.DayOfWeek* and System.TimeSpan[,][] as well as CoreLib-qualified forms. The 1,152 pinned cases cover eight base types, twelve compositions, canonical/lowercase/CoreLib-qualified input, both case flags and both throw flags. Successful lookups preserve factory cache identity, full/simple/element names and array/pointer/by-reference/enum flags. General malformed-name grammar, arbitrary ranks and assembly resolution remain open.
