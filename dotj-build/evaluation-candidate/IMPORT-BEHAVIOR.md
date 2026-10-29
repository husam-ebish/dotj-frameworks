# Explicit relative import behavior v1

This extends only the non-exported internal candidate. It supplies bounded
Windows evidence for DJ-005-WP-01-T1 / F01-01 and observations relevant to F01-02.
No work package, public API, release, platform, cycle-chain or product acceptance
is claimed. E01-E03/N01/NF01-NF03 and shared public core representation remain open.

## Immutable reference and profiles

The component remains `dotnet/msbuild@b44cdcec4c79c50c67560876707d57d4f635fa3b`,
SDK 10.0.401 / MSBuild 18.9.11 / runtime 10.0.12, roll-forward disabled.
[import-lock-v1.json](evidence/import-lock-v1.json) binds source, installed host,
runtime files, SDK assemblies/deps, compiler and net10.0 reference assemblies.
The owned probe compiles directly with the pinned local Roslyn compiler: no
project build, restore, package sources, tasks or network. The new probe's TFM is
net10.0, default SDK language version, nullable enabled; no existing project's
TFM, language, nullable, analyzer, SDK or runtime constraint changes.

Each case uses a new ProjectCollection, Local toolsets, explicit pinned
MSBUILD_EXE_PATH, synchronous logging and a private root-element cache. `None`
toolsets failed during host setup because the legacy framework path was absent;
the two failed attempts and their raw logs remain in the task report. They are
not import results. Local toolset discovery uses the SDK directory, without a
fixture SDK attribute or resolver. Only controlled SDK-free project XML is read.
The probe has no Build(), target scheduling or task-execution call.

The [plan](evidence/import-plan-v1.json) predates native execution. Its IDs are
designed fixtures, not upstream test IDs. Actual pinned source anchors include:

| Source file relative to component `src` | Inspected declarations/behavior |
|---|---|
| Build/Definition/Project.cs:436,693,698,1153,2279 | Filename constructor with load flags; Imports; ImportsIncludingDuplicates and its required flag; GetPropertyValue |
| Build/Definition/ProjectCollection.cs:314,630,1488,1582 | Explicit synchronous/cache constructor; Count; UnloadAllProjects; Dispose |
| Build/Definition/ResolvedImport.cs | ImportingElement, ImportedProject; location comes from the importing XML element |
| Framework/ILogger.cs; IEventSource.cs; BuildWarningEventArgs.cs; BuildErrorEventArgs.cs | Typed logger, warning/error events and actual code/file/line/column/message getters |
| Build/Errors/InvalidProjectFileException.cs | Typed failure code/file/line/column/message; inherited HResult |
| Build/Evaluation/Evaluator.cs:2146-2230 | Self-import branch; load-flag cycle branch; previous-import warning and duplicate skip |
| Build/Definition/ToolsetReader.cs; ToolsetLocalReader.cs; Framework/BuildEnvironmentHelper.cs | Missing legacy fallback and explicit local toolset setup |
| Build.UnitTests/Evaluation/Evaluator_Tests.cs:839,1003,1063 | ImportsOnlyIncludedOnce; RecordDuplicateButNotCircularImportsWithCircularImports; RejectCircularImportsWithCircularImports |

Source tests are navigation evidence; their Build-using upstream harness was not
run or claimed ported. Direct compilation of the typed probe independently binds
the consumed API signatures to the actual installed assemblies.

## Native matrix and candidate disposition

[All native observations](evidence/native-import-observations-v1.json) retain
27 ordered results per run. Two runs match with only the planned fixture-root
substitution in owner/project/file/message fields. Runtime/assembly paths are
retained. Property values, diagnostic codes (including null), source positions,
messages, import order, failure fields and cleanup fields are not discarded.
Raw stdout, stderr, host traces, commands, producer/assembly/runtime/input hashes
remain at the immutable paths bound by the observation lock.

