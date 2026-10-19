# DJ-061 .j Semantic: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/microsoft/semantic-kernel |
| Effective canonical source | https://github.com/microsoft/semantic-kernel |
| Immutable analysis revision | `7a92cd4e7c2712370b8d85b687a474b2e858cdcc` |
| Immutable tree | [7a92cd4e7c2712370b8d85b687a474b2e858cdcc](https://github.com/microsoft/semantic-kernel/tree/7a92cd4e7c2712370b8d85b687a474b2e858cdcc) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 4843 |
| New sampled source/API/test files | 3 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


The README points to microsoft/agent-framework as a successor. This plan remains for the requested C# Semantic Kernel source; existing Java/Python implementations and successor code are not automatically reused.

## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [dotnet/notebooks/config/Utils.cs](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/notebooks/config/Utils.cs) | `a95d802719aa0c1c9d3bd2a34b490678206d62e95b6836848936c51336b25723` |
| [dotnet/src/IntegrationTests/PromptTests.cs](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/IntegrationTests/PromptTests.cs) | `422997774cb75c20fdfaab9d72c14e02b5ab422f6f9f156944f46a1479de6fa1` |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs) | `e4eb5272821fc43f886b27fd18547e4765f067d435958790a8804ef146101a38` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
