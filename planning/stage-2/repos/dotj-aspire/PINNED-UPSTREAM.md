# DJ-013 .j Aspire: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/microsoft/aspire |
| Effective canonical source | https://github.com/microsoft/aspire |
| Immutable analysis revision | `118781118dddea1f7a524ab3d244fa4cee3c62cf` |
| Immutable tree | [118781118dddea1f7a524ab3d244fa4cee3c62cf](https://github.com/microsoft/aspire/tree/118781118dddea1f7a524ab3d244fa4cee3c62cf) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 13147 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [playground/AksDemo/AksDemo.AppHost/AppHost.cs](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/AksDemo/AksDemo.AppHost/AppHost.cs) | `7699b63f9da09b3864d6af168e720e33b7f60a79c0ca8324b6024db3ae4fae24` |
| [playground/AksDemo/AksDemo.ApiService/Program.cs](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/AksDemo/AksDemo.ApiService/Program.cs) | `d099d3632733877d0dfe356d3df8775a3473c4ba83a51b3ceda331db3cf9a5ee` |
| [playground/KnownResourceNames.cs](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/KnownResourceNames.cs) | `d21e7e91f925d54626ae64c80f7455cf8d44a6c8dbebcb13c9f1b37392475db6` |
| [tests/Aspire.Cli.Tests/ProgramTests.cs](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/ProgramTests.cs) | `ab4cd24b336b0cf68e4eb21e0ebf284f35676868b6e4b2b1aa1ba7f5be55f4d2` |
| [tests/Aspire.Cli.Tests/CliSmokeTests.cs](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/tests/Aspire.Cli.Tests/CliSmokeTests.cs) | `35f8738117fd6ee42c076365904a4e78b058760442b524f00f63c93e94a463a9` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
