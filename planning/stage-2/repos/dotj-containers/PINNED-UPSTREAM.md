# DJ-011 .j Containers: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/dotnet-docker |
| Effective canonical source | https://github.com/dotnet/dotnet-docker |
| Immutable analysis revision | `a5ada4c290f2dc087c6926beeeaffcd07912abe7` |
| Immutable tree | [a5ada4c290f2dc087c6926beeeaffcd07912abe7](https://github.com/dotnet/dotnet-docker/tree/a5ada4c290f2dc087c6926beeeaffcd07912abe7) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1941 |
| New sampled source/API/test files | 2 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs) | `b3ac27593931ce99bcf539206a04c8db7e303218cbbe2c81c330fca7ce6f483a` |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs) | `d986a67b4f02b0d621a56b812ab4d9319bf866d1e5d36b7e6060716923cf4c34` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
