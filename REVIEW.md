# Reviewer guide and readiness record

**Snapshot:** `6e44986dc83c60aa6aee3e8429be0a35179c8436` (Batch 2525, 6 November 2026). This document describes the checked-in snapshot; it does not claim that a live remote, release registry, or external proof store was checked on every review.

## What is available for review

| Scope | Evidence to inspect | Current claim |
|---|---|---|
| Ecosystem plan | [Stage-2 index](planning/stage-2/README.md), [repository status data](planning/stage-2/evidence/repository-status.json), [task backlog](planning/stage-2/evidence/task-backlog.json), [designed acceptance cases](planning/stage-2/evidence/acceptance-fixtures.json) | 66 targets, 356 work packages, 1,356 named tasks, and 1,311 designed cases. These counts describe plans, not implemented features or executed acceptance cases. |
| Progress | [Implementation ledger](planning/stage-2/IMPLEMENTATION-PROGRESS.json), [Batch 2525 report](planning/stage-2/implementation/batches/Batch-2525.md), [three-task acceptance record](planning/stage-2/implementation/acceptance/Batch-2523-accepted-tasks.json) | 2,525 bounded batches; 3/1,092 accepted implementation tasks; 0/66 fully qualified frameworks. The next proposed work is Batch 2526. |
| Core Java | [Public candidates](dotj-core/dotj-core-public/src/main/java), [internal prototypes](dotj-core/dotj-core-01/src/main/java), [core tests](dotj-core/dotj-core-public/src/test/java), [bounded candidate gate](planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json) | Source and tests exist; the candidate gate reports a bounded pass and explicitly says `releaseQualified: false`. Core E01/E02/E03/N01 remain in progress. |
| Evaluation SDK | [Seed README](dotj-sdk/README.md), [seed build scripts](dotj-sdk/seed), [Batch 2523 record](planning/stage-2/implementation/batches/Batch-2523.md) | A JDK-only development seed and launcher have accepted bounded tasks. Full SDK functions and public distribution remain open. |
| Build evaluator | [Candidate README](dotj-build/evaluation-candidate/README.md), [build oracle guide](tools/oracle/dotj-build/README.md) | Internal project-evaluation candidates and fixtures exist. This is not a supported public Microsoft.Build-compatible product. |

The progress ledger is the current numerical source. Earlier Stage-1 and Stage-2 planning documents describe the state when those packages were written and can be stale about later implementation.

## Testing and reproducibility

- The checked-in [Batch 2000 report](planning/stage-2/implementation/batches/Batch-2000.md) records a 20/20 bounded foundation gate pass for selected `TimeSpan.TryParse` cases. The [candidate gate record](planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json) lists its checks and states that public qualification remains open.
- The [foundation gate runner](tools/oracle/dotj-core/run-foundation-gate.py) describes selected Java fixtures, .NET reference oracles, upstream test probes, and a pinned JDK/CoreLib environment. Its execution can create build and evidence output; review the script and prerequisites before running it.
- The [Batch 2523 acceptance record](planning/stage-2/implementation/acceptance/Batch-2523-accepted-tasks.json) cites detailed artifacts and proof files in an external `D:\AI\Implementation\...` location. Those external files are not supplied by this repository, so a reviewer with only this checkout can inspect the committed summary but cannot independently replay every cited proof.
- A new reviewer should record the exact commit, toolchain, output directory, commands, exit status, and retained result hashes for any rerun. Do not convert a scoped passing fixture into a general compatibility claim.

## Decisions still needed before public release or an OSS program application

| Gate | Current evidence | Review action |
|---|---|---|
| Public hosting and maintainer activity | The configured remote for this snapshot is Azure DevOps; this repository does not supply a public GitHub URL, release history, usage metrics, or public PR/issue history. | Confirm the intended public repository and record real adoption and maintenance signals. The [Codex for Open Source form](https://openai.com/form/codex-for-oss/) asks for a public GitHub repository. |
| Rights and notices | [`dotj-core/LICENSE`](dotj-core/LICENSE) contains MIT text. [Provenance policy](planning/stage-2/05-PROVENANCE-AND-MAINTENANCE.md) and [core E01 review packet](planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json) leave source/notice applicability and release review open. | Decide the exact scope of each license and notice for any public source or binary release. Do not infer a repository-wide license from the core file. |
| Compatibility and release scope | [Implementation ledger](planning/stage-2/IMPLEMENTATION-PROGRESS.json) shows no fully qualified framework. The [SDK README](dotj-sdk/README.md) lists its narrow admitted behavior and exclusions. | Name a small first supported slice, run its release gates, and document deviations and supported environments. |
| Public onboarding and security | This snapshot has no repository-root license, public release notes, GitHub CI workflow, or verified private vulnerability-reporting channel. | Add these after the hosting, rights, maintainer-contact, and supported-slice decisions are made. Avoid publishing a security contact that has not been confirmed. |

This guide is for technical review. It does not grant release approval, establish legal rights, or establish eligibility for an external program.
