# How to start implementation from this plan

**Owner requirement:** exact upstream .NET public names, casing and concepts across all 66 repositories. Read [the mandatory naming policy](08-DOTNET-API-COMPATIBILITY-POLICY.md). N01 adds a source-to-Java public API mapping and concept-preservation gate; Java implementation details must not become a replacement learning path.

**You now have the full written Stage-2 plan for all 66 repositories.** Commit it in the main repo. The next work is the first implementation slice, beginning with its explicit evidence gates; another whole-ecosystem planning response is not required.

## First selected slice: dotj-core foundation

Use [core WORK-PACKAGES](repos/dotj-core/WORK-PACKAGES.md), [architecture](repos/dotj-core/JAVA-ARCHITECTURE.md) and [deeper foundation contracts](repos/dotj-core/foundation-research/JAVA-ARCHITECTURE.md).

1. Complete E01 for the portable foundation: qualify an immutable runtime reference profile, resolve its source/dependency rights, lock the .NET oracle and exact JDK binary. Do not assume the currently inspected prerelease-development pin is a GA baseline.
2. Complete E02 for WP-01/WP-02 only: semantic public API and conditional dependency mapping for type identity, errors/context, ownership and cancellation. Whole-core BCL/native work remains retained for later slices.
3. Complete E03 for those contracts: actual upstream test IDs, expected raw oracle results, Java adaptation decisions and fixture envelopes. The supplied designed fixture IDs are the starting acceptance requirements.
4. Complete N01 for this slice: exact names/namespaces, public .NET type vocabulary, concept/lifecycle mapping and unavoidable syntax representations. Keep helper types internal. Then, after implementation is requested and these gates pass, create minimal independently compilable foundation modules, test fixtures and plain subprocess runners. Use installed javac/jar; do not wait for SDK/build/package/test frameworks to be finished.
5. Implement WP-01, then WP-02. Verify resource ownership, partial-failure cleanup, context isolation, late cancellation registration, unregister/close distinctions and callback races. Freeze only the contracts actually validated.
6. Continue default DI/configuration and then options/logging/hosting. Begin separate JSON/build/test tool slices when their narrow core prerequisites are ready.

## Definition of done for the first slice

- Exact baseline, dependency/toolchain and rights evidence is recorded.
- Source-derived public contract signatures preserve exact .NET names/casing/concepts, with explicit syntax representations and a versioned N01 ledger.
- A clean build works with the documented bootstrap tools.
- Mapped oracle fixtures and designed negative/concurrency/lifecycle cases pass.
- Caller-owned resources remain caller-owned; failed construction and cancellation release owned state.
- A small documented usage example demonstrates the accepted behavior.
- Unsupported APIs and remaining whole-core scope remain visible.

## Suggested implementation handoff text

> Begin the first dotj-core foundation implementation slice using planning/stage-2. Complete E01-E03 and N01 for WP-01/WP-02, preserve the exact .NET public names and concepts, then implement only the eligible contracts and cancellation/resource behavior. Use the pinned evidence, keep unresolved rights/platform gates visible, preserve all other repositories' scope, and report the exact tests and compatibility profile achieved.

This is a handoff you can use when requesting implementation. This planning package itself has not created application source or changed your Windows/Azure DevOps repository.
