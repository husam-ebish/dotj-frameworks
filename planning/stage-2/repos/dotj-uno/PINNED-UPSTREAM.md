# DJ-044 .j Uno: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/unoplatform/uno |
| Effective canonical source | https://github.com/unoplatform/uno |
| Immutable analysis revision | `78728530f26880286be77d9042a8e4118a42df43` |
| Immutable tree | [78728530f26880286be77d9042a8e4118a42df43](https://github.com/unoplatform/uno/tree/78728530f26880286be77d9042a8e4118a42df43) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 24699 |
| New sampled source/API/test files | 3 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Uno.Sdk/UnoArea.cs](https://github.com/unoplatform/uno/blob/78728530f26880286be77d9042a8e4118a42df43/src/Uno.Sdk/UnoArea.cs) | `cf1043dbfb4a95f12d463f15d429173e5e9b7c5441ecb9999e5544ebc9087a7d` |
| [src/Uno.Analyzers.Tests/UnoNotImplementedTests.cs](https://github.com/unoplatform/uno/blob/78728530f26880286be77d9042a8e4118a42df43/src/Uno.Analyzers.Tests/UnoNotImplementedTests.cs) | `3e84ceafefb16310209cf219693cd6e6d3c7d0a22293334fbaca8412fceeb7e4` |
| [src/Uno.Analyzers.Tests/UnoDoNotDisposeNativeViewsTests.cs](https://github.com/unoplatform/uno/blob/78728530f26880286be77d9042a8e4118a42df43/src/Uno.Analyzers.Tests/UnoDoNotDisposeNativeViewsTests.cs) | `b34b5cc46918c5120d1b5bc543fb8a5dc16827220d1d7a3d4845d16d026db49f` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
