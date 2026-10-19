# DJ-060 .j ML: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/machinelearning |
| Effective canonical source | https://github.com/dotnet/machinelearning |
| Immutable analysis revision | `655f469b0d54bccf94dc251b8db457b57d56d084` |
| Immutable tree | [655f469b0d54bccf94dc251b8db457b57d56d084](https://github.com/dotnet/machinelearning/tree/655f469b0d54bccf94dc251b8db457b57d56d084) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 4362 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Microsoft.ML.Core/PublicKey.cs](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/src/Microsoft.ML.Core/PublicKey.cs) | `268b024fafa790f035993581b5c6780602d28e2c1740c5414f1f0818aff717ca` |
| [src/Microsoft.ML.Core/BestFriendAttribute.cs](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/src/Microsoft.ML.Core/BestFriendAttribute.cs) | `3297387785388032071f525231d138ff5f5ac8a96e5856a0ece381f815869fdb` |
| [src/Microsoft.ML.Maml/MAML.cs](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/src/Microsoft.ML.Maml/MAML.cs) | `721da39be861797cd9091d90f5413c27ffd8346f57ca8e1e77d808079258694f` |
| [test/Microsoft.ML.Tests/ImagesTests.cs](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs) | `86edfd67d41be19a4d867b7c36c26348f6251bd7e3b9208eda022056675ecd91` |
| [test/Microsoft.ML.Tests/CachingTests.cs](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/CachingTests.cs) | `b5c66b08d42cbff69c351226ae73868db23e1949f0b6e11f0efdf2b26fe091b0` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
