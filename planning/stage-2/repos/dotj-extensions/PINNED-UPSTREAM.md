# DJ-006 .j Extensions: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/extensions |
| Effective canonical source | https://github.com/dotnet/extensions |
| Immutable analysis revision | `42a0f358b14bb27bc324939d858dd04309f30477` |
| Immutable tree | [42a0f358b14bb27bc324939d858dd04309f30477](https://github.com/dotnet/extensions/tree/42a0f358b14bb27bc324939d858dd04309f30477) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 3721 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Analyzers/Microsoft.Analyzers.Extra/DiagDescriptors.cs](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Analyzers/Microsoft.Analyzers.Extra/DiagDescriptors.cs) | `2f74a0d8bdb3fdf83e832b91ef2c51397974f121ebf26cfe460de23907176d27` |
| [src/Analyzers/Microsoft.Analyzers.Local/DiagDescriptors.cs](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Analyzers/Microsoft.Analyzers.Local/DiagDescriptors.cs) | `68f4066272da985d87f054ea77c5dc1a74d08e7ea3624b37d97cb02797d9215c` |
| [src/Shared/Throw/Throw.cs](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Shared/Throw/Throw.cs) | `a02163eb4daea112efb32c14be664bc2a44c6066637539c96c5ebd08831682b8` |
| [test/Shared/Pools/PoolTests.cs](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Pools/PoolTests.cs) | `28732c396f09367108454afaa9bf641a955a2b35f36197a6da18a1c8a235b625` |
| [test/Shared/Throw/LongTests.cs](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/test/Shared/Throw/LongTests.cs) | `2e9cefa11ad5cb6cdb63d6c25e854cdbc6e853158251336c45e50081d9da61da` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
