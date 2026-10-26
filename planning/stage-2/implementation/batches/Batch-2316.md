# Batch-2316: Implemented Decimal IComparable/IFormattable declarations and selected Type mappings; corrected native comparison and invalid-standard-format failure text while preserving existing formatting/arithmetic.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented Decimal IComparable/IFormattable declarations and selected Type mappings; corrected native comparison and invalid-standard-format failure text while preserving existing formatting/arithmetic. |
| Validation | 331/331 foundation checks; 2378 groups from 228 object comparisons, 960 native interface formats, 1188 immutable bit snapshots and two interface identities; previous JAR fails typed interface compilation; retained numeric/rounding/message/interface/API checks passed. Selected interface profile explicitly expands from one to three implemented Decimal interfaces; native profile recaptured. |
| Limitation | Selected Decimal object-comparison and string-format interface dispatch only. Char/UTF8 span interfaces and complete generic numerics/reflection remain open; no task/framework acceptance. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,316 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 184 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2317: Implement and qualify Decimal ISpanFormattable Char array and sliced-span formatting using existing selected format behavior; verify buffer/written-count/provider/error boundaries and explicitly retain UTF8/full ABI work. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
