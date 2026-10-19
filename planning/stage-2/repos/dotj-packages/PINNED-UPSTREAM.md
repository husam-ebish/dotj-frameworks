# DJ-062 .j Packages: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/NuGet/NuGet.Client |
| Effective canonical source | https://github.com/NuGet/NuGet.Client |
| Immutable analysis revision | `4c4510d29a64fcbcba6360e29c3a1e8288a87f9f` |
| Immutable tree | [4c4510d29a64fcbcba6360e29c3a1e8288a87f9f](https://github.com/NuGet/NuGet.Client/tree/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 5870 |
| New sampled source/API/test files | 6 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/NuGet.Clients/NuGet.Indexing/PublicAPI.Shipped.txt](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.Indexing/PublicAPI.Shipped.txt) | `5e3685170fa6443d1028af355a4a8dcd6a68e30b7fcc4b5baf1bb0679d71b995` |
| [src/NuGet.Clients/NuGet.VisualStudio.Contracts/PublicAPI.Shipped.txt](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Contracts/PublicAPI.Shipped.txt) | `34da76affb8f5f84cae0bb627e8e89a919ff973ca097cdbf709cc56c9e2dcb90` |
| [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGetExtension.cs](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGetExtension.cs) | `1f8ed943aa505666452b36cd72dfbf7add14eb5be5ca38c72f77847d090c42f2` |
| [tools-local/ship-public-apis/Program.cs](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/tools-local/ship-public-apis/Program.cs) | `63fe4a182c99bdc449ead69486c1eb84fe1d392feec8428dec46fb565b739f51` |
| [test/NuGet.Tests.Apex/NuGet.OptProf/Tests.cs](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Tests.Apex/NuGet.OptProf/Tests.cs) | `08d415c6fc427d41cb5f9110ee4b8fed82691286cbc50feba318dc727a423789` |
| [test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Commands.Test/CycleTests.cs) | `4581ce4bfcded86fc85e4d8b3161ff5a3e8b26145415ee9bc4a63c2254f5e892` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
