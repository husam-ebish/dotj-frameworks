# SDK, packages and distribution: binding implementation plan

Revision: 2026-10-19. Requirement ID: `DOTNET-SDK-EXPERIENCE-001`. Status: detailed written specification; implementation NOT STARTED. This supplements all 66 repository plans and is mandatory for every product delivered through the SDK.

## Owner requirement

The owner wants Java frameworks to feel familiar to C#/.NET developers, with the exact same public names, casing, concepts and corresponding developer workflows. Apply [DOTNET-API-EXACT-001](08-DOTNET-API-COMPATIBILITY-POLICY.md) to classes, interfaces, methods, properties, events, namespaces and lifecycle behavior. Do not substitute Java-style names, a Maven/Gradle workflow, a new configuration vocabulary or a new dependency-injection model. Internal JDK machinery must remain behind the familiar surface.

For SDK commands, preserve the .NET command words, option spellings, argument roles, project concepts and observable behavior in the selected reference profile. The product executable is `dotj`; examples replace the `dotnet` launcher with `dotj`. Do not claim Microsoft affiliation or that this is part of the official .NET SDK or JDK.

Exact compatibility is a requirement to verify, not a result already achieved. A Java library cannot by itself make the Java compiler accept all C# syntax, execute CLR assemblies or reproduce every CLR behavior. Keep such gaps visible in the compatibility ledger. A blocked capability stays blocked; a different implementation cannot pass by relabeling it as exact parity. The objective is no new framework vocabulary, with unavoidable language/runtime differences isolated and explained.

## What is being added

| Specification | Implementation agent must use it for |
|---|---|
| [01-CLI-PARITY.md](sdk/01-CLI-PARITY.md) | Command families, parsing, help, exit behavior and familiar everyday workflows |
| [02-PROJECT-AND-BUILD-CONTRACT.md](sdk/02-PROJECT-AND-BUILD-CONTRACT.md) | SDK-style projects, solutions, properties, references and build behavior |
| [03-INSTALLATION-AND-RESOLUTION.md](sdk/03-INSTALLATION-AND-RESOLUTION.md) | SDK distribution, JDK bootstrap, global.json, side-by-side versions and offline installation |
| [04-PACKAGES-AND-FEEDS.md](sdk/04-PACKAGES-AND-FEEDS.md) | PackageReference, NuGet concepts, Java payload profile, restore and feed protocols |
| [05-PUBLISH-AND-HOSTING.md](sdk/05-PUBLISH-AND-HOSTING.md) | Application deployment, release hosting, Azure DevOps/GitHub and operations |
| [06-TEMPLATES-TOOLS-WORKLOADS.md](sdk/06-TEMPLATES-TOOLS-WORKLOADS.md) | Templates, project scaffolding, tools, optional platform packs and IDE integration |
| [07-AGENT-EXECUTION-AND-ACCEPTANCE.md](sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) | Ordered integration packages, named tasks, failure cases and acceptance gates |
| [08-REFERENCE-AND-DECISION-LEDGER.md](sdk/08-REFERENCE-AND-DECISION-LEDGER.md) | Official references, version baseline and explicit platform differences |
| [66-product distribution ledger](evidence/sdk-product-contributions.json) | Per-product packaging and SDK contribution gates |
| [SDK integration backlog](evidence/sdk-integration-plan.json) | Machine-readable owners, dependencies, tasks and acceptance cases |

## Hosting and product decisions

1. The framework libraries execute inside consuming applications. Development and local use do not require a hosted framework service.
2. A source repository stores code and planning. A package feed distributes versioned dependencies. A download endpoint distributes SDK/runtime installers and archives. An application host runs a user's application. These are separate responsibilities.
3. Begin with local packages and local archives. Add a private compatible package feed when a team needs shared consumption; add a public feed and download endpoint for public releases. Do not block foundation implementation on building a public registry.
4. Ship an independently installable `.j SDK` containing the launcher, build/restore/template tooling, reference packs and a qualified Java toolchain or an explicit existing-JDK variant. A smaller `.j Runtime` distribution is a separate deliverable.
5. Consumers use `dotj new`, `restore`, `build`, `run`, `test`, `pack` and `publish`; they do not have to install Maven or Gradle or learn their project files.
6. Additional libraries are restored as packages. Larger platform tooling is installed as workloads. Tools and templates have the corresponding .NET-style management commands. Do not put all 66 repositories into every application or installation.

## Scope, profiles and readiness

The initial command reference family is .NET 10. Before implementation, E01 must select a concrete SDK patch, artifact checksum, matching CLI source revision and executable oracle. This proposal does not silently replace the existing SDK analysis pin. Reconcile the release with [PINNED-UPSTREAM](repos/dotj-sdk/PINNED-UPSTREAM.md), retaining both identities. Future reference updates require a compatibility diff.

The first runnable milestone is a console application and class library, with local feed restore and a clean offline rebuild. Later milestones add packaged test runners, web tooling, tools, workloads, installers and hosted feeds. The entire scope remains in this plan; milestones sequence the work and do not authorize permanent omission of corresponding .NET features.

All 66 repositories must identify their package identity, dependency closure, SDK/reference pack membership, supported targets, sample/template requirements and distribution license evidence before their release. UI, browser, native/mobile and AOT capabilities retain platform feasibility gates. Never expose a working-looking command which returns success without performing its advertised operation.

## Ownership and precedence

`dotj-sdk` owns orchestration and the public command surface; `dotj-build` owns project evaluation and targets; `dotj-packages` owns package semantics; `dotj-registry` owns hosted feed behavior; `dotj-templates` and `dotj-scaffold` own generation; `dotj-core` owns the foundation/runtime facade. `dotj-code`, test products, diagnostics, containers and workload products supply their respective adapters.

This specification replaces vague earlier SDK/distribution proposals where they conflict. Original source evidence, licenses and immutable pins are unchanged. Existing feature work packages remain; the additional integration work packages connect them and add precise acceptance criteria. E01-E03, N01 and Q01 still apply. No extra permission round is required to implement already authorized, eligible work, but unresolved compatibility or rights issues must not be hidden.

## Handoff instruction for the AI implementation agent

> Read this document, the eight SDK specifications and the existing naming policy. Start SDK-I01 to lock the command reference and record exact contract mappings. Complete the prerequisite foundation slice, then implement SDK-I02 through SDK-I12 in dependency order. Preserve exact upstream names, concepts and applicable command grammar. Use Java internally, with no replacement Java framework dependencies. Build a minimal console/library/local-feed path first. Commit executable tests and evidence with each slice. Keep failed, blocked and deferred capabilities visible. Do not market the result as exact .NET compatibility until the relevant differential and integration gates pass.
