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
| Imports | Literal relative slash paths and bounded property-expanded single explicit paths (see IMPORT-PATH-EXPANSION.md); depth-first first-import order; each file evaluates once. Under the selected Default policy, repeats including non-root active ancestors emit private `MSB4011` notices with first-import context; root re-imports emit `MSB4210` with root-path context and no previous import site. Nested paths resolve relative to the defining file. A false condition skips the read; a true missing import yields private failure code `MSB4019` with owner/missing paths. |
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

Literal-empty, malformed dynamic, list and glob import-path syntax is rejected
statically, including skipped imports/groups. Well-formed ASCII property
references expand once after true conditions. Raw absolute/URI/backslash syntax
refuses statically; such syntax introduced by property values and outside-sandbox
paths refuses when evaluated. False conditions skip expansion, value validation
and target reads. Evaluated empty expansion has the observed MSB4020 failure
with no target; see IMPORT-PATH-EXPANSION.md for this Default-only qualification.
SDK attributes/resolvers and implicit imports, ItemGroup/items/metadata/globs,
property functions, reserved `MSBuild*` properties,
non-ASCII property names/comparison and unqualified condition coercions refuse.
The selected Default root/non-root cycles use the captured warning/ignore policy,
**not a source-compatible full cycle-chain diagnostic**. Duplicate imports use the captured once-only policy; native warning
current source locations and directly observed first-import context are now compared by the bounded [source-location extension](IMPORT-LOCATIONS.md); full text remains unimplemented. The private import failure does not
implement `InvalidProjectFileException`, native text or HResult. The bounded
[internal profile extension](IMPORT-PROFILES.md) adds the two individually observed
record/reject settings; combined flags and a public selector remain unqualified.

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
| F01-02 cycles report chains | Three distinct cycle inputs captured under three native load profiles; selected Default warning/ignore, ordering and current/root/previous context now compare | Full cycle-chain contract, other load profiles and public representation; Default warnings do not qualify full chains |
| F01-03 Windows/Linux globs | Item/glob refusal | Entire item/glob and Linux/case matrix |
| F01-04 no task execution | Native and candidate marker absent; packaged code has no execution engine | Full eligible public evaluation profile and forbidden-feature coverage |
| E01 | Immutable reports/source/tool/runtime hashes retained | Release/profile/rights/notice/build-input eligibility closure |
| E02/E03 | Selected source anchors, fixtures and captured outputs retained | Semantic inventory, effective dependencies, reviewed fixture/API contract |
| N01 / NF01–NF03 | No replacement API exported; explicit source-signature gaps retained | Compiler-derived public mapping, exact API diff and paired compiled C#/.j examples |

No WP01 task, package, NF case, numbered batch or release acceptance is claimed.
The selected compiled lifecycle mapping is now retained separately in planning.
The remaining behavior scope includes the full diagnostic
chain contract and additional load settings; public dependency
representation, eligibility and lifecycle work still precede public promotion. New semantic coverage needs real
native captures; the predecessor observations do not authorize guessed behavior.

## Explicit-import extension v1

[IMPORT-BEHAVIOR.md](IMPORT-BEHAVIOR.md) is the bounded extension contract and
per-observable disposition. Its immutable nine-case corpus and two native runs
retain all three load profiles, ordered diagnostics, original source positions,
null codes, failures and unload/disposal observations. Only acyclic once-only
properties/import order and private notice code/owner/target order are compared
as supported behavior. No public logger, diagnostic or load-settings API is added.

## Acyclic import source locations v1

[IMPORT-LOCATIONS.md](IMPORT-LOCATIONS.md) supersedes the original source-location
and previous-context gaps only for its selected internal Default-profile fields.
All 52 predecessor inputs/dispositions and 27 historical native observations
remain intact; cycle/public/message acceptance remains open.

## Selected Default import cycles v1

[IMPORT-DEFAULT-CYCLES.md](IMPORT-DEFAULT-CYCLES.md) supersedes the earlier
explicit cycle refusals only for its bounded internal Default behavior. All 52
legacy IDs and ten location comparisons remain; the three selected cycle inputs
also compare native notice coordinates and honest root/previous context absence.
Historical producer/observation bytes remain unchanged. The bounded record/reject
profile gap is superseded below; full chains/messages/public ABI and task acceptance
remain open.


## Selected individual import profiles v1

[IMPORT-PROFILES.md](IMPORT-PROFILES.md) adds package-private record/reject
selection on the original nine inputs. Eighteen new same-profile native captures
supply diagnostic and failure ends without borrowing Default coordinates, while
preserving every pre-existing native field. Immutable import edges, nullable
record-list availability, ordered warning/error snapshots and typed missing vs
circular failures are compared. Root imports keep their earlier precedence;
completed shared imports remain ordinary duplicates. All 65 retained packaged
comparisons and their IDs remain, plus 18 selected profile comparisons. No
public .NET facade, full cycle chain, combined flags or acceptance credit is added.


## Property-expanded single explicit paths v1

[IMPORT-PATH-EXPANSION.md](IMPORT-PATH-EXPANSION.md) defines the eight native-backed
Default cases, observed empty-expression failures, strict expression/value limits
and the exact legacy disposition transition. All83 prior comparison obligations
remain; NEG-dynamic-import changes disposition after identical-byte capture,
while seven new unique cases bring the full unique count to90. Historical evidence
is preserved. No public ABI, combined-profile or task acceptance is implied.


## Whitespace in a single expanded import path

[import-path-whitespace-v1/CONTRACT.md](import-path-whitespace-v1/CONTRACT.md)
qualifies FR-18-01 with four additional Default cases and a separately captured
BMP whitespace classifier. Only the selected path is trimmed with the native
whitespace definition; whitespace-only values fail before selecting a target and
properties retain their original padding. The original90 comparison outcomes
must remain unchanged; the extended full suite requires94 unique comparisons. Every v1
producer/corpus/evidence artifact stays intact. Acceptance and public ABI gates
remain open.
