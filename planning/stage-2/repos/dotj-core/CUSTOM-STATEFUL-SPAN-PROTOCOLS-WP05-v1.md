# Custom stateful span callback protocols

Batch 2210 qualifies the selected UTF-8 Encoder/Decoder heap span count, write and Convert adapters with custom fallback providers. The corpus records 88 profiles (44 per direction), 616 independent sequences and 3,520 calls. Its packaged consumer passes 19,712 comparison groups: exact success/count or exception identity, HRESULT and parameter, factory calls, all five buffer callback counters, destination guards, used slots and completion state.

The four replacement templates include surrogate pairs, embedded NUL and an unpaired high surrogate. Eleven provider modes include throwing Remaining, Next, Fallback and Reset callbacks, false Fallback, unusual rewind behavior, and null or throwing buffer factories. Overflow, fallback changes, reset and later recovery are observed in sequences. Guarded source/destination slices check the view boundaries. All selected cases already agree after the preceding NLS override and generic adapter corrections; this batch adds qualification evidence rather than another product behavior change.

The native fixture runs the pinned runtime 10.0.12 and binds its CoreLib and producer hashes. The differential record binds the native fixture, versioned custom-provider consumer and candidate JAR. Native fixture bytes and LF differential output have explicit Git attributes. Existing stateful, generic span and Convert regressions remain required.

This is bounded heap span callback evidence. Arbitrary reentrancy, direct pointer overrides, CLR lifetime and pinning, full source/reflection ABI, E01 applicability and WP-05 task acceptance remain open. No accepted implementation task, qualified framework or rights clearance is credited.

Next is implementation and qualification of Encoding.TryGetBytes and TryGetChars heap span projections, including capacity failure, exception/output ordering and guarded destinations.
