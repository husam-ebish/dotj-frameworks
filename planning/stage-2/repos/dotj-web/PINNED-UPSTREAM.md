# DJ-012 .j Web: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/aspnetcore |
| Effective canonical source | https://github.com/dotnet/aspnetcore |
| Immutable analysis revision | `c09e2b89bd8cf25e819230a94e9061023f508afe` |
| Immutable tree | [c09e2b89bd8cf25e819230a94e9061023f508afe](https://github.com/dotnet/aspnetcore/tree/c09e2b89bd8cf25e819230a94e9061023f508afe) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 17711 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Antiforgery/src/PublicAPI.Shipped.txt](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Antiforgery/src/PublicAPI.Shipped.txt) | `ff3f42bcb840841200647aa7187fd039d1c534dde1b09bb28b4ffbae4e5dafe0` |
| [src/Azure/AzureAppServices.HostingStartup/src/PublicAPI.Shipped.txt](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Azure/AzureAppServices.HostingStartup/src/PublicAPI.Shipped.txt) | `1a90d903e72038d4e12dcef95a5d90d039f38db92a670a0cfbe1ba239426d9f1` |
| [src/Antiforgery/src/IAntiforgery.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Antiforgery/src/IAntiforgery.cs) | `0c156c50d5d936df3cfc7d322523c41b1c4a3be699d60d3e3e1c1058be04a69a` |
| [src/Antiforgery/src/AntiforgeryOptions.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Antiforgery/src/AntiforgeryOptions.cs) | `6b837f20e9582316bce0eab6ded2a68e8d8b848e148aa1c108824c79ebf09eb2` |
| [src/Shared/Reroute.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Shared/Reroute.cs) | `75a2d53a9560f57fa5afd9fcdd6fa8501ea1190bff3f31b34e81dc01a9beabf0` |
| [src/Testing/test/DockerTests.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Testing/test/DockerTests.cs) | `8fc9fb785980d5e50d9d169107a4a4f5ea06e6ff80f332086d0228cea487aa12` |
| [src/Testing/test/SkipOnCITests.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Testing/test/SkipOnCITests.cs) | `5c4eac7466dd9c1c70d9a8eb646605dc2ee91d99982f76b35245b7a880fb63f2` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
