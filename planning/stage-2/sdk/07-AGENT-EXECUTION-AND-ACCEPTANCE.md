# AI agent execution plan and acceptance gates

Parent: [SDK plan](../10-SDK-AND-DISTRIBUTION-PLAN.md). This adds **12 integration work packages, 60 named implementation tasks and 60 designed acceptance cases**. They connect existing repository features; they are not claims that any feature or test already works. Machine-readable entries are in [sdk-integration-plan.json](../evidence/sdk-integration-plan.json) and the main task/acceptance backlogs.

## Execution rules

Start with SDK-I01 contract evidence and the existing first core foundation slice. Implement one usable vertical slice at a time. Do not wait for all 66 repositories, a complete public registry or all optional workloads before proving console/library/local-feed development. Existing E01-E03, N01 and Q01 gates still apply to each consumed slice. Qualified partial capability profiles can progress while unrelated capabilities remain blocked.

For every task: identify exact inputs and prerequisite status; implement owned code; add meaningful command/API/integration tests; retain raw results; update the capability ledger; and report the artifact/commit and remaining blockers. Do not mark an acceptance case passed without executing it. Complete source mapping before choosing public declarations. Keep task status and feature status separate.

The acceptance environment must capture the pinned .NET oracle, JDK/.j builds, OS/architecture, locale, source fixtures, environment/configuration, exact invocation, stdout/stderr/exit, filesystem delta and network observations. Only explicit product/platform representation differences may be normalized. A stub, mock feed or synthetic success response cannot qualify the end-to-end release path.

## Milestones and delivery order

| Milestone | Required result | Integration packages |
|---|---|---|
| M0 | Qualified baseline and independent bootstrap | I01-I02 plus core prerequisites |
| M1 | Console/library/solution projects using local packages | I03-I06 |
| M2 | Offline SDK installation and real runtime publication | I07-I08 |
| M3 | Optional tools/workloads and qualified remote feed | I09-I10 |
| M4 | Portable release pipeline and all-product disposition | I11-I12 |

Dependencies below refer to consumed contracts/results, not automatic whole-product completion. For example, a registry integration needs a qualified package profile; it does not require every NuGet client UI to exist. Optional capability owners qualify their own products before SDK integration claims them.

## Required outputs for every integration package

- A source-derived contract and mapping ledger, implementation commit(s) and explicit prerequisite record.
- Relevant executable tests and raw reference/.j results, with negative and interruption cases below.
- Public command/API diff, dependency/provenance updates and any platform representation decisions.
- A working sample and operational instructions appropriate to the capability.
- Updated task/acceptance status, known limitations and rollback behavior for persisted/install/distribution state.

## SDK-I01: Reference baseline and exact compatibility contracts

**Accountable owner:** `dotj-sdk`. **Prerequisites:** E01 baseline qualification and relevant core contract research. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [01-CLI-PARITY.md](01-CLI-PARITY.md), [08-REFERENCE-AND-DECISION-LEDGER.md](08-REFERENCE-AND-DECISION-LEDGER.md).

### Named tasks

- `SDK-I01-T1`: Lock the concrete .NET 10 SDK artifact, matching source revision, OS images and invocation environment; reconcile the older analysis pins without overwriting them.
- `SDK-I01-T2`: Extract every CLI token, option, alias, default and source test identity into a versioned command contract ledger; mark unimplemented commands explicitly.
- `SDK-I01-T3`: Map SDK project/configuration names and framework public identities to the N01 ledger; separate source-verified identities from internal helper vocabulary.
- `SDK-I01-T4`: Qualify the proposed project extension, target moniker, package envelope, cache roots and mixed-product coexistence rules; record any remaining language/runtime conflicts.
- `SDK-I01-T5`: Capture raw reference results for positive and negative command fixtures, define an auditable normalization allowlist and publish the baseline lock with hashes.

### Designed acceptance cases

