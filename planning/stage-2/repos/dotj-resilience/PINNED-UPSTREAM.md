# DJ-027 .j Resilience: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/App-vNext/Polly |
| Effective canonical source | https://github.com/App-vNext/Polly |
| Immutable analysis revision | `3f3adad9d5af85658fc3585018f02a2d8c2173e8` |
| Immutable tree | [3f3adad9d5af85658fc3585018f02a2d8c2173e8](https://github.com/App-vNext/Polly/tree/3f3adad9d5af85658fc3585018f02a2d8c2173e8) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1026 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Polly.Core/.PublicAPI/PublicAPI.Shipped.txt](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/.PublicAPI/PublicAPI.Shipped.txt) | `2da557319867b292cc267ee669d910eb625382d60f346388c0661f90bfb05370` |
| [src/Polly.Extensions/.PublicAPI/PublicAPI.Shipped.txt](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Extensions/.PublicAPI/PublicAPI.Shipped.txt) | `ec2bdee0dedfda85a42466399b2654f6832ee6dbe3ef4c28d1d3fab0fc055228` |
| [src/Polly.Core/Outcome.cs](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Outcome.cs) | `85912d2db5c5cce3d8875d1c679cc0e35c8cfb7e4d6060ebb6542ad39dac8249` |
| [src/Polly.Core/VoidResult.cs](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/VoidResult.cs) | `f09a96e85de8f6fdde7ea3836aba1292b5b4027b622b99ead243aa4b17b18a71` |
| [cake.cs](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/cake.cs) | `ab39b46c8e5e015a1c187fa4a7a52811a3c41281312ae2d0e419e63263bf5895` |
| [test/Shared/StrongNameTests.cs](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Shared/StrongNameTests.cs) | `95ac27a5da396d441948599be7a6562c5aae46c4c4942184580c6f0b1c61567d` |
| [test/Polly.Core.Tests/OutcomeTests.cs](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs) | `9e8454e6fd76cc3a61fa562cb596faab437211dbd754d836d590936afe56e7e9` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
