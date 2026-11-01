# Foundation acceptance review after Batch 2500

Batch 2501 reviews what blocks task acceptance after the authorized numbered milestone. It changes no product source and grants no acceptance credit.

## Measured position

| Measure | Value |
|---|---|
| Accepted implementation tasks | 0/1092 |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Frameworks in progress | 2 (`dotj-core`, `dotj-build`) |
| `dotj-core` named tasks | 11 in progress, 20 not started |
| Foundation gates | E01, E02, E03 and N01 in progress; Q01 not started |
| Candidate | 108 sources, unchanged JAR `fc7c2a41...`, 515-check gate passed |

The current task tracker records no in-progress `dotj-build` task, although its bounded evaluator work is merged. That status needs reconciling when its acceptance is reviewed.

## Why acceptance remains zero

1. Every work package requires N01 and its E01-E03 slice closure. Those gates are still open.
2. E01 has three open review decisions: source and notice applicability, reference and dependency rights, and release review. The notice queue names four overlap paths: `DateTime`, `Decoder`, `Encoder` and `TimeSpan`.
3. Recent batches 2392-2500 sharpened Exception, Type, reflection and enum field behavior. That work supports `DJ-001-N01-T2` and WP-08, but it does not close a WP-01 or WP-02 acceptance statement.
4. The roadmap order is WP-01, WP-02, then WP-03/WP-04. The public source root has `System.IDisposable` and `System.Type`, but no `System.IAsyncDisposable` and no `System.Threading` cancellation or context surface.

## WP-01 acceptance gaps

| Fixture | Criterion | Current evidence | Gap |
|---|---|---|---|
| `DJ-001-F01-01` | Equal parameterized types share identity | One bounded shape plus five supporting upstream cases | Public `System.Type` mapping must carry the fixture; no direct upstream reference-identity assertion |
| `DJ-001-F01-02` | Different generic arguments do not share identity | One bounded shape plus four supporting upstream cases | Same public mapping; no direct upstream inequality assertion |
| `DJ-001-F01-03` | Supplied resources are never closed implicitly | Java and .NET oracle cases; 37 upstream DI cases | Source-backed lifecycle oracle matched to the public disposal surface |
| `DJ-001-F01-04` | Context values do not leak between requests | Java and CLR same-worker cases; two supporting upstream methods | Public `ExecutionContext`/`AsyncLocal` mapping; mechanisms still differ |

## Retained unmerged work

| Worktree branch | State | Use |
|---|---|---|
| `feature/dotj-core-ownership-source-qualification-v1` | Untracked static lifecycle tools; 30 batches behind master | `DJ-001-WP-01-T2`, `DJ-001-F01-03` |
| `feature/dotj-build-condition-logic-v2` | Untracked native preparation; pass 2 ran and awaits review | `DJ-005-WP-01-T1`, And/Or conditions |
| `feature/dotj-core-provenance-history-audit` | One unmerged tooling commit | Gate performance only |

## Decision

Stop adding enum and reflection detail batches. Future numbered batches must each name the acceptance statement or E01-E03/N01 decision they close. Work in this order:

1. Finish the ownership lifecycle oracle for `DJ-001-WP-01-T2` and `DJ-001-F01-03`.
2. Review the `dotj-build` condition pass 2 and finish And/Or for `DJ-005-WP-01-T1`.
3. Add the public async disposal and context mapping needed by `DJ-001-F01-04`.
4. Start the public WP-02 cancellation contract and fixtures `DJ-001-F02-01` to `DJ-001-F02-05`.

The three E01 decisions stay open for the repository licensing review. No task can be recorded as accepted while they apply to its slice. The project batch total remains unknown.
