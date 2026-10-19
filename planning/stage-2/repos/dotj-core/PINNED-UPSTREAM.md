# DJ-001 .j Core: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/runtime |
| Effective canonical source | https://github.com/dotnet/runtime |
| Immutable analysis revision | `9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819` |
| Immutable tree | [9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | partial listing |
| Listed blob paths | 48370 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


The inspected global.json requests a .NET 11 release-candidate SDK. This is a development analysis pin, not an established GA compatibility baseline. The complete immediate src/libraries listing has 218 directories; the overall recursive source listing is partial.

## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/libraries/Microsoft.CSharp/ref/Microsoft.CSharp.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.CSharp/ref/Microsoft.CSharp.cs) | `dae7e40cc45eb2f9328ab6a949d83700e9b1128870f66bcf86c8c3e66bc7dc8b` |
| [src/libraries/Microsoft.Extensions.Caching.Abstractions/ref/Microsoft.Extensions.Caching.Abstractions.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Caching.Abstractions/ref/Microsoft.Extensions.Caching.Abstractions.cs) | `159e325c51ddb12aec576a37d1b23c6a9973c9df9eaaec741ada0a19648a8191` |
| [src/libraries/Microsoft.Extensions.DependencyInjection/src/ServiceProvider.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/src/ServiceProvider.cs) | `7e2c220000026da888b3cb3d1b773273f49ee4709f70f8b29cde590cf7dda598` |
| [src/libraries/Microsoft.Extensions.DependencyInjection/src/CallSiteJsonFormatter.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/src/CallSiteJsonFormatter.cs) | `11a6b87e539c7aeac80f2b0a298115884e03002c00da6c592d2ea758abed2494` |
| [src/tasks/Common/Utils.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/tasks/Common/Utils.cs) | `31d8eb82f660c2189d80bf7b14bf3a5ffbac1289ae64aa50497983d1c49c20a7` |
| [src/mono/wasm/Wasm.Build.Tests/IcuTests.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/mono/wasm/Wasm.Build.Tests/IcuTests.cs) | `139f98280a3fbbedec894a51862050076e967fe9fb8521abab4085ee813fafd2` |
| [src/libraries/System.Linq/tests/AllTests.cs](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/tests/AllTests.cs) | `b82d5362e9a4c6cfda2e4357f6b0877e1e6215db7ef42ef803147c3875f2ce96` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
