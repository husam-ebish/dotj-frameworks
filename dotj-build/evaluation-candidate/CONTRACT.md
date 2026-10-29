# Evaluation contract v1

Status: internal executable candidate; product promotion blocked. Scope follows
the actual WP-01 plans and the predecessor native/candidate reports, whose
hashes are retained in [baseline-lock.json](evidence/baseline-lock.json).

## Source and oracle identity

The historical analysis pin remains
`dotnet/msbuild@6348d0c087aeec18c323b01a2c77da089ddafea0`.
The available implementation reference is separately identified as
`dotnet/msbuild@b44cdcec4c79c50c67560876707d57d4f635fa3b`, root tree
`3ffd98251b9d775b41982e28202f0febcb28666c`.
The official SDK VMR manifest attributed that component, and prior acquisition
verified its source blobs. Its `src` tree matched the installed SDK component;
VMR `eng` and `global.json` build inputs differed. This candidate does not claim
that a standalone build of the component reproduces SDK binaries.

Native observations were already captured using the installed official SDK
10.0.401 / MSBuild 18.9.11, explicitly pinned .NET runtime 10.0.12 with
`rollForward: Disable`. Native commands, raw outputs and host traces are locked,
not rerun. `producerSha256` in that native report hashes `capture-evaluation.py`,
not MSBuild.dll; the latter is separately bound by SDK-entry evidence.
Source-map canonical blob hashes differ from materialized file hashes because
the acquisition retained both representations. This runner verifies the
materialized bytes it reads. No source/binary download or rebaseline occurs.

## Supported input and behavior

Only namespace-free, SDK-less `Project` XML under an explicit existing sandbox
is eligible. The project plus at most 15 distinct imports may be read; each file is at
most 65,536 bytes. Inputs are controlled immutable fixtures, not a concurrent
hostile-filesystem sandbox. Existing ancestors and resolved files must remain
inside the declared sandbox. Filesystem races and a general MSBuild filesystem
security boundary are not qualified.

| Area | Executable contract |
|---|---|
| Properties | Explicit ASCII identifiers, ASCII case-insensitive lookup, source-order assignment and one-pass expansion of values already assigned. Forward/undefined references become empty. Stored values remain escaped until retrieval. |
| Globals | Explicit caller-supplied values precede assignments. A global cannot be overwritten except for one explicitly named root `TreatAsLocalProperty` property. No ambient environment or toolset prelude is imported. |
| Imports | Literal relative slash paths; depth-first first-import order; repeated acyclic resolved files are ignored after the first evaluation and recorded as private `MSB4011` code/owner/target notices. Nested paths resolve relative to the defining file. A false condition skips the read; a true missing import yields private failure code `MSB4019` with owner/missing paths. |
| Conditions | Empty condition, lowercase literal `true`/`false`, single-quoted alphabetic/empty ASCII string equality, and selected literal `Exists('relative/path')`. ASCII folding is explicit. Numeric/version/boolean-alias coercion, Unicode comparisons and general operators refuse. |
| Escapes | One-pass `%25`, `%3B`, `%24`, case-insensitive hex. Other percent escapes refuse when evaluated/retrieved; full MSBuild escaping is not implemented. |
| XML | JDK DOM with DTD/entity/external DTD/schema access disabled, no namespace or XInclude processing. Unsupported structural elements/attributes and static property functions refuse, including in skipped groups. |
| Validation | All declared conditions are syntax-checked without property reads/filesystem probes, even inside skipped groups. Actual expansion still occurs at the original evaluation point. This fail-closed policy is a candidate restriction, not a claim that native MSBuild rejects the same skipped input. |
| Targets | Selected `Target` declarations containing `WriteLinesToFile` or `Error` are inert data only. There is no task registry, task invocation, process launch, restore or network operation. `DefaultTargets`/`InitialTargets` never schedule execution. |
| Results | Per-call state and immutable result snapshots. Private JDK types do not qualify a public .NET collection, string, path or exception contract. |

The inherited evaluator remains intentionally narrow. Unsupported property
reference/escape forms in unevaluated scalar data may remain unevaluated; they
are not supported operations. An accepted document does not certify every
unexecuted scalar expression as native-compatible. Property functions detected
by the selected static guard, unknown conditions and unsupported structures
are refused before evaluation.

