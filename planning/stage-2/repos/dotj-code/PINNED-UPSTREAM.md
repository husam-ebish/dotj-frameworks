# DJ-003 .j Code: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/roslyn |
| Effective canonical source | https://github.com/dotnet/roslyn |
| Immutable analysis revision | `3645b6aa36ad41775a73e57a620787a3d38327a0` |
| Immutable tree | [3645b6aa36ad41775a73e57a620787a3d38327a0](https://github.com/dotnet/roslyn/tree/3645b6aa36ad41775a73e57a620787a3d38327a0) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 35410 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/CodeStyle/CSharp/Analyzers/PublicAPI.Shipped.txt](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/CodeStyle/CSharp/Analyzers/PublicAPI.Shipped.txt) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| [src/CodeStyle/CSharp/CodeFixes/PublicAPI.Shipped.txt](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/CodeStyle/CSharp/CodeFixes/PublicAPI.Shipped.txt) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| [src/Interactive/csi/Csi.cs](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Interactive/csi/Csi.cs) | `95c8cec76460dfd4697134afdf02b624ffdc96ae96a76fd2447d8d9411b0a964` |
| [src/Interactive/HostTest/StressTests.cs](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Interactive/HostTest/StressTests.cs) | `0544094df791d01292206fd6dc9db75aa662b8473cf991a4d201de1a19c5c70c` |
| [src/Scripting/CSharpTest/ScriptTests.cs](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs) | `bf7dbe2c47b32c8304b7a8fe25f4f23cb4a2f15fe95ccde5719747d1faff563b` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