- `SDK-I01-F01`: A command contract points to a concrete reference SDK/source and reproducible raw oracle result; no latest-only identity is accepted.
- `SDK-I01-F02`: Noun-first and retained legacy package/reference forms have separately tested parsing and equivalent reference edits where upstream supports both.
- `SDK-I01-F03`: Unsupported options fail without project/cache/install mutations; help and version commands work without a feed.
- `SDK-I01-F04`: A generic-arity, illegal-identifier or runtime gap remains blocked instead of passing after a silent public rename.
- `SDK-I01-F05`: Changing the reference patch invalidates affected contract evidence and produces a reviewed compatibility diff.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I02: Independent JDK bootstrap and minimal launcher

**Accountable owner:** `dotj-build`. **Prerequisites:** SDK-I01. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [03-INSTALLATION-AND-RESOLUTION.md](03-INSTALLATION-AND-RESOLUTION.md).

### Named tasks

- `SDK-I02-T1`: Pin an eligible JDK vendor/build and minimal core slice; record archive hashes, platform prerequisites and redistribution evidence for each proposed platform.
- `SDK-I02-T2`: Create the JDK-only seed build using javac/jar and owned foundation code, without an installed dotj SDK, Maven, Gradle or replacement framework.
- `SDK-I02-T3`: Build a minimal launcher that discovers its own root, selects the qualified toolchain and reports actual product versions and architecture.
- `SDK-I02-T4`: Implement internal process execution with argument arrays, cancellation, environment scoping and diagnostic redaction; keep helper APIs internal.
- `SDK-I02-T5`: Build the first SDK from the seed, rebuild it using the resulting SDK and retain reproducibility evidence and bootstrap recovery instructions.

### Designed acceptance cases

- `SDK-I02-F01`: A clean environment with only the locked JDK and source can build the seed and first SDK without a circular dependency.
- `SDK-I02-F02`: Paths containing spaces and Unicode reach javac and child applications unchanged on each advertised OS.
- `SDK-I02-F03`: Missing or incompatible JDK fails before producing a success marker or incomplete installation.
- `SDK-I02-F04`: Cancellation terminates owned children and leaves reusable previous outputs intact.
- `SDK-I02-F05`: The seed-built and SDK-rebuilt outputs satisfy the declared reproducibility comparison with all nondeterministic inputs explained.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I03: SDK-style project evaluation and solutions

**Accountable owner:** `dotj-build`. **Prerequisites:** SDK-I02. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [02-PROJECT-AND-BUILD-CONTRACT.md](02-PROJECT-AND-BUILD-CONTRACT.md).

### Named tasks

- `SDK-I03-T1`: Implement the qualified XML property/item/import/condition evaluation slice with source-derived ordering and exact public names; diagnose unsupported tasks at their import origin.
- `SDK-I03-T2`: Define Dotj.Sdk defaults, Java compilation/resource targets, target/configuration output paths and explicit unsupported-property diagnostics.
- `SDK-I03-T3`: Implement ProjectReference graph evaluation and qualified solution read/edit support while preserving unrelated entries and detecting dependency/import cycles.
- `SDK-I03-T4`: Implement incremental input identity, output ownership, parallel build isolation and Clean/Rebuild behavior for the selected profiles.
- `SDK-I03-T5`: Add property/item/target evaluation and project mutation differential fixtures, including central versions, conditional references, alternate paths and mixed solution contents.

### Designed acceptance cases

- `SDK-I03-F01`: Equivalent conditional project inputs select the same conceptual references and target order as the locked reference fixture.
- `SDK-I03-F02`: Directory.Build props/targets and command-line property overrides follow the qualified precedence with no hidden second evaluator.
- `SDK-I03-F03`: Editing a solution preserves unrelated projects/comments and reports unsupported project types explicitly.
- `SDK-I03-F04`: A compiler, package, generated-source or target change invalidates the affected cache, while a no-change build reuses verified outputs.
- `SDK-I03-F05`: Clean and cancellation cannot delete source files or another configuration/project output tree.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I04: Working console and library templates

**Accountable owner:** `dotj-templates`. **Prerequisites:** SDK-I03. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [06-TEMPLATES-TOOLS-WORKLOADS.md](06-TEMPLATES-TOOLS-WORKLOADS.md).

### Named tasks

