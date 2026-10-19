# DJ-049 .j Log: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/NLog/NLog |
| Effective canonical source | https://github.com/NLog/NLog |
| Immutable analysis revision | `d9ebf823ee8ba54977c336709928a96ea58c6259` |
| Immutable tree | [d9ebf823ee8ba54977c336709928a96ea58c6259](https://github.com/NLog/NLog/tree/d9ebf823ee8ba54977c336709928a96ea58c6259) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 995 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/NLog/Logger.cs](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/src/NLog/Logger.cs) | `a8957a91d00258a982131eb6816c3f15417d7c26a36c53a6f3038f5ed34577be` |
| [src/NLog/ILogger.cs](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/src/NLog/ILogger.cs) | `a585f632e4ee1d72cf9e1def2b5dc5bb44863cf5541fd469cfc04dbc4fa7e006` |
| [tests/NLog.UnitTests/ApiTests.cs](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs) | `608b41a83126a5c28b17b3650c0bff05837ae975908d5a2be93ad048a36f3a1b` |
| [tests/NLog.UnitTests/LoggerTests.cs](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs) | `f2a53b4acd3d78c69b586ed06215ba857acfde03a4f5ebcf02b4d12449257f8c` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
