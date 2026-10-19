# DJ-022 .j Redis: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/StackExchange/StackExchange.Redis |
| Effective canonical source | https://github.com/StackExchange/StackExchange.Redis |
| Immutable analysis revision | `84765eede5c49419ed251a9cfc491a2d58667fb9` |
| Immutable tree | [84765eede5c49419ed251a9cfc491a2d58667fb9](https://github.com/StackExchange/StackExchange.Redis/tree/84765eede5c49419ed251a9cfc491a2d58667fb9) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1029 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/RESPite/PublicAPI/Debug/PublicAPI.Shipped.txt](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/src/RESPite/PublicAPI/Debug/PublicAPI.Shipped.txt) | `13c98f7e5f8065f79c391c9a60de2b2ecf10251b0fb8f105ab0f6e9b1d6b262d` |
| [src/RESPite/PublicAPI/PublicAPI.Shipped.txt](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/src/RESPite/PublicAPI/PublicAPI.Shipped.txt) | `89bf3627cc6f8c6881676de08d5c6a658d417f7de70d560d7f5bce41709f67b7` |
| [toys/AotRig/Program.cs](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/toys/AotRig/Program.cs) | `38b018a33ec9be133f4355207360891702b3e14695dbedc6dd326d53a2a604d9` |
| [tests/RESPite.Tests/RespReaderTests.cs](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/RespReaderTests.cs) | `d4162baeaad4b69b037ffaa197f738f9992b43f040cfe50adb45ad8d464967ea` |
| [tests/RESPite.Tests/CycleBufferTests.cs](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/RESPite.Tests/CycleBufferTests.cs) | `84e2fa5967b7349895205a1fb18ce9e5e2263546c6c1c112c44dc70c0d2844a4` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
