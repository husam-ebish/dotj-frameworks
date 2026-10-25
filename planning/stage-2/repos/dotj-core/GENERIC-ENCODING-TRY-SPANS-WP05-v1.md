# Generic Encoding Try span virtual dispatch

Batch 2212 qualifies Encoding.TryGetBytes and TryGetChars with independently implemented span count/write overrides. Native and Java synthetic subclasses deliberately reject array callback dispatch. The generic base invokes the span count first, skips writing when required capacity is larger than the view, and otherwise calls the span writer exactly once.

The 3,584 native cases vary direction, multiplier, count/write callback modes, input lengths, destination lengths and view offsets. The packaged consumer passes 14,336 groups for outcome/exception, written slot, full guarded destination and exact ordered callback trace. Cases include throwing count callbacks, throwing writers after a destination mutation, negative callback returns and values larger than capacity. Exceptions preserve the old written slot; successful negative writer values remain native observations rather than normalized counts. Existing UTF8 Try span and encoding suites remain regressions.

No additional product change is required after Batch 2211. The native fixture binds runtime 10.0.12, CoreLib and producer hashes. The differential binds the versioned consumer, fixture and candidate JAR. Explicit LF attributes protect hash-bound evidence.

This is selected synthetic generic dispatch qualification. Arbitrary custom UTF8 fallback failures, pointer/ref-struct lifetime, full metadata/source ABI, E01 applicability and WP-05 task acceptance remain open. No accepted task, qualified framework or rights clearance is credited.

Next is custom UTF8 Try span fallback qualification, including callback exceptions that resemble destination-capacity failures.