- `SDK-I04-T1`: Port the required template discovery/schema/parameter behavior with exact template short names and source-qualified option spellings.
- `SDK-I04-T2`: Create minimal console, classlib, solution, globaljson and nugetconfig templates using only qualified APIs and explicit Java-profile artifact representations.
- `SDK-I04-T3`: Implement template installation/version tracking and output transformations with archive/path validation and transactional owned-file writes.
- `SDK-I04-T4`: Implement dry-run, overwrite and post-action behavior using the locked reference contracts and documented unattended execution rules.
- `SDK-I04-T5`: Create paired C#/.j sample projects and run each advertised template through create, restore, build and its appropriate run/test path.

### Designed acceptance cases

- `SDK-I04-F01`: Console and classlib templates create compilable projects with exact framework API names and no Maven/Gradle requirement.
- `SDK-I04-F02`: Dry-run leaves the filesystem unchanged while identifying intended outputs and conflicts.
- `SDK-I04-F03`: A template archive or transform attempting to escape its output root is rejected before writes.
- `SDK-I04-F04`: A requested C# language option cannot silently generate Java and claim equivalent language support.
- `SDK-I04-F05`: Repeated installation/uninstallation preserves user files and removes only template-owned state.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I05: Java package profile and deterministic restore

**Accountable owner:** `dotj-packages`. **Prerequisites:** SDK-I03. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [04-PACKAGES-AND-FEEDS.md](04-PACKAGES-AND-FEEDS.md).

### Named tasks

- `SDK-I05-T1`: Freeze the versioned nupkg/nuspec plus explicit Java manifest/payload profile; qualify custom package types, source-derived package IDs and target compatibility rules.
- `SDK-I05-T2`: Implement NuGet-compatible version/dependency resolution, conditional PackageReference and central package versions with exact public API naming and oracle fixtures.
- `SDK-I05-T3`: Implement local feeds and qualified V3 discovery/content acquisition, source mapping, credential scoping and Java-runtime-kind rejection of incompatible packages.
- `SDK-I05-T4`: Implement lock/assets representations, isolated immutable caches, content verification, atomic extraction and concurrent/offline restore behavior.
- `SDK-I05-T5`: Implement package/reference CLI edits, pack manifests and qualified push/signature operations with explicit capability errors for unimplemented formats.

### Designed acceptance cases

- `SDK-I05-F01`: A local Java-profile package restores and builds; a same-ID CLR-only package is rejected before compilation.
- `SDK-I05-F02`: Locked restore reproduces the graph and content hashes; changed dependency metadata or payload bytes fail without silently rewriting the lock.
- `SDK-I05-F03`: Package source mapping prevents unintended source selection, including an inherited public CLR feed.
- `SDK-I05-F04`: Interrupted or concurrent downloads never expose partial cache entries; corrupt/path-traversal packages are rejected.
- `SDK-I05-F05`: A complete local package closure restores offline, while a missing transitive package produces a named deterministic failure.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I06: End-to-end CLI orchestration and real test runners

**Accountable owner:** `dotj-sdk`. **Prerequisites:** SDK-I04, SDK-I05. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [01-CLI-PARITY.md](01-CLI-PARITY.md), [06-TEMPLATES-TOOLS-WORKLOADS.md](06-TEMPLATES-TOOLS-WORKLOADS.md).

### Named tasks

- `SDK-I06-T1`: Connect command parsing to actual project/build/package/template services with reference-qualified implicit restore/build and configuration selection.
- `SDK-I06-T2`: Implement run and exec with Java payload validation, argument delimiter forwarding, exit propagation and owned process cleanup.
- `SDK-I06-T3`: Integrate a real qualified dotj-xtest or dotj-test adapter and explicitly pin the reference VSTest or Microsoft.Testing.Platform mode.
- `SDK-I06-T4`: Implement command diagnostics, help, failure categories and any qualified machine output schemas; reject unsupported commands without false success.
- `SDK-I06-T5`: Run the multi-project example from creation through package addition, locked restore, build, run and tests, retaining both reference and Java-profile results.

### Designed acceptance cases

