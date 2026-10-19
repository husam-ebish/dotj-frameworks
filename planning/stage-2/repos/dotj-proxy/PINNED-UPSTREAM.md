# DJ-014 .j Proxy: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/yarp |
| Effective canonical source | https://github.com/dotnet/yarp |
| Immutable analysis revision | `2aa3d83550a9b7a719e347ef6a0363e5ea9505a9` |
| Immutable tree | [2aa3d83550a9b7a719e347ef6a0363e5ea9505a9](https://github.com/dotnet/yarp/tree/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1054 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Application/Program.cs](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Program.cs) | `568ce25064e8310d14afa3f18f6ba184ba6652537f38ca458a6501027bbae036` |
| [src/Application/Extensions.cs](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Extensions.cs) | `712f44d0eecf42d6da2e2bcf86a5b079db8e60a31bc2b71ffb9c0fbb188e2ab8` |
| [test/Kubernetes.Tests/ReconcilerTests.cs](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Kubernetes.Tests/ReconcilerTests.cs) | `a89bbc3f832ee64a591f64344763cf0a20463f7bea100f6ff6242182f24fbf43` |
| [test/Application.Tests/SpaFallbackTests.cs](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs) | `fb927b6b9d9c44cf685eca80ae4ea438adf0eea5e4512142ab512ad6425b690f` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
