# DJ-002 .j SDK: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/sdk |
| Effective canonical source | https://github.com/dotnet/sdk |
| Immutable analysis revision | `c70b3856e7948678daa3950ec5517759754bf47c` |
| Immutable tree | [c70b3856e7948678daa3950ec5517759754bf47c](https://github.com/dotnet/sdk/tree/c70b3856e7948678daa3950ec5517759754bf47c) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 12023 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Containers/Microsoft.NET.Build.Containers/PublicAPI/net12.0/PublicAPI.Shipped.txt](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Containers/Microsoft.NET.Build.Containers/PublicAPI/net12.0/PublicAPI.Shipped.txt) | `7c6e932683ad1006590cf407d256c0d9264e0e1e46cd10cd769476aaa5f499f6` |
| [src/Microsoft.DotNet.ProjectTools/PublicAPI.Shipped.txt](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.DotNet.ProjectTools/PublicAPI.Shipped.txt) | `3c3b422dddb1efeb0fc5b228608fd8682452b2a9507d4031894bce3c4dedadbd` |
| [src/BlazorWasmSdk/Tool/Program.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/BlazorWasmSdk/Tool/Program.cs) | `971bb47062d98d5e8f46b097439c2cdc987dbb5d472e7f43fd63bf2cf9335282` |
| [src/BlazorWasmSdk/Tasks/BootJsonData.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/BlazorWasmSdk/Tasks/BootJsonData.cs) | `22f045ea8dcfcf63be5118b254c02f8b6f5571d86b9891cf225523b4e2cf37ca` |
| [src/Common/Polyfills.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Common/Polyfills.cs) | `00138e102a68da0924f726744b594df547e4bcc26023da36243bcedf1ef11f55` |
| [scripts/RunTests.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/scripts/RunTests.cs) | `c9c577953ba33b676450bc308be951655f549558700bae92cb67fc14e9d1bc76` |
| [test/EndToEnd.Tests/VersionTests.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/EndToEnd.Tests/VersionTests.cs) | `48eb1874e9c43eb78f2f5b1ad52ee2037cd9e40b87172a58d47577a9bdae4de6` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