- `SDK-I06-F01`: New, restore, build and run complete a working two-project application with source-verified framework APIs.
- `SDK-I06-F02`: No-restore/no-build behavior matches the selected command contract and cannot silently fetch or compile missing inputs.
- `SDK-I06-F03`: A real failing test causes the expected nonzero result and report; a crashed runner cannot be counted as passing.
- `SDK-I06-F04`: Application arguments and exit status survive launcher forwarding, including spaces and Unicode.
- `SDK-I06-F05`: A reference/JVM differential check rejects an altered default, missing warning or wrong exit code instead of normalizing it away.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I07: SDK bundles, global.json and installation transactions

**Accountable owner:** `dotj-sdk`. **Prerequisites:** SDK-I06. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [03-INSTALLATION-AND-RESOLUTION.md](03-INSTALLATION-AND-RESOLUTION.md).

### Named tasks

- `SDK-I07-T1`: Assemble full SDK, existing-JDK SDK and runtime bundle layouts with explicit component versions, reference/runtime packs, notices and integrity manifests.
- `SDK-I07-T2`: Implement global.json discovery and every supported SDK version/preview/roll-forward policy from the locked reference with product-specific installed versions.
- `SDK-I07-T3`: Implement staged per-user installation, architecture selection, checksums/publisher verification, atomic activation and version ownership records.
- `SDK-I07-T4`: Add system-install integration, PATH/shim handling, repair/uninstall and shared-pack retention per qualified operating system.
- `SDK-I07-T5`: Create an offline closure bundle and install it on clean target environments with network disabled; retain startup and console build evidence.

### Designed acceptance cases

- `SDK-I07-F01`: Side-by-side SDKs select the expected version for each qualified global.json case without altering DOTNET_ROOT or unrelated JAVA_HOME.
- `SDK-I07-F02`: A missing exact SDK with roll-forward disabled fails locally and does not silently download a replacement.
- `SDK-I07-F03`: Interrupted/corrupt installation leaves the previous version runnable and no staged version advertised as installed.
- `SDK-I07-F04`: Uninstalling one SDK preserves another SDK and packs still referenced by it.
- `SDK-I07-F05`: An offline full bundle installs, creates, restores locally, builds and runs its declared sample without network access.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I08: Publish profiles and deployable runtime outputs

**Accountable owner:** `dotj-sdk`. **Prerequisites:** SDK-I06, SDK-I07. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [05-PUBLISH-AND-HOSTING.md](05-PUBLISH-AND-HOSTING.md).

The SDK-I10 dependency for a preview release is qualification of the selected distribution endpoint and its actual operations. A qualified external feed can satisfy that slice; finishing the entire owned registry is not required before releasing a preview SDK. Owned registry implementation remains retained scope.

### Named tasks

- `SDK-I08-T1`: Implement source-qualified publish configuration/runtime/self-contained options and the versioned Java dependency/runtime metadata mapping.
- `SDK-I08-T2`: Build framework-dependent outputs and runtime selection/startup contracts with clear missing-runtime and incompatibility diagnostics.
- `SDK-I08-T3`: Build self-contained output using a qualified runtime image and declared native/resource closure; separate platform-specific artifacts.
- `SDK-I08-T4`: Integrate container/workload publication only after each backend passes its own feasibility and ownership gates; reject unsupported single-file/AOT requests explicitly.
- `SDK-I08-T5`: Run clean-machine deployment fixtures covering entry point, arguments, exit status, signals, runtime absence, missing assets and output integrity.

### Designed acceptance cases

- `SDK-I08-F01`: Framework-dependent output runs with an eligible runtime and clearly fails when that runtime is absent or incompatible.
- `SDK-I08-F02`: Self-contained output runs on the qualified clean OS/architecture without a preinstalled JDK or dotj SDK.
- `SDK-I08-F03`: Local publish creates complete local outputs and performs no unrequested remote deployment or upload.
- `SDK-I08-F04`: A missing native asset or incompatible runtime identifier fails before publication is declared successful.
- `SDK-I08-F05`: A JAR, jlink image or restart loop cannot satisfy a NativeAOT, single-file or hot-reload parity test without its actual required behavior.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I09: Tool, workload and IDE integration

