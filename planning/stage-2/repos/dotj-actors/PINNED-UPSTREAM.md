# DJ-015 .j Actors: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/orleans |
| Effective canonical source | https://github.com/dotnet/orleans |
| Immutable analysis revision | `9f8310cb6e5bbe35cd3bbb0752052993578eb083` |
| Immutable tree | [9f8310cb6e5bbe35cd3bbb0752052993578eb083](https://github.com/dotnet/orleans/tree/9f8310cb6e5bbe35cd3bbb0752052993578eb083) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 5904 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [docs/site/src/content/docs/dashboard/snippets/secure-dashboard/Program.cs](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/dashboard/snippets/secure-dashboard/Program.cs) | `95bb18a36365c8d6c831fa10cbfb07c2d20d812fe902977eca251e6b33af5879` |
| [docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/Program.cs](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/Program.cs) | `e384d9db175f179632fef0bea95149f462b12fce185dece3aa1b4e5b970b5e69` |
| [src/Orleans.Streaming/QueueId.cs](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/src/Orleans.Streaming/QueueId.cs) | `24fe04fa03ef9f40f4f125d7680fae32976488722ceb1c37c213b2d852ee153f` |
| [test/Orleans.Core.Tests/ConfigTests.cs](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/ConfigTests.cs) | `7387567f2ce22146fe194f4655d35f5d00653cc2aa0e2d9776fbce31120b481e` |
| [test/Orleans.Core.Tests/IdSpanTests.cs](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/test/Orleans.Core.Tests/IdSpanTests.cs) | `06ca03ac8c000dc8c418acee89792601760bf7cd1d1d9a1e88e44205ad7b46da` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
