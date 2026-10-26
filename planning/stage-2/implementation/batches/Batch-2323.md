# Batch-2323: Added Decimal String NumberStyles-only Parse overload and Char-span optional-provider convenience adapter; expanded exact API declarations.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Added Decimal String NumberStyles-only Parse overload and Char-span optional-provider convenience adapter; expanded exact API declarations. |
| Validation | 338/338 foundation checks; 147 groups: 144 native outcomes, two exact method shapes and ambiguous-null compile rejection; previous JAR lacks overloads; retained parsing/formatting/conversion/interface/API checks passed. |
| Limitation | Selected overload delegation and invariant styles only. Legacy format/overflow message text is explicitly deferred; ambient culture, UTF8, full grammar/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,323 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 177 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2324: Verify native Decimal Parse/TryParse provider callback ordering, exception identity and result preservation across String and Char-span routes. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
