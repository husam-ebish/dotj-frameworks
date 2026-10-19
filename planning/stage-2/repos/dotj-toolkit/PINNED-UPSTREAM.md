# DJ-045 .j Toolkit: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/CommunityToolkit/dotnet |
| Effective canonical source | https://github.com/CommunityToolkit/dotnet |
| Immutable analysis revision | `b135626dd54d33b8f05f2ff31591592c004aa848` |
| Immutable tree | [b135626dd54d33b8f05f2ff31591592c004aa848](https://github.com/CommunityToolkit/dotnet/tree/b135626dd54d33b8f05f2ff31591592c004aa848) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 465 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/CommunityToolkit.Common/Converters.cs](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/src/CommunityToolkit.Common/Converters.cs) | `8dee9b54b979717b75b8d8820cbe50cc7747278e4d5f4e45080cd28214c8b0fb` |
| [src/CommunityToolkit.Common/Deferred/EventDeferral.cs](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/src/CommunityToolkit.Common/Deferred/EventDeferral.cs) | `550187edb2183972eb23d98534ffdc7e95a322baaae6aecab6035d5806bd5848` |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs) | `f10bfce42cf01462e1aa22ae67daa4a02198c9bbb7613ff90f539a0d1bc1f85b` |
| [tests/CommunityToolkit.Common.UnitTests/Test_Converters.cs](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Common.UnitTests/Test_Converters.cs) | `f5a9d41eb8a903f4a251ed4ccd46f9c95718ee5e8f7207f84ba3824212c8ccbd` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
