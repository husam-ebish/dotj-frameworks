# Batch-2315: Corrected represented core interface-name ignoreCase matching to reject non-ASCII aliases consistently across existing enum/numeric/encoding/protocol type mappings.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected represented core interface-name ignoreCase matching to reject non-ASCII aliases consistently across existing enum/numeric/encoding/protocol type mappings. |
| Validation | 330/330 foundation checks; 9207 native lookups across 31 receivers, 99 name profiles and three routes; dotted/dotless-I and long-S substitutions, exact namespace, null and overload boundaries; prior JAR admits bad aliases; retained lookup/enum/API consumers passed. |
| Limitation | Selected core interface names on 31 types only. Native generic inventories are reference-only; separate missing Decimal interfaces are recorded for next implementation. Full reflection, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,315 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 185 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2316: Implement and qualify existing Decimal comparison/formatting methods through IComparable and IFormattable, with selected Type interface mapping; leave Char/UTF8 span implementation as explicit follow-up. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
