# DJ-028 .j Reactive: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/reactive |
| Effective canonical source | https://github.com/dotnet/reactive |
| Immutable analysis revision | `89e05b8730107983c3f77af54a52974ae12d37f4` |
| Immutable tree | [89e05b8730107983c3f77af54a52974ae12d37f4](https://github.com/dotnet/reactive/tree/89e05b8730107983c3f77af54a52974ae12d37f4) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 2347 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [Rx.NET/Source/src/System.Reactive.MakeRefAssemblies/.PublicApi/PublicAPI.Shipped.txt](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/Rx.NET/Source/src/System.Reactive.MakeRefAssemblies/.PublicApi/PublicAPI.Shipped.txt) | `3aa64dbd6c49df1e294bc999c8cf094d91524e81d36571c1cad5ac6b355f92a6` |
| [AsyncRx.NET/ApiCompare/Program.cs](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/AsyncRx.NET/ApiCompare/Program.cs) | `1bc909d4b00fb271a6ef25050574787316f2103f556d297bd1518a6046da3654` |
| [AsyncRx.NET/Playground/Program.cs](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/AsyncRx.NET/Playground/Program.cs) | `82f882b939f6bf0b7df4e8f5ae60114cd0962f9792d64bb034bcca05a267ecec` |
| [Ix.NET/Source/System.Interactive.Tests/Tests.cs](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/Ix.NET/Source/System.Interactive.Tests/Tests.cs) | `412171e948012e3da665030b8318334e318f3354815375a1989d6440ff1a68d2` |
| [Ix.NET/Source/System.Interactive.Async.Tests/AsyncTests.cs](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/Ix.NET/Source/System.Interactive.Async.Tests/AsyncTests.cs) | `c5964e8ac8efbde5f9d37fc13a6dcfbef43d60ab1df65ccd8885349ac7eed0c1` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
