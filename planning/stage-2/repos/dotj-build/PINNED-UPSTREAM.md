# DJ-005 .j Build: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/msbuild |
| Effective canonical source | https://github.com/dotnet/msbuild |
| Immutable analysis revision | `6348d0c087aeec18c323b01a2c77da089ddafea0` |
| Immutable tree | [6348d0c087aeec18c323b01a2c77da089ddafea0](https://github.com/dotnet/msbuild/tree/6348d0c087aeec18c323b01a2c77da089ddafea0) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 3316 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Framework/ITask.cs](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/ITask.cs) | `c9944f58bb3e86aca2e732dad27eeb008d086b99a13f97105ac3513d4716b187` |
| [src/Framework/Traits.cs](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Traits.cs) | `12de8d13cfdf8295c896e1879392bd1a78938530397c057dc49d13a145a8fade` |
| [src/Tasks/Al.cs](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks/Al.cs) | `00e435c9f0dd08d32a3f828f48134a0736e9fb5dec90fddb05f1b12be646a456` |
| [src/Tasks.UnitTests/Al_Tests.cs](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/Al_Tests.cs) | `e1ad51a97dcc149ead9ef9b16b0ff89ed94311449f2338280bbb1abf4684148a` |
| [src/Tasks.UnitTests/LC_Tests.cs](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Tasks.UnitTests/LC_Tests.cs) | `b9e179954ef595e741a31b83e36ff07698ead2718f2dbf59f114016f0bf9a147` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