## Refusals and qualification limits

Missing/empty, dynamic, list and glob import-path syntax is rejected statically,
including in skipped imports and import groups. Absolute/URI/backslash paths
and outside-sandbox imports are rejected when the import is evaluated; false
import or import-group conditions skip those path checks and the import read.
SDK attributes/resolvers and implicit imports, ItemGroup/items/metadata/globs,
property functions, cycles, reserved `MSBuild*` properties,
non-ASCII property names/comparison and unqualified condition coercions refuse.
Cycles currently produce `IMPORT_CYCLE_UNQUALIFIED`, **not a
source-compatible chain diagnostic**. Acyclic duplicate imports now use the captured once-only policy; native warning
source locations, previous-import context and text remain unimplemented. The private missing-import failure does not
implement `InvalidProjectFileException`, native text, source lines or HResult.

The independent ordinal-comparison prototype is not imported. The central
research index explicitly leaves full Unicode equivalence unqualified and the
build evaluator's ASCII restriction unchanged.

## Fixtures and normalization

The 24 original native fixture files are retained byte-for-byte. The runner
copies them into its new private output and changes exactly one absolute
fixture-root prefix in BE19's inert marker attribute. The inverse replacement
restores the original bytes. Property values receive no normalization. The
missing path is compared relative to the declared fixture root. Native producer
properties `MSBuildRuntimeType` and `MSBuildVersion` are excluded from semantic
comparison and retained as oracle identity, not implemented Java properties.

BE01–BE20 are designed captures, not invented upstream test IDs. Relevant real
methods in the locked `Evaluator_Tests.cs` include `EmptyPropertyIsThenSet`,
`SetPropertyToItself`, `UsePropertyInCondition`, `UsePropertyBeforeSet`,
`ImportsOnlyIncludedOnce`, `VerifyConditionsInsideOutsideTargets`,
`VerifyGlobalPropertyOverridesIfNoTreatAsLocalProperty` and
`VerifyLocalPropertyOverridesIfTreatAsLocalPropertySet`. They were source
anchors; their `Build()`-using upstream tests were not run or ported here.
The native tranche was independently captured through evaluation-only
`-getProperty` without a target or restore switch.

## Acceptance disposition

| Requirement | Actual evidence | Remaining gap |
|---|---|---|
| F01-01 deterministic imports/expansion | Existing bounded 20-case replay plus the same-input acyclic import matrix | Full properties/items/conditions/environment and platform contract |
| F01-02 cycles report chains | Three distinct cycle inputs captured under three native load profiles; candidate explicitly refuses cycles | Source-compatible chain/error policy; native warning/ignore or pair diagnostics do not qualify full chains |
| F01-03 Windows/Linux globs | Item/glob refusal | Entire item/glob and Linux/case matrix |
| F01-04 no task execution | Native and candidate marker absent; packaged code has no execution engine | Full eligible public evaluation profile and forbidden-feature coverage |
| E01 | Immutable reports/source/tool/runtime hashes retained | Release/profile/rights/notice/build-input eligibility closure |
| E02/E03 | Selected source anchors, fixtures and captured outputs retained | Semantic inventory, effective dependencies, reviewed fixture/API contract |
| N01 / NF01–NF03 | No replacement API exported; explicit source-signature gaps retained | Compiler-derived public mapping, exact API diff and paired compiled C#/.j examples |

No WP01 task, package, NF case, numbered batch or release acceptance is claimed.
The selected compiled lifecycle mapping is now retained separately in planning.
The next behavior scope is a separately specified cycle policy and diagnostic
chain contract, grounded in the distinct observed load profiles; public dependency
representation, eligibility and lifecycle work still precede public promotion. New semantic coverage needs real
native captures; the predecessor observations do not authorize guessed behavior.

## Explicit-import extension v1

[IMPORT-BEHAVIOR.md](IMPORT-BEHAVIOR.md) is the bounded extension contract and
per-observable disposition. Its immutable nine-case corpus and two native runs
retain all three load profiles, ordered diagnostics, original source positions,
null codes, failures and unload/disposal observations. Only acyclic once-only
properties/import order and private notice code/owner/target order are compared
as supported behavior. No public logger, diagnostic or load-settings API is added.
