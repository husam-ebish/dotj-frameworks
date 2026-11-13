# .j Frameworks

.j Frameworks is an early-stage effort to provide familiar .NET API names and workflows in Java. The intended ecosystem spans 66 framework targets. Development is incremental: the checked-in implementation currently covers selected core behavior, an unreleased evaluation SDK seed, and internal build-evaluation candidates.

**Current status:** development and review, not a qualified framework release. The [implementation ledger](planning/stage-2/IMPLEMENTATION-PROGRESS.json) records 2,525 bounded batches, 3 accepted implementation tasks out of 1,092, and 0 fully qualified frameworks out of 66 at the latest checked-in snapshot. Batches include analysis, reference experiments, fixtures, code, and tooling; they are not a count of shipped features. The total number of future batches is unknown.

## Start here

| If you want to… | Read |
|---|---|
| Understand the current evidence and review limits | [Review guide](REVIEW.md) |
| Inspect the full 66-target plan | [Stage-2 planning index](planning/stage-2/README.md) |
| Check implementation progress and open gates | [Implementation state](planning/stage-2/IMPLEMENTATION-STATE.md) and [progress ledger](planning/stage-2/IMPLEMENTATION-PROGRESS.json) |
| Inspect the core Java candidates | [`dotj-core/dotj-core-public`](dotj-core/dotj-core-public/src/main/java) and [`dotj-core/dotj-core-01`](dotj-core/dotj-core-01/src/main/java) |
| Build the bounded evaluation SDK seed | [SDK seed instructions](dotj-sdk/README.md) |
| Review the internal build evaluator | [Build evaluation candidate](dotj-build/evaluation-candidate/README.md) |
| Propose a change | [Contribution guide](CONTRIBUTING.md) |

The evaluation SDK seed is versioned `0.1.100-dev.1` and is **unreleased**. Its supported scope and exclusions are documented in its README. The build evaluator is an internal candidate, not a supported public build API. The core public-source tree contains candidate Java types, but framework-wide API compatibility, licensing, and release qualification remain open.

## How the work is organized

- `planning/` contains historical Stage-1 material, the Stage-2 architecture and work packages, pinned upstream samples, acceptance designs, batch reports, and progress records.
- `dotj-core/` contains the Java core candidates, internal prototypes, tests, and a core MIT license file.
- `dotj-sdk/` contains the JDK-only evaluation seed and launcher.
- `dotj-build/` contains bounded internal build-evaluation candidates and fixtures.
- `tools/oracle/` contains reference capture and verification tools. These tools are not the product runtime.

The root `START-HERE.md` and `APPLY-THIS-UPDATE.md` are historical planning-package handoff instructions. Use this README and the implementation ledger for current status.

## Evidence and release limits

The repository includes Java test source, .NET reference oracles, local runners, and saved validation records. A saved passing result applies to its stated slice and environment; it does not certify the 66-target ecosystem. The [review guide](REVIEW.md) identifies a bounded example and what remains unverified.

The repository has an MIT text at [`dotj-core/LICENSE`](dotj-core/LICENSE), alongside upstream source and notice evidence with separate terms. No repository-wide rights clearance or public release approval is asserted here. See [provenance and maintenance](planning/stage-2/05-PROVENANCE-AND-MAINTENANCE.md) and the [core readiness record](planning/stage-2/repos/dotj-core/READINESS.md) before distributing code or artifacts.
