# DJ-048 .j Structured Log: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/serilog/serilog |
| Effective canonical source | https://github.com/serilog/serilog |
| Immutable analysis revision | `81af75f3a5e28ec9f5be18ef74357a9914a51745` |
| Immutable tree | [81af75f3a5e28ec9f5be18ef74357a9914a51745](https://github.com/serilog/serilog/tree/81af75f3a5e28ec9f5be18ef74357a9914a51745) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 284 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Serilog/Log.cs](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs) | `7f4d0ebe8b8f044c5ba3b3a9f87ce2191bdcbf644f54f1b1ce883e2b857dfe6d` |
| [src/Serilog/Guard.cs](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Guard.cs) | `7cbaf2e185c487f94f062fde7db4aedca045dabdc1520faf6066b8d53d101425` |
| [test/Serilog.Tests/LogTests.cs](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/LogTests.cs) | `897e496a9bc00332aebbe8174021632951d2e02217d8b3622a29a13360c5da20` |
| [test/Serilog.Tests/VersioningTests.cs](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/VersioningTests.cs) | `574f7f2cf4df472206b43967ac3bf3ae8ce6118330a1dad888410a2828190d96` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
