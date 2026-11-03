# DJ-005 .j Build: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Tasks.UnitTests/Al_Tests.cs:34](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L34) | AlgorithmId | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:50](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L50) | BaseAddress | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:66](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L66) | CompanyName | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:82](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L82) | Configuration | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:98](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L98) | Copyright | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:114](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L114) | Culture | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:130](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L130) | DelaySign | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:146](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L146) | Description | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:162](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L162) | EmbedResourcesWithPrivateAccess | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:187](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L187) | EvidenceFile | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:203](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L203) | FileVersion | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:219](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L219) | Flags | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:235](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L235) | GenerateFullPaths | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:251](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L251) | KeyFile | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:267](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L267) | KeyContainer | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:283](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L283) | LinkResourcesWithPrivateAccessAndTargetFile | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:309](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L309) | LinkResourcesWithTwoItems | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:342](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L342) | MainEntryPoint | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:358](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L358) | OutputAssembly | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:374](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L374) | Platform | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:389](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L389) | PlatformAndPrefer32Bit | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:436](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L436) | ProductName | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:452](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L452) | ProductVersion | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:468](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L468) | ResponseFiles | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:485](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L485) | SourceModules | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:510](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L510) | TargetType | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:526](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L526) | TemplateFile | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:544](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L544) | Title | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:560](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L560) | Trademark | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:576](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L576) | Version | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:594](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L594) | Win32Icon | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:610](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L610) | Win32Resource | yes |
| [src/Tasks.UnitTests/Al_Tests.cs:628](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L628) | GenerateFullPathToTool_ReturnsAbsolutePathOrNull | not confirmed |
| [src/Tasks.UnitTests/Al_Tests.cs:653](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs#L653) | GetProcessStartInfo_UsesTaskEnvironmentWorkingDirectory | not confirmed |
| [src/Tasks.UnitTests/LC_Tests.cs:25](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/LC_Tests.cs#L25) | SimpleValidArgumentsCommandLine | not confirmed |
| [src/Tasks.UnitTests/LC_Tests.cs:51](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/LC_Tests.cs#L51) | GenerateFullPathToToolResolvesRelativeSdkToolsPath | yes |
| [src/Tasks.UnitTests/LC_Tests.cs:79](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/LC_Tests.cs#L79) | SimpleValidArgumentsResponseFile | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-005-F01-01 | WP-01 | Conditional imports and property expansion are deterministic | Bounded: 35 And/Or condition cases compared with a native MSBuild capture in Batch 2503. [Or conditions](../../../../dotj-build/evaluation-candidate/CONDITION-LOGIC-V2.md) |
| DJ-005-F01-02 | WP-01 | import cycles report chains | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F01-03 | WP-01 | glob behavior is tested for Windows/Linux case differences | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F01-04 | WP-01 | evaluator never executes tasks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F02-01 | WP-02 | Cycles show a reproducible path | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F02-02 | WP-02 | no target runs before prerequisites | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F02-03 | WP-02 | task failure prevents dependent work without cancelling unrelated work under continue mode | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F03-01 | WP-03 | Untrusted project tasks require explicit execution policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F03-02 | WP-03 | command arguments preserve quoting | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F03-03 | WP-03 | killed tasks cannot report success | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F03-04 | WP-03 | .NET assemblies are never loaded as Java tasks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F04-01 | WP-04 | Changing any declared input invalidates the correct targets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F04-02 | WP-04 | interrupted writes never create valid cache hits | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F04-03 | WP-04 | fresh and cached builds yield equivalent artifacts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F05-01 | WP-05 | Bootstrap javac build and self-hosted build agree on artifacts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F05-02 | WP-05 | cancellation closes child processes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-005-F05-03 | WP-05 | clean rebuild requires no private machine state | Designed; map actual upstream case or specify independent oracle in E03 |

## Candidate2521 item evaluation evidence

The [selected contract](../../../../dotj-build/evaluation-candidate/items-evaluation-v1/contract.json)
maps IP01-06, IO01-06, IM01-06, ID01-05, IC01-06, IG01-10 and IS01-03 to
source-derived cases and actual native observations. Forty-two definitions have
two native passes per OS,168 repeated rows total; four supplemental definitions
have16 repeated rows. This adapts selected upstream item/default/glob tests to
evaluation-only operation, not a claim that the upstream suite ran. Fourteen
private groups cover grammar, bounds, ownership, cache/site admission and real
Windows junction/Linux symlink and case-collision capabilities. See the
[qualification](evidence/private-items-evaluation-v1.json) for final-artifact
historical consumers and the sole `NEG-items` transition. No designed full task
or public compatibility case is accepted by this bounded private evidence.

## Differential runner design

The bounded private cycle-trace successor adds 19 byte-frozen import graphs across
three individual profiles, Windows and measured case-enabled Linux 9p/NTFS.
Its native projection evidence has two independent observations for every field
in all 114 graph/profile/platform rows (228 required row-passes, 190 new).
Full root-prefix traces are independently authored source adaptations, not a
native public Chain field. Fourteen private groups include deterministic
two-thread isolation, original compiled ABI consumers, 57 actual proof-negative
controls and physical relocation. The same immutable final JAR reruns all
inherited 303 Build obligations. See
[the private qualification](evidence/private-cycle-trace-v1.json) and
[the contract](../../../../dotj-build/evaluation-candidate/cycle-trace-v1/README.md).
This advances F01-02 only as a partial adaptation; public/task/framework acceptance
and the existing deferred families remain open.

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Property precedence; wildcard paths; target cycles; dependency invalidation; parallel task determinism; cancellation.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-005-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-005-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-005-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I02`: Independent JDK bootstrap and minimal launcher; five named tasks and five designed cases in the integration plan.
- `SDK-I03`: SDK-style project evaluation and solutions; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.

## SDK artifact replay, candidate Batch 2523

The six evaluator/module sources are unchanged, but the new45-class SDK JAR
was actually exercised through the retained cycle-trace selected/private, ABI,
and history harnesses. `tools/oracle/dotj-sdk/seed-v1/freeze_inherited.py` binds
114 trace rows, items42 per OS, private14/61, supplement4, raw sort and three
boundary families per OS, ordering308/M1, Boolean297/private16/control14, all14
history operations and stable94 sole NEG-items transition to that exact JAR.
The SDK pure reader requires matching operation/output inventories before those
semantic comparisons. Historical JAR qualification is preserved as lineage and
native-reference evidence; old class-byte equality is additional provenance.