**Accountable owner:** `dotj-sdk`. **Prerequisites:** SDK-I05, SDK-I07. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [06-TEMPLATES-TOOLS-WORKLOADS.md](06-TEMPLATES-TOOLS-WORKLOADS.md).

### Named tasks

- `SDK-I09-T1`: Implement qualified local/global/tool-path tool management with exact CLI options, familiar manifest discovery and explicit Java package runtime validation.
- `SDK-I09-T2`: Implement tool shims and execution isolation with version tracking, argument/exit forwarding and owned-file uninstall behavior.
- `SDK-I09-T3`: Implement workload manifest/pack closure, SDK band selection and transactional install/update/repair/uninstall with shared-pack ownership.
- `SDK-I09-T4`: Integrate qualified platform/test/web templates and developer tools without making optional workloads mandatory for console development.
- `SDK-I09-T5`: Provide thin IDE service contracts using the same SDK resolution/build/test logic, with honest Java language/debugger capabilities and a qualified integration matrix.

### Designed acceptance cases

- `SDK-I09-F01`: Local tool restore/run follows the checked-in manifest and cannot overwrite an unrelated CLR/global tool installation.
- `SDK-I09-F02`: A tool command collision fails or follows the locked reference behavior without silently hijacking another executable.
- `SDK-I09-F03`: Failed workload update preserves the previous usable workload, and shared packs survive removal while still referenced.
- `SDK-I09-F04`: An incompatible platform or missing required external tool is reported before a workload is marked installed.
- `SDK-I09-F05`: IDE and terminal builds select the same SDK, project configuration and dependencies for the same fixture.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I10: Hosted feed protocol and immutable distribution

**Accountable owner:** `dotj-registry`. **Prerequisites:** SDK-I05. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [04-PACKAGES-AND-FEEDS.md](04-PACKAGES-AND-FEEDS.md), [05-PUBLISH-AND-HOSTING.md](05-PUBLISH-AND-HOSTING.md).

### Named tasks

- `SDK-I10-T1`: Implement/qualify the selected V3 service index, registration/content/search and publish/delete resource contracts using actual request/response fixtures.
- `SDK-I10-T2`: Implement atomic immutable package storage and metadata indexing, duplicate identity checks, authorization and scoped publisher ownership.
- `SDK-I10-T3`: Provide local-to-private-to-public deployment profiles and stable download/release metadata, with explicit provider capabilities and no hard-coded invented endpoints.
- `SDK-I10-T4`: Define backups, isolated recovery, quotas, retention, monitoring and secret-redacted audit records; choose recovery objectives during deployment qualification.
- `SDK-I10-T5`: Run restore/push/search/authentication/recovery tests against both the qualified reference profile and the owned feed using real Java-profile packages.

### Designed acceptance cases

- `SDK-I10-F01`: The client discovers resource URLs from the service index and restores the Java-profile package using the qualified protocol.
- `SDK-I10-F02`: Same-ID/version publication with different bytes is rejected and cannot make a partially uploaded artifact visible.
- `SDK-I10-F03`: Expired credentials, throttling and service failure produce bounded retry/error behavior with no secrets in logs.
- `SDK-I10-F04`: Restoring a backup yields metadata whose content hashes and downloadable artifacts all agree.
- `SDK-I10-F05`: Package downloads already published remain recoverable when search or nonessential portal components are unavailable.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I11: Portable CI, signing and release distribution

**Accountable owner:** `dotj-sdk`. **Prerequisites:** SDK-I07, SDK-I08, SDK-I10. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [05-PUBLISH-AND-HOSTING.md](05-PUBLISH-AND-HOSTING.md).

The SDK-I10 dependency for a preview release is qualification of the selected distribution endpoint and its actual operations. A qualified external feed can satisfy that slice; finishing the entire owned registry is not required before releasing a preview SDK. Owned registry implementation remains retained scope.

### Named tasks

