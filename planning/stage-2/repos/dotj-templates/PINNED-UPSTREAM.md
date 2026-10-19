# DJ-010 .j Templates: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/templating |
| Effective canonical source | https://github.com/dotnet/sdk |
| Immutable analysis revision | `c70b3856e7948678daa3950ec5517759754bf47c` |
| Immutable tree | [c70b3856e7948678daa3950ec5517759754bf47c](https://github.com/dotnet/sdk/tree/c70b3856e7948678daa3950ec5517759754bf47c) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1960 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


Source relocation: requested repository revision `7ce3ee46d3fc002dccef042c7847bd9db0a730e9` is retained as archive/move evidence. Effective source scope is `src/Cli/Microsoft.TemplateEngine` and matching engine source paths recorded in inventory. Its parent repository is not absorbed into this target.

## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/TemplateEngine/Microsoft.TemplateEngine.Abstractions/PublicAPI.Shipped.txt](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/TemplateEngine/Microsoft.TemplateEngine.Abstractions/PublicAPI.Shipped.txt) | `a01c78aa366add95395d19ceb3df168ca3af0f957e195ede97c22a2abd05eb8e` |
| [src/TemplateEngine/Microsoft.TemplateEngine.Core.Contracts/PublicAPI.Shipped.txt](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/TemplateEngine/Microsoft.TemplateEngine.Core.Contracts/PublicAPI.Shipped.txt) | `9ae6d610893fbafe2cbd1fb3001bf38bdb65098bedb4fb38d194bab0a016e1d9` |
| [src/TemplateEngine/Shared/JExtensions.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/TemplateEngine/Shared/JExtensions.cs) | `f282ea39be75e8a853a3d16eff1d4389c66b61faa4e3a154ee4ca44ec1ab7dc8` |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/JExtensionsTests.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/JExtensionsTests.cs) | `b664ee0816d027fd2ca0865f4cabe24de2a4a00c29e55504b7761ce91fd54b11` |
| [test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/Microsoft.TemplateEngine.Cli.UnitTests/TabularOutputTests.cs) | `b5213be4f3d5b67b4f81a71ca791d1224282c935ec413f9bbf7847ce8ced5a03` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
