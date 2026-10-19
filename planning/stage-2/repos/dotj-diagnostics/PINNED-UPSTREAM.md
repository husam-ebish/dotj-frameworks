# DJ-007 .j Diagnostics: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/diagnostics |
| Effective canonical source | https://github.com/dotnet/diagnostics |
| Immutable analysis revision | `1d95e75015fa3ccd063a59ed3d0bfe26040a6637` |
| Immutable tree | [1d95e75015fa3ccd063a59ed3d0bfe26040a6637](https://github.com/dotnet/diagnostics/tree/1d95e75015fa3ccd063a59ed3d0bfe26040a6637) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 2824 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Microsoft.Diagnostics.DebugServices.Implementation/Host.cs](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Host.cs) | `8947981fb137910e9bdd1329d4d75a1d2751a6d0c401de88574612d9d585ae0c` |
| [src/Microsoft.Diagnostics.DebugServices.Implementation/Module.cs](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Module.cs) | `2b62b8b510da593fec46ace478db491007289439a35786739286d8a9e76ff1db` |
| [src/Microsoft.FileFormats/SizeT.cs](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.FileFormats/SizeT.cs) | `ce1f545e2a506df854b153240504ce5f3e403e5b7d6654cc0e15f5e01574a953` |
| [src/tests/SOS.Tests/ClrUTests.cs](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/ClrUTests.cs) | `21ed8a49411bdca03358f357f81dfc408ff8f75d5588f3b2cec69b864bd5d65a` |
| [src/tests/SOS.Tests/DumpIlTests.cs](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/tests/SOS.Tests/DumpIlTests.cs) | `099dc767f2353fdfba271506c89e48eb7b37a42f778785bdbe9467c18179d385` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
