# DJ-004 .j Razor: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/razor |
| Effective canonical source | https://github.com/dotnet/roslyn |
| Immutable analysis revision | `3645b6aa36ad41775a73e57a620787a3d38327a0` |
| Immutable tree | [3645b6aa36ad41775a73e57a620787a3d38327a0](https://github.com/dotnet/roslyn/tree/3645b6aa36ad41775a73e57a620787a3d38327a0) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 13931 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


Source relocation: requested repository revision `8fcba40eb7566d4efc2765edb5fbd517605f720b` is retained as archive/move evidence. Effective source scope is `src/Razor/` and matching engine source paths recorded in inventory. Its parent repository is not absorbed into this target.

## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Razor/src/Razor/src/Microsoft.CodeAnalysis.Razor.DotNetFormat/PublicAPI/PublicAPI.Shipped.txt](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Razor/src/Razor/src/Microsoft.CodeAnalysis.Razor.DotNetFormat/PublicAPI/PublicAPI.Shipped.txt) | `7c6e932683ad1006590cf407d256c0d9264e0e1e46cd10cd769476aaa5f499f6` |
| [src/Razor/src/Razor/src/Microsoft.CodeAnalysis.Razor.Workspaces/PublicAPI/PublicAPI.Shipped.txt](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Razor/src/Razor/src/Microsoft.CodeAnalysis.Razor.Workspaces/PublicAPI/PublicAPI.Shipped.txt) | `7c6e932683ad1006590cf407d256c0d9264e0e1e46cd10cd769476aaa5f499f6` |
| [src/Razor/src/Shared/Microsoft.AspNetCore.Razor.SharedUtilities/Opt`1.cs](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Razor/src/Shared/Microsoft.AspNetCore.Razor.SharedUtilities/Opt`1.cs) | `12923dd1813e5d54f5a68cc9a5c5aa0139070320d5ef8f0d3f089dcb8cab325f` |
| [src/Razor/src/Shared/Microsoft.AspNetCore.Razor.Utilities.Shared.UnitTests/ChecksumTests.cs](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Razor/src/Shared/Microsoft.AspNetCore.Razor.Utilities.Shared.UnitTests/ChecksumTests.cs) | `41bf993f2b325027ee840fcc749ec88bb033bd7a0d1644c5d2936e13b4489539` |
| [src/Razor/src/Shared/Microsoft.AspNetCore.Razor.Utilities.Shared.UnitTests/MemoryBuilderTests.cs](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Razor/src/Shared/Microsoft.AspNetCore.Razor.Utilities.Shared.UnitTests/MemoryBuilderTests.cs) | `c1db7ccbce8c562d7c5dd3c1b7f5cbf22ffc6e5b1a0a7c156e61360a49ee7b46` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
