# Batch-2001: foundation acceptance review

| Field | Result |
|---|---|
| Status | COMPLETE: bounded acceptance review and executable integrity audit |
| Scope | dotj-core foundation E01/E02/E03/N01/Q01 prerequisites; no implementation task accepted |
| Baseline | Fetched origin; master and origin/master matched `2ea47045`; clean working tree |
| Change | Added `tools/oracle/dotj-core/review-foundation-acceptance.ps1` to recompute tracker counts, verify historical evidence and product source hashes, identify open E01 decisions, and inventory local validation prerequisites |
| Verification | Audit passed; 9 evidence-file and 73 product-source SHA-256 hashes matched; negative fixtures rejected a wrong open-item count, altered review decision, and altered product source; restored fixture passed |
| Candidate validation | Historical gate records 20 checks. Packaged consumers and gate were **not rerun**: Python, JDK tools, pinned SDK 10.0.401, runtime 10.0.12 and candidate JAR are absent here |
| Local .NET | SDK 10.0.402 and runtime 10.0.13; these do not satisfy the pinned oracle |
| E01 decisions | SOURCE_AND_NOTICE_APPLICABILITY, REFERENCE_AND_DEPENDENCY_RIGHTS and RELEASE_REVIEW remain OPEN |
| Other gates | E02, E03 and N01 IN PROGRESS; Q01 NOT STARTED |
| Missing old-PC context | No applicable AGENTS.md, installed RooFlow skill or project RooFlow memory found in searched locations; repository plans and trackers used directly. No C# changed |
| Temporary files | `D:\AI\Implementation\dotj Frameworks\Batch-2001\` (logs and isolated negative-test fixture) |

The integrity audit verifies current checked-out bytes against historical evidence. It does not rebuild the candidate, prove behavior, verify local toolchain binary hashes, or grant rights/release approval. A successful review can therefore coexist with unavailable validation prerequisites. Evidence changes cause a visible failure rather than silently refreshing the old gate.

Run from the repository root (execution-policy override applies only to this process):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/review-foundation-acceptance.ps1
```

Optional `-OutputPath` writes JSON to an existing directory. Use a path under the project directory on D: for local logs. `-RepositoryRoot` supports auditing an isolated evidence fixture without changing the checkout.

## Acceptance and next work

| Metric | Actual value |
|---|---|
| Numbered batches completed | 2,001 |
| Remaining to original 2,000 target | 0; original target already reached |
| Project batches planned / remaining | Unknown / unknown; no new fixed total established |
| Accepted implementation tasks | 0 / 1,092 (0.00%) |
| Open acceptance items | 1,686: 330 gates + 264 naming prerequisites + 1,092 implementation tasks |
| Qualified frameworks | 0 / 66 |
| Acceptance credit this batch | None; prerequisite review only |
| Git workflow | `feature/batch-2001-foundation-acceptance-review`, merge to master, then push master; actual result reported after execution |
| Next concrete task | Batch-2002: restore isolated pinned validation tools on D:, verify baseline binary hashes, redirect gate build/cache output off C:, and rerun packaged consumers plus the 20-check foundation candidate gate |

The next task addresses the reproducibility gap before adding another public API. The existing gate scripts place build outputs inside the C: checkout; those paths must be made configurable before running them under the current storage instruction. Restoration and a fresh bounded pass still will not close the three E01 review decisions or qualify a framework. Subsequent acceptance work should follow WP-01/WP-02 prerequisites and mapped fixtures in `WORK-PACKAGES.md` and `07-IMPLEMENTATION-START.md`, rather than counting additional API methods as accepted tasks.
