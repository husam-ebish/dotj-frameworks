# DJ-050 .j XTest: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/xunit/xunit |
| Effective canonical source | https://github.com/xunit/xunit |
| Immutable analysis revision | `e91cdbe7557649b1179fbc47b01e8d3a615d1256` |
| Immutable tree | [e91cdbe7557649b1179fbc47b01e8d3a615d1256](https://github.com/xunit/xunit/tree/e91cdbe7557649b1179fbc47b01e8d3a615d1256) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1819 |
| New sampled source/API/test files | 3 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [tools/builder/Program.cs](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/tools/builder/Program.cs) | `3238c2eff5b551e8b2d1cdef59c7bc4cab5092e45798f5b09bd511b439c5693e` |
| [src/xunit.v3.core.tests/RecordTests.cs](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/RecordTests.cs) | `b7fed23656c87112b43ec858312e780f8e6167288824502d2c3e149e3a9ab9db` |
| [src/xunit.v3.core.tests/TestContextTests.cs](https://github.com/xunit/xunit/blob/e91cdbe7557649b1179fbc47b01e8d3a615d1256/src/xunit.v3.core.tests/TestContextTests.cs) | `e8a92f0f3b70cea0d0891a9dc1db7a671245941a149e00a77adc204dafef762c` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
