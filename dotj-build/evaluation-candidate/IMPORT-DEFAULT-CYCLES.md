# Selected internal Default import cycles v1

This extension supports three selected Windows Default-profile cycle inputs.
It grants no F01-02, task, product, public ABI, full cycle-chain or message
acceptance. RecordDuplicateButNotCircularImports and RejectCircularImports
remain unsupported: their distinct null warning/error codes and exception
observations are preserved, not replaced by the Default policy.

The existing same-input Default capture already contains every required native
field. No additional native compilation/capture was necessary. The original 27
three-profile observations, 14 location observations, original 20 fixtures,
52 legacy case IDs, 10 location comparisons and all producer/lock bytes remain
unchanged. The new verifier derives a separate comparison envelope and bridge
from location-observations-v1.json; it never generates expectations from Java.

| Exact immutable input | P / Q | First-evaluation order | Current native notice | Context |
|---|---|---|---|---|
| BI03-two-file-cycle | root;one / empty | main.proj, one.props | MSB4210 at one.props 1:56, end 0:0 | Root main.proj; previous import absent |
| BI07-prior-cycle | empty / empty | main.proj, one.props | MSB4210 at one.props 1:10, end 0:0 | Root main.proj; previous import absent |
| BI08-nonroot-cycle | root;one;two / empty | main.proj, one.props, two.props | MSB4011 at two.props 1:56, end 0:0 | First import at main.proj 1:75; root context absent |

BI07 is byte-identical to the original NEG-cycle-import payload. That original
ID is still executed using its original two payloads and hashes, now with an
explicit native-supported disposition. The three historical matrix rows retain
their CYCLE_REFUSAL labels in the immutable old bridge; the runner records their
changed current disposition. cycle-predecessor-dispositions-v1.json enumerates
every predecessor and the four changed dispositions rather than deleting them.

Pinned Evaluator.cs:2146-2230 checks root re-import before duplicate imports,
logs SelfImport and ignores the edge. Under Default, the non-root active edge
uses the ordinary seen-import check and first-import context. Separate flag
branches account for different record/reject observations. The owned Java
implementation uses this small once-only policy: properties and file order stay
depth-first and every file is evaluated at most once. Existing sandbox, syntax,
DTD, file/import bounds and no-task restrictions remain in force.

The historical private DuplicateImport notice now also carries rootContext.
For an MSB4210 self-import this is the observed root path and previous is null;
for an MSB4011 duplicate previous is the first import site and rootContext is
null. A root has no prior importing element: no 0:0 or guessed previous site is
invented. Current positions continue to use the existing lexical index; native
unavailable end coordinates remain 0:0. No extra ancestor list or claimed native
cycle-chain field is added. Private JDK records do not qualify native public
Project, ElementLocation, ProjectLoadSettings or logger/exception ABI.

The native-derived verifier rejects fifteen malformed evidence/context controls,
including null code, invalid/missing coordinates, absent/mismatched root context,
mismatched previous context, invented previous root coordinates, wrong context
kind, changed cleanup/marker state and non-Default profile. Full localized
messages are retained and used only to cross-check the consumed context; the
candidate implements no full message. Success, cleanup counts and task-marker
absence remain retained native observations. Java repeat-call equality and
immutable snapshots establish per-call isolation, not public lifecycle equality.

Use the existing pinned Python to run `verify.py --focus-cycles --out <new-D-path>`.
The default runner checks all 52 legacy cases, ten acyclic location cases and
three selected cycle comparisons. The module still has zero exports/opens and
only java.base/java.xml runtime dependencies. .NET SDK 10.0.401, MSBuild 18.9.11,
runtime 10.0.12 and Roslyn/reference assemblies remain development/reference
tools; JDK 21 is the product runtime. No metadata-locked input changed, so the
separate compiled lifecycle inventory does not need a rerun.

Next work: specify and qualify a bounded non-Default load-profile contract
against the retained distinct native record/reject outcomes. Full cycle chains,
messages/public representation, E01-E03/N01/NF, general graphs/platforms, items,
SDK resolution and complete task acceptance remain open.
