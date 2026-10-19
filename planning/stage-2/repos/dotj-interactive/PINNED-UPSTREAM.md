# DJ-008 .j Interactive: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/interactive |
| Effective canonical source | https://github.com/dotnet/interactive |
| Immutable analysis revision | `098a01b9183103186805a186a7dee3a3a70b2997` |
| Immutable tree | [098a01b9183103186805a186a7dee3a3a70b2997](https://github.com/dotnet/interactive/tree/098a01b9183103186805a186a7dee3a3a70b2997) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 2172 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Microsoft.DotNet.Interactive.AspNetCore/Startup.cs](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Startup.cs) | `a9f6e156d0b8be402db25ac25c1e50fcae1ee0e40835448bd555c19c6ca0afae` |
| [src/Microsoft.DotNet.Interactive.AspNetCore/LogMessage.cs](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/LogMessage.cs) | `f55872ef37f36353dbcc02266f4d51c710efffa8dfdefb275bbbd3c531389aac` |
| [src/dotnet-interactive/Program.cs](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive/Program.cs) | `26e6c538e801cbf4e9f16c90a9753f1ab70734916bd9645973981ac282df265d` |
| [src/dotnet-interactive.Tests/HttpApiTests.cs](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs) | `04e1f13cbe5c74a400e7b1a8008ffe98a2253b8ec2fc79995185eea2ffcfb2ef` |
| [src/dotnet-interactive.Tests/FileProviderTests.cs](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/FileProviderTests.cs) | `7505e3d13819ae3e55688943d9f43a798acf28aadd26f28a86742d2d2bb44e83` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
