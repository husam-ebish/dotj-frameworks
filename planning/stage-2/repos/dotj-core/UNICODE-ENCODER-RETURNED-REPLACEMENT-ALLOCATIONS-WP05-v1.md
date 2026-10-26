# UTF16 returned encoder replacement allocations

Batch 2263 qualifies stateless encoder allocating surfaces for all 138 selected known returned count contexts under eighteen endian/replacement configurations. Selection requires a returned original reference row with encode=true, stateful=false and countBefore=true; source values are deduplicated per profile. Six of the original 144 stateless source/profile combinations are not selected and remain unqualified. The producer verifies the pinned public string-range GetBytes allocation signature before invoking it.

Each context calls array and string counts plus allocating GetBytes for array range, whole array, string range and whole string. Range inputs have protected surrogate sentinels. The packaged consumer passes 1,364 groups across 828 native calls, including 536 returned allocated byte arrays and 24 exception outcomes. It verifies the exact original context selection, reference count result, returned lengths and every byte, plus exact failures. The count-returning selection is a bound on this proof; it does not establish return behavior for the excluded contexts or all possible inputs.

No additional product source correction is required after the encoder source/fallback scheduling correction. Runtime, original reference, allocation producer/fixture, consumer and candidate JAR hashes bind the proof. Final integration requires the full foundation gate, retained consumers, compiled API audit and source/map/notice/distribution checks. Source inventory remains 98 and the API is unchanged.

Original native no-return outcomes, a final product liveness policy, arbitrary callbacks, unsafe pointers/lifetimes and complete byref/source ABI remain open. E01/E02/E03/N01/Q01 and task acceptance remain open; no task or framework is accepted. The next task is TryGetBytes heap spans for the same known returned count contexts.

The product uses JDK APIs only; Python and pinned .NET are development/reference tools. Broader dependencies and public .j distribution remain unresolved. Scratch artifacts use D:\AI\Implementation\dotj Frameworks. Batch 2500 is the authorized milestone; total project batches remain unknown.