- `SDK-I11-T1`: Provide repository-owned build/release entry points used by thin Azure Pipelines now and qualified GitHub Actions later, with pinned toolchains and explicit cache keys.
- `SDK-I11-T2`: Build the supported OS/architecture matrix and generate version/provenance/compatibility manifests, SBOMs, notices and immutable artifact hashes.
- `SDK-I11-T3`: Integrate eligible signing and staging verification, separating build, package push, release promotion and actual deployment authorization.
- `SDK-I11-T4`: Document source/CI migration, feed/download continuity, secret re-provisioning and rollback; prove a fixed commit builds equivalently on both providers.
- `SDK-I11-T5`: Stage a preview release with install/restore/run smoke evidence and retention/recovery instructions; keep public promotion disabled until authorized.

### Designed acceptance cases

- `SDK-I11-F01`: Equivalent source/toolchain inputs run through provider-independent build steps and satisfy the declared artifact reproducibility check.
- `SDK-I11-F02`: Artifacts lacking a required notice, signature, manifest or platform acceptance result cannot be promoted.
- `SDK-I11-F03`: A Git import alone is never reported as migrating pipeline secrets, work items or branch protections.
- `SDK-I11-F04`: Changing source host does not silently break existing immutable package/download references.
- `SDK-I11-F05`: Failed promotion leaves the previous channel usable and does not overwrite a previously released package version.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## SDK-I12: All-product SDK qualification and agent handoff

**Accountable owner:** `dotj-sdk`. **Prerequisites:** SDK-I06, SDK-I08, SDK-I09, SDK-I11. All consumed repository slices also require E01-E03 and N01.

**Specifications:** [07-AGENT-EXECUTION-AND-ACCEPTANCE.md](07-AGENT-EXECUTION-AND-ACCEPTANCE.md), [08-REFERENCE-AND-DECISION-LEDGER.md](08-REFERENCE-AND-DECISION-LEDGER.md).

### Named tasks

- `SDK-I12-T1`: Create distribution contribution records for all 66 repos covering exact API identities, package/version/type, targets, dependencies, notices and SDK compatibility.
- `SDK-I12-T2`: Map every product to core/reference/runtime packs, optional packages, templates/tools or workloads without forcing all products into the base SDK.
- `SDK-I12-T3`: Run the final command/API/behavior/package/install/publish matrix and retain explicit blocked/deferred capability ownership and evidence.
- `SDK-I12-T4`: Produce executable paired C#/.j onboarding examples and a concise syntax/runtime differences table; verify no substitute Java framework vocabulary leaked into the public workflow.
- `SDK-I12-T5`: Publish the implementation handoff report, achieved compatibility profile, open gates and next eligible slices; archive all acceptance evidence with the release candidate.

### Designed acceptance cases

- `SDK-I12-F01`: All 66 products have a distribution disposition and owner, including products not yet implemented.
- `SDK-I12-F02`: Every advertised public API preserves its source-verified name/case and every claimed command behavior has named passing evidence.
- `SDK-I12-F03`: A new developer completes the qualified create/add/build/test/publish path without Maven, Gradle or a new framework vocabulary.
- `SDK-I12-F04`: Unimplemented mobile/browser/AOT or language gaps remain visible and cannot be hidden behind a blanket exact-parity claim.
- `SDK-I12-F05`: The final report distinguishes written requirements, executed tests, implemented capabilities and release authorization status.

**Completion gate:** the corresponding cases pass on the supported matrix, source-derived naming/command checks pass, outputs are reviewable and unresolved capabilities remain explicitly blocked. Rollback must preserve the last verified usable state where this package changes installed or published state.

## Final review and reporting format

The implementation report names the achieved profile and reference versions; lists exact delivered commands/APIs/platforms; links raw evidence; states failed/blocked/deferred capabilities with owners; and identifies the next eligible slice. Separately report package/SDK publication and deployment status. A completed planning task, a successful local build and an authorized public release are different facts.

For the initial milestone, the required demonstration is concrete: create a solution, class library and console app; add a project and Java-profile package reference; restore from a local feed; build; run and observe expected output; run real passing and failing test fixtures once the test slice is available; pack; install from a clean SDK archive; then publish and run the qualified deployment output. Record each capability as it becomes available rather than claiming the full sequence before all its prerequisites exist.