| Designed input | Default native observation | Other native profiles | Candidate |
|---|---|---|---|
| BI01 direct repeat | P=root;one;between; one unique import; MSB4011 | Recording list contains both occurrences | Supported once-only, private notice |
| BI02 diamond | P=root;left;shared;right; left/shared/right order; MSB4011 from right | Recording list appends repeated shared import | Supported once-only, private notice |
| BI03 two-file root cycle | P=root;one; MSB4210 at one.props | Both explicit flags still warn/ignore root re-import | Refuses IMPORT_CYCLE_UNQUALIFIED |
| BI04 relative aliases | P=root;one; two MSB4011 warnings | Recording list contains all three normalized occurrences | Supported once-only, two ordered notices |
| BI05 false then true | P=root;one; one import; no warnings | Same properties/order, one recorded import | Supported; skipped occurrence does not mark seen |
| BI06 exact old duplicate input | Empty P/Q; one import; MSB4011 | Two recorded occurrences | Prior refusal now supported with same bytes |
| BI07 exact old cycle input | Empty P/Q; MSB4210 | Root re-import still warn/ignore | Same old candidate refusal retained |
| BI08 non-root cycle | P=root;one;two; MSB4011 at two.props | Recording profile: warning code null, cycle edge omitted. Reject profile: warning and error codes null, InvalidProjectFileException with null ErrorCode | Refuses IMPORT_CYCLE_UNQUALIFIED |
| BI09 true missing import | InvalidProjectFileException / MSB4019; no completed project | Same failure across profiles | Existing private code/owner/missing-path failure |

`ImportsIncludingDuplicates` throws InvalidOperationException without
RecordDuplicateButNotCircularImports, including under RejectCircularImports.
The candidate adds no load-settings or ImportsIncludingDuplicates API.
The default cycle warning/ignore policy and flagged pair diagnostics do not
establish F01-02's requested full cycle chain behavior.

## Per-observable comparison contract

| Observable | Native retained evidence | Actual Java comparison/disposition |
|---|---|---|
| P and Q | Exact captured values per profile | Exact values for five supported inputs; no value normalization |
| Unique import order | Ordered Imports owner/target plus source location | Exact ordered resolved files, with root prepended for candidate evaluatedFiles; native owner/location retained but no equivalent public API claimed |
| Duplicate warning code | Ordered warning/error events, null codes retained | MSB4011 only for acyclic repeat cases; exact private notice code/order match |
| Current owner and target paths | Current warning owner plus recording-profile duplicate owner/target records | Exact resolved owner/target order in private notices |
| Previous import paths/context | Original warning messages retain prior importing location/path and parent context | Unqualified; private notices do not expose prior-owner/path context |
| Source locations | Native line and column retained for every warning/error/failure | Unqualified; DOM candidate has no native line/column diagnostics |
| Messages | Entire native text with fixture-root-only substitution; raw text also retained | Unqualified; no text or public warning ABI equivalence |
| Cycles and flagged behavior | All three profiles, root/non-root distinctions, null codes and exception fields retained | Explicit refusal; no native cycle exception, warning or chain compatibility claim |
| Missing failure | Code, source owner/location, native message, type, HResult | Code/owner/missing path compare only; type/text/line/HResult ABI remains unqualified |
| Cleanup | Every native case starts Count=0; successful loads Count=1, failed loads Count=0; UnloadAllProjects returns Count=0 and Dispose completes | Per-call evaluation and immutable result/notice snapshots verified; no ProjectCollection/unload/disposal equivalence claim |
| Task execution | All native/candidate markers absent, immutable fixture hashes verified | Matched no-marker observation; evaluator remains an inert evaluation implementation |

[The comparison bridge](evidence/native-import-comparison-v1.tsv) is mechanically
reconstructed from the native observations before Java launches; its values are
not generated from candidate output. Fixture-relative paths are bridge transport
representations, compared as resolved paths. Cycles have explicit gap rows, not
success rows. The verifier retains every original case ID and checks all 23 old
refusal payload hashes against the original source-derived manifest. The original
20 native inputs and unrelated refusal payloads remain byte-for-byte unchanged.
The BE19 single fixture-root substitution remains exactly the original approval.

The full suite is 52 cases: original 20 native comparisons, 22 unchanged refusal
inputs, the original duplicate input now paired to native support, and nine new
matrix comparisons/dispositions. The duplicate and cycle predecessor payloads
also have independently hashed native fixtures. This is accounting, not added
acceptance credit. Runtime dependencies remain JDK java.base and java.xml only;
.NET/Roslyn/reference packs and Python are development-only tools.

Next concrete work: specify a bounded cycle-chain/diagnostic contract against the
observed distinct load profiles, resolve source location/previous-import/message
representation, and separately close public lifecycle/core/eligibility gates.
Item/glob/SDK/Unicode/environment/Windows-Linux and complete public ABI work remain
unqualified. No public Project, ProjectCollection or diagnostic facade is added.
