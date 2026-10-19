# DJ-066 .j Bus: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/MassTransit/MassTransit |
| Effective canonical source | https://github.com/MassTransit/MassTransit |
| Immutable analysis revision | `d9f61f764c802785cc9a4be92547d8f5b63018d4` |
| Immutable tree | [d9f61f764c802785cc9a4be92547d8f5b63018d4](https://github.com/MassTransit/MassTransit/tree/d9f61f764c802785cc9a4be92547d8f5b63018d4) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 5653 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/MassTransit/Bus.cs](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/Bus.cs) | `5bf2512337c039b592a2ed3242e909cfe539edde12653aae4a97646b6e789173` |
| [src/MassTransit/Retry.cs](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/Retry.cs) | `4e34538efdabc1a74f06b58a4268d622870708248c58c49e5b76ac4bc44bf5d7` |
| [tests/MassTransit.Tests/CronExpressionTests.cs](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs) | `22a04b646efff55efd9ac9e7906cb74232f7bd9b792a7e754bda5f263a8ea5cf` |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs) | `2d79f1ae994b88f56a3e7bc4cfb88ef5039d5dbb989dbb6656476907899978db` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
