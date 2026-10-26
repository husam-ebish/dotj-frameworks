# UTF16 returned-count encoder TryGetBytes heap spans

Batch 2264 qualifies TryGetBytes heap spans for every selected known returned stateless count context from the allocation corpus. The 138 original basis case IDs are each tested at six capacities and two destination offsets, yielding 1,656 native calls. The source view and replacement configuration match the basis exactly; source surrogate sentinels and three protected destination suffix bytes remain outside the visible views.

The packaged consumer passes 4,968 groups comparing success/failure, bytesWritten and entire destination buffers. The native capture records 632 insufficient-capacity returns and 48 exceptions. Count-based capacity decisions are preserved, including false returns that leave the destination unchanged and set bytesWritten to zero. Exception carriers and exact type/message/HResult/parameter are compared. Coverage requires every selected basis case, capacity and offset exactly once.

No additional product source correction is required after the encoder source/fallback scheduling correction. Runtime, allocation-reference fixture, Try producer/fixture, consumer and candidate JAR hashes bind the proof. Final integration requires the full foundation gate, retained consumers, compiled API audit and source/map/notice/distribution checks. Source inventory remains 98 and the API is unchanged.

The six unselected source/profile contexts and original native no-return outcomes remain unqualified. A final product liveness policy, arbitrary callbacks, unsafe pointers/lifetimes and complete byref/source ABI remain open. E01/E02/E03/N01/Q01 and task acceptance remain open; no implementation task or framework is accepted. Next is encoder replacement Convert, beginning with bounded native classification before returned-case implementation.

The product uses JDK APIs only; Python and pinned .NET are development/reference tools. Broader dependencies and public .j distribution remain unresolved. Scratch artifacts use D:\AI\Implementation\dotj Frameworks. Batch 2500 is the authorized milestone; total project batches remain unknown.
