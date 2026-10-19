# DJ-019 .j Entity: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/efcore |
| Effective canonical source | https://github.com/dotnet/efcore |
| Immutable analysis revision | `2e8882748cc45b317a98a6f27f0680948221ae3b` |
| Immutable tree | [2e8882748cc45b317a98a6f27f0680948221ae3b](https://github.com/dotnet/efcore/tree/2e8882748cc45b317a98a6f27f0680948221ae3b) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 6352 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/EFCore/EF.cs](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore/EF.cs) | `1f55ac4ff3d066e4e425e15a9d404afdc6e4d7bd3db54085c55ab88974b154e6` |
| [src/EFCore/DbSet.cs](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore/DbSet.cs) | `016c00eb59f523a227d70a80b71a812cf3d5b990423cab52800b51fd36c020d0` |
| [src/ef/Json.cs](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/ef/Json.cs) | `2e7f2d8269cc7473b02dff51e7453d405eebd13a432dcb5b63a3d9b73756476d` |
| [test/EFCore.Proxies.Tests/ProxyTests.cs](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs) | `2bb1615f1f9b785f08b5cf30f4319a499f6dd66ebdfa8536dacec80dcc2fc3c5` |
| [test/EFCore.Tests/DbContextLoggerTests.cs](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs) | `92924617245a7cd8b3749c8db1e1d45d923e50b6c7c10442b701c6f2357d81b5` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
