# DJ-030 .j Scheduler: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/quartznet/quartznet |
| Effective canonical source | https://github.com/quartznet/quartznet |
| Immutable analysis revision | `a94922ad3b1c2efa6d2613916fa2f386aede6681` |
| Immutable tree | [a94922ad3b1c2efa6d2613916fa2f386aede6681](https://github.com/quartznet/quartznet/tree/a94922ad3b1c2efa6d2613916fa2f386aede6681) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 2930 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Quartz/Key.cs](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Key.cs) | `68d4677c1f8d1d3112ae97fe5034315474632613a45301dd59e36749132c29ff` |
| [src/Quartz/IJob.cs](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/IJob.cs) | `07215324649795fbc377afcb5086151c7c02b1046b7f3b8ba6f0929695c441cf` |
| [src/Quartz.Tests.Unit/SimpleTriggerDstTests.cs](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/SimpleTriggerDstTests.cs) | `161cc04675b6efd21f84070426d53f13527314ff8e7f32693cb19ccfa7812e60` |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs) | `c1d255488a8d83b6c673d1a6a53888f00d0e29e6cf96873f4c5dfbb96f361a85` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
